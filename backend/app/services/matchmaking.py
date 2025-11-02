"""
Matchmaking service for 1v1 battles
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.user import User
from app.models.battle import Battle
from app.services.ranking import RankingService


class MatchmakingService:
    """Service for finding opponents for 1v1 battles"""

    @staticmethod
    def find_opponent(
        user: User,
        db: Session,
        elo_threshold: int = 200
    ) -> Optional[User]:
        """
        Find a suitable opponent for matchmaking

        Args:
            user: User looking for a match
            db: Database session
            elo_threshold: Maximum ELO difference allowed

        Returns:
            Matched opponent User or None
        """
        # Calculate ELO range
        min_elo = user.elo_rating - elo_threshold
        max_elo = user.elo_rating + elo_threshold

        # Get users currently not in active battles
        active_battle_user_ids = db.query(Battle.user1_id).filter(
            or_(
                Battle.status == 'pending',
                Battle.status == 'active'
            )
        ).union(
            db.query(Battle.user2_id).filter(
                or_(
                    Battle.status == 'pending',
                    Battle.status == 'active'
                )
            )
        ).all()

        active_user_ids = [uid[0] for uid in active_battle_user_ids]

        # Find potential opponents
        potential_opponents = db.query(User).filter(
            and_(
                User.id != user.id,  # Not the same user
                User.elo_rating >= min_elo,
                User.elo_rating <= max_elo,
                User.id.notin_(active_user_ids) if active_user_ids else True
            )
        ).order_by(
            # Prefer opponents with similar ELO
            func.abs(User.elo_rating - user.elo_rating)
        ).limit(10).all()

        if not potential_opponents:
            # Widen the search if no matches found
            return MatchmakingService.find_opponent(
                user, db, elo_threshold=elo_threshold + 100
            ) if elo_threshold < 500 else None

        # Return the best match (closest ELO)
        return potential_opponents[0]

    @staticmethod
    def create_battle(
        user1: User,
        user2: User,
        distance_km: float,
        db: Session
    ) -> Battle:
        """
        Create a new battle between two users

        Args:
            user1: First user
            user2: Second user
            distance_km: Battle distance in kilometers
            db: Database session

        Returns:
            Created Battle object
        """
        battle = Battle(
            user1_id=user1.id,
            user2_id=user2.id,
            distance_km=distance_km,
            user1_elo_before=user1.elo_rating,
            user2_elo_before=user2.elo_rating,
            status='pending'
        )

        db.add(battle)
        db.commit()
        db.refresh(battle)

        return battle

    @staticmethod
    def complete_battle(
        battle: Battle,
        user1_distance: float,
        user2_distance: float,
        user1_time: int,
        user2_time: int,
        db: Session
    ) -> Battle:
        """
        Complete a battle and calculate results

        Args:
            battle: Battle object
            user1_distance: Distance covered by user1 in km
            user2_distance: Distance covered by user2 in km
            user1_time: Time taken by user1 in seconds
            user2_time: Time taken by user2 in seconds
            db: Database session

        Returns:
            Updated Battle object
        """
        from datetime import datetime

        # Update battle stats
        battle.user1_distance = user1_distance
        battle.user2_distance = user2_distance
        battle.user1_time = user1_time
        battle.user2_time = user2_time

        # Calculate pace
        if user1_distance > 0:
            battle.user1_pace = (user1_time / 60) / user1_distance
        if user2_distance > 0:
            battle.user2_pace = (user2_time / 60) / user2_distance

        # Determine winner (who completed the distance faster)
        # If both completed, faster time wins
        # If only one completed, they win
        # If neither completed, longer distance wins

        distance_threshold = battle.distance_km * 0.99  # 99% of target

        user1_completed = user1_distance >= distance_threshold
        user2_completed = user2_distance >= distance_threshold

        if user1_completed and user2_completed:
            # Both completed - faster time wins
            winner_id = battle.user1_id if user1_time < user2_time else battle.user2_id
        elif user1_completed:
            winner_id = battle.user1_id
        elif user2_completed:
            winner_id = battle.user2_id
        else:
            # Neither completed - longer distance wins
            winner_id = battle.user1_id if user1_distance > user2_distance else battle.user2_id

        battle.winner_id = winner_id

        # Calculate ELO changes
        user1 = db.query(User).filter(User.id == battle.user1_id).first()
        user2 = db.query(User).filter(User.id == battle.user2_id).first()

        if winner_id == battle.user1_id:
            new_user1_elo, new_user2_elo = RankingService.calculate_elo_change(
                user1.elo_rating, user2.elo_rating
            )
        else:
            new_user2_elo, new_user1_elo = RankingService.calculate_elo_change(
                user2.elo_rating, user1.elo_rating
            )

        # Update battle ELO
        battle.user1_elo_after = new_user1_elo
        battle.user2_elo_after = new_user2_elo

        # Update users
        user1_elo_change = new_user1_elo - user1.elo_rating
        user2_elo_change = new_user2_elo - user2.elo_rating

        user1.elo_rating = new_user1_elo
        user2.elo_rating = new_user2_elo

        user1.league_tier = RankingService.get_tier_from_elo(new_user1_elo)
        user2.league_tier = RankingService.get_tier_from_elo(new_user2_elo)

        user1.league_points += RankingService.calculate_league_points(user1_elo_change)
        user2.league_points += RankingService.calculate_league_points(user2_elo_change)

        # Update battle status
        battle.status = 'completed'
        battle.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(battle)

        return battle

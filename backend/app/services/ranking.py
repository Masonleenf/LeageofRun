"""
Ranking and ELO calculation service
"""
from typing import Tuple


class RankingService:
    """Service for calculating ELO ratings and league tiers"""

    # League tier thresholds
    TIERS = {
        'Bronze': (0, 1299),
        'Silver': (1300, 1499),
        'Gold': (1500, 1699),
        'Platinum': (1700, 1899),
        'Diamond': (1900, float('inf'))
    }

    # K-factor for ELO calculation (higher = more volatile)
    K_FACTOR = 32

    @staticmethod
    def calculate_elo_change(
        winner_elo: int,
        loser_elo: int,
        k_factor: int = K_FACTOR
    ) -> Tuple[int, int]:
        """
        Calculate new ELO ratings after a match

        Args:
            winner_elo: Current ELO of winner
            loser_elo: Current ELO of loser
            k_factor: K-factor for ELO calculation

        Returns:
            Tuple of (new_winner_elo, new_loser_elo)
        """
        # Expected scores
        expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

        # Actual scores (winner gets 1, loser gets 0)
        actual_winner = 1
        actual_loser = 0

        # Calculate new ratings
        new_winner_elo = round(winner_elo + k_factor * (actual_winner - expected_winner))
        new_loser_elo = round(loser_elo + k_factor * (actual_loser - expected_loser))

        return new_winner_elo, new_loser_elo

    @staticmethod
    def get_tier_from_elo(elo: int) -> str:
        """
        Get league tier based on ELO rating

        Args:
            elo: ELO rating

        Returns:
            Tier name (Bronze, Silver, Gold, Platinum, Diamond)
        """
        for tier, (min_elo, max_elo) in RankingService.TIERS.items():
            if min_elo <= elo <= max_elo:
                return tier
        return 'Bronze'

    @staticmethod
    def calculate_league_points(elo_change: int) -> int:
        """
        Calculate league points gained/lost based on ELO change

        Args:
            elo_change: Change in ELO rating

        Returns:
            League points to add (positive for gain, negative for loss)
        """
        # League points = ELO change * 2
        return elo_change * 2

    @staticmethod
    def is_similar_skill(elo1: int, elo2: int, threshold: int = 200) -> bool:
        """
        Check if two players have similar skill levels for matchmaking

        Args:
            elo1: First player's ELO
            elo2: Second player's ELO
            threshold: Maximum ELO difference allowed

        Returns:
            True if players are within threshold
        """
        return abs(elo1 - elo2) <= threshold

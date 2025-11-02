-- RunBattle Database Schema
-- Execute this in Supabase SQL Editor: https://rfmczdnkfijskblccqql.supabase.co

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(500),
    weight_kg FLOAT DEFAULT 70.0,

    -- Stats
    total_distance_km FLOAT DEFAULT 0.0,
    total_duration_seconds INTEGER DEFAULT 0,
    total_runs INTEGER DEFAULT 0,
    avg_pace FLOAT DEFAULT 0.0,

    -- Rankings
    elo_rating INTEGER DEFAULT 1200,
    league_tier VARCHAR(20) DEFAULT 'Bronze',
    league_points INTEGER DEFAULT 0,

    -- Integrations
    strava_access_token VARCHAR(255),
    strava_refresh_token VARCHAR(255),
    strava_athlete_id VARCHAR(50),

    -- Premium
    is_premium BOOLEAN DEFAULT FALSE,
    premium_expires_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);

-- Runs table
CREATE TABLE IF NOT EXISTS runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Metrics
    distance_km FLOAT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    avg_pace FLOAT NOT NULL,
    avg_speed FLOAT NOT NULL,
    calories_burned FLOAT DEFAULT 0.0,

    -- Route data
    route_polyline TEXT,
    start_lat FLOAT,
    start_lng FLOAT,
    end_lat FLOAT,
    end_lng FLOAT,

    -- Timestamps
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    -- Source
    source VARCHAR(20) DEFAULT 'app',
    external_id VARCHAR(100)
);

-- Battles table
CREATE TABLE IF NOT EXISTS battles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Participants
    user1_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Battle config
    distance_km FLOAT NOT NULL,

    -- Results
    winner_id UUID REFERENCES users(id) ON DELETE SET NULL,
    user1_distance FLOAT DEFAULT 0.0,
    user2_distance FLOAT DEFAULT 0.0,
    user1_time INTEGER DEFAULT 0,
    user2_time INTEGER DEFAULT 0,
    user1_pace FLOAT DEFAULT 0.0,
    user2_pace FLOAT DEFAULT 0.0,

    -- ELO changes
    user1_elo_before INTEGER,
    user2_elo_before INTEGER,
    user1_elo_after INTEGER,
    user2_elo_after INTEGER,

    -- Status: 'pending', 'active', 'completed', 'cancelled'
    status VARCHAR(20) DEFAULT 'pending',

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Crews table
CREATE TABLE IF NOT EXISTS crews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    avatar_url VARCHAR(500),

    captain_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Stats
    total_members INTEGER DEFAULT 0,
    total_distance_km FLOAT DEFAULT 0.0,
    total_runs INTEGER DEFAULT 0,
    battle_wins INTEGER DEFAULT 0,
    battle_losses INTEGER DEFAULT 0,

    -- Settings
    is_public BOOLEAN DEFAULT TRUE,
    max_members INTEGER DEFAULT 50,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Crew Memberships table
CREATE TABLE IF NOT EXISTS crew_memberships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crew_id UUID NOT NULL REFERENCES crews(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    role VARCHAR(20) DEFAULT 'member',

    joined_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(crew_id, user_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_elo ON users(elo_rating);
CREATE INDEX IF NOT EXISTS idx_runs_user_id ON runs(user_id);
CREATE INDEX IF NOT EXISTS idx_runs_completed_at ON runs(completed_at DESC);
CREATE INDEX IF NOT EXISTS idx_battles_user1 ON battles(user1_id);
CREATE INDEX IF NOT EXISTS idx_battles_user2 ON battles(user2_id);
CREATE INDEX IF NOT EXISTS idx_battles_status ON battles(status);
CREATE INDEX IF NOT EXISTS idx_crew_memberships_crew ON crew_memberships(crew_id);
CREATE INDEX IF NOT EXISTS idx_crew_memberships_user ON crew_memberships(user_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_crews_updated_at BEFORE UPDATE ON crews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ All tables created successfully!';
    RAISE NOTICE 'Tables: users, runs, battles, crews, crew_memberships';
END $$;

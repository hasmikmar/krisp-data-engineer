-- Create the users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the sessions table, which references the users table
CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    device_id VARCHAR(255),
    platform VARCHAR(255),
    location VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the user_metrics table, which references the sessions table
CREATE TABLE user_metrics (
    metric_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES sessions(session_id) ON DELETE CASCADE,
    talked_time INTERVAL,
    microphone_used BOOLEAN,
    speaker_used BOOLEAN,
    voice_sentiment VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices for performance optimization
CREATE INDEX idx_user_metrics_timestamp ON user_metrics (timestamp);
CREATE INDEX idx_sessions_user_id ON sessions (user_id);
CREATE INDEX idx_user_metrics_session_id ON user_metrics (session_id);
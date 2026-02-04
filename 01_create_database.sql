-- Running Tracker Database Schema
-- Database: running_tracker
-- Description: Track your runs, routes, shoes, and training goals

DROP DATABASE IF EXISTS running_tracker;
CREATE DATABASE running_tracker;
USE running_tracker;

-- Table 1: Runners
-- Stores information about individual runners
CREATE TABLE runners (
    runner_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    gender ENUM('M', 'F', 'Other') DEFAULT 'Other',
    weight_lbs DECIMAL(5,2),
    height_inches INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_name (last_name, first_name)
);

-- Table 2: Running Shoes
-- Track different pairs of running shoes and their mileage
CREATE TABLE running_shoes (
    shoe_id INT PRIMARY KEY AUTO_INCREMENT,
    runner_id INT NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    purchase_date DATE NOT NULL,
    total_miles DECIMAL(7,2) DEFAULT 0,
    retired BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (runner_id) REFERENCES runners(runner_id) ON DELETE CASCADE,
    INDEX idx_runner (runner_id),
    INDEX idx_active (retired)
);

-- Table 3: Routes
-- Store favorite running routes
CREATE TABLE routes (
    route_id INT PRIMARY KEY AUTO_INCREMENT,
    runner_id INT NOT NULL,
    route_name VARCHAR(100) NOT NULL,
    distance_miles DECIMAL(5,2) NOT NULL,
    elevation_gain_ft INT DEFAULT 0,
    surface_type ENUM('Road', 'Trail', 'Track', 'Treadmill', 'Mixed') DEFAULT 'Road',
    description TEXT,
    start_location VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (runner_id) REFERENCES runners(runner_id) ON DELETE CASCADE,
    INDEX idx_runner (runner_id),
    INDEX idx_distance (distance_miles)
);

-- Table 4: Runs
-- Main table storing individual run records
CREATE TABLE runs (
    run_id INT PRIMARY KEY AUTO_INCREMENT,
    runner_id INT NOT NULL,
    route_id INT,
    shoe_id INT,
    run_date DATE NOT NULL,
    distance_miles DECIMAL(5,2) NOT NULL,
    duration_minutes INT NOT NULL,
    pace_min_per_mile DECIMAL(5,2) GENERATED ALWAYS AS (duration_minutes / distance_miles) STORED,
    average_heart_rate INT,
    calories_burned INT,
    weather VARCHAR(50),
    temperature_f INT,
    run_type ENUM('Easy', 'Tempo', 'Interval', 'Long', 'Race', 'Recovery') DEFAULT 'Easy',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (runner_id) REFERENCES runners(runner_id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE SET NULL,
    FOREIGN KEY (shoe_id) REFERENCES running_shoes(shoe_id) ON DELETE SET NULL,
    INDEX idx_runner_date (runner_id, run_date),
    INDEX idx_date (run_date),
    INDEX idx_distance (distance_miles)
);

-- Table 5: Training Goals
-- Track training goals and progress
CREATE TABLE training_goals (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    runner_id INT NOT NULL,
    goal_type ENUM('Distance', 'Time', 'Pace', 'Race', 'Weight', 'Weekly_Mileage') NOT NULL,
    target_value DECIMAL(10,2) NOT NULL,
    current_value DECIMAL(10,2) DEFAULT 0,
    target_date DATE,
    status ENUM('Active', 'Completed', 'Abandoned') DEFAULT 'Active',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (runner_id) REFERENCES runners(runner_id) ON DELETE CASCADE,
    INDEX idx_runner (runner_id),
    INDEX idx_status (status)
);

-- Create views for common queries
CREATE VIEW runner_statistics AS
SELECT 
    r.runner_id,
    CONCAT(r.first_name, ' ', r.last_name) AS runner_name,
    COUNT(ru.run_id) AS total_runs,
    COALESCE(SUM(ru.distance_miles), 0) AS total_miles,
    COALESCE(AVG(ru.pace_min_per_mile), 0) AS average_pace,
    COALESCE(MIN(ru.pace_min_per_mile), 0) AS best_pace,
    COALESCE(MAX(ru.distance_miles), 0) AS longest_run
FROM runners r
LEFT JOIN runs ru ON r.runner_id = ru.runner_id
GROUP BY r.runner_id, r.first_name, r.last_name;

CREATE VIEW recent_runs AS
SELECT 
    ru.run_id,
    CONCAT(r.first_name, ' ', r.last_name) AS runner_name,
    ru.run_date,
    ru.distance_miles,
    ru.duration_minutes,
    ru.pace_min_per_mile,
    ru.run_type,
    rt.route_name,
    CONCAT(rs.brand, ' ', rs.model) AS shoe_name
FROM runs ru
JOIN runners r ON ru.runner_id = r.runner_id
LEFT JOIN routes rt ON ru.route_id = rt.route_id
LEFT JOIN running_shoes rs ON ru.shoe_id = rs.shoe_id
ORDER BY ru.run_date DESC, ru.created_at DESC
LIMIT 20;

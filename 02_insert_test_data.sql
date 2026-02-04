-- Running Tracker Test Data
-- Populates the database with realistic running data

USE running_tracker;

-- Insert Runners (5 runners)
INSERT INTO runners (first_name, last_name, email, date_of_birth, gender, weight_lbs, height_inches) VALUES
('Sarah', 'Johnson', 'sarah.johnson@email.com', '1990-05-15', 'F', 135.5, 66),
('Mike', 'Chen', 'mike.chen@email.com', '1985-08-22', 'M', 175.0, 71),
('Emily', 'Rodriguez', 'emily.rodriguez@email.com', '1992-11-30', 'F', 125.0, 64),
('James', 'Williams', 'james.williams@email.com', '1988-03-10', 'M', 185.5, 73),
('Alex', 'Taylor', 'alex.taylor@email.com', '1995-07-18', 'Other', 155.0, 68);

-- Insert Running Shoes (10 pairs of shoes)
INSERT INTO running_shoes (runner_id, brand, model, purchase_date, total_miles, retired, notes) VALUES
(1, 'Nike', 'Pegasus 40', '2024-01-15', 245.8, FALSE, 'Great for daily training'),
(1, 'Brooks', 'Ghost 15', '2023-06-20', 512.3, TRUE, 'Retired after 500 miles'),
(2, 'Hoka', 'Clifton 9', '2024-03-01', 156.2, FALSE, 'Very cushioned'),
(2, 'Asics', 'Gel-Nimbus 25', '2023-11-10', 387.5, FALSE, 'Good for long runs'),
(3, 'New Balance', 'Fresh Foam 1080', '2024-02-14', 189.7, FALSE, 'Comfortable fit'),
(3, 'Saucony', 'Triumph 21', '2023-08-05', 445.0, TRUE, 'Loved these shoes'),
(4, 'Adidas', 'Ultraboost 23', '2024-01-20', 213.4, FALSE, 'Responsive and fast'),
(4, 'Nike', 'Vaporfly 3', '2024-04-01', 78.5, FALSE, 'Race day shoes only'),
(5, 'Brooks', 'Adrenaline GTS 23', '2024-02-28', 167.9, FALSE, 'Good stability'),
(5, 'Hoka', 'Speedgoat 5', '2023-12-15', 298.6, FALSE, 'Trail running');

-- Insert Routes (12 routes)
INSERT INTO routes (runner_id, route_name, distance_miles, elevation_gain_ft, surface_type, description, start_location) VALUES
(1, 'Park Loop', 3.5, 45, 'Road', 'Easy loop around Central Park', 'Central Park Entrance'),
(1, 'Riverfront Trail', 5.0, 120, 'Trail', 'Scenic trail along the river', 'Riverside Park'),
(1, 'Downtown Circuit', 4.2, 80, 'Road', 'City streets with some hills', 'City Hall'),
(2, 'Hill Repeats Route', 2.0, 250, 'Road', 'Steep hill for training', 'Highland Ave'),
(2, 'Long Beach Run', 10.0, 30, 'Road', 'Flat beachfront run', 'Beach Parking Lot'),
(2, 'Track Workout', 0.25, 0, 'Track', 'Local high school track', 'Jefferson High School'),
(3, 'Neighborhood Loop', 3.0, 55, 'Road', 'Around the neighborhood', 'Home'),
(3, 'Mountain Trail', 6.5, 850, 'Trail', 'Challenging mountain trail', 'Trailhead Parking'),
(4, 'Morning Commute', 4.8, 95, 'Road', 'Run to work route', 'Home to Office'),
(4, 'Greenway Path', 8.0, 140, 'Mixed', 'Mixed surface greenway', 'Greenway North Entrance'),
(5, 'Cemetery Hills', 5.5, 320, 'Road', 'Rolling hills through historic cemetery', 'Main Gate'),
(5, 'Lake Loop', 7.2, 180, 'Trail', 'Around the entire lake', 'Lake Visitor Center');

-- Insert Runs (60 runs to ensure 50+ rows)
INSERT INTO runs (runner_id, route_id, shoe_id, run_date, distance_miles, duration_minutes, average_heart_rate, calories_burned, weather, temperature_f, run_type, notes) VALUES
-- Sarah's runs (Runner 1)
(1, 1, 1, '2025-01-05', 3.5, 31, 145, 320, 'Sunny', 55, 'Easy', 'Felt great today'),
(1, 2, 1, '2025-01-07', 5.0, 47, 152, 485, 'Cloudy', 48, 'Long', 'Good endurance run'),
(1, 3, 1, '2025-01-10', 4.2, 36, 158, 398, 'Rainy', 42, 'Tempo', 'Pushed the pace'),
(1, 1, 1, '2025-01-12', 3.5, 30, 142, 315, 'Sunny', 58, 'Easy', 'Recovery run'),
(1, 2, 1, '2025-01-15', 5.0, 46, 155, 490, 'Partly Cloudy', 52, 'Easy', 'Nice weather'),
(1, 3, 1, '2025-01-17', 4.2, 35, 160, 405, 'Windy', 45, 'Tempo', 'Fighting headwind'),
(1, 1, 1, '2025-01-20', 3.5, 29, 148, 325, 'Sunny', 60, 'Easy', 'Beautiful morning'),
(1, 2, 1, '2025-01-22', 5.0, 45, 150, 480, 'Foggy', 50, 'Long', 'Good long run'),
(1, 3, 1, '2025-01-25', 4.2, 37, 156, 395, 'Clear', 54, 'Easy', 'Feeling strong'),
(1, 1, 1, '2025-01-27', 3.5, 31, 144, 318, 'Sunny', 62, 'Recovery', 'Light and easy'),
(1, 2, 1, '2025-01-30', 6.0, 56, 158, 590, 'Cloudy', 47, 'Long', 'Extended the route'),
(1, 3, 1, '2025-02-01', 4.2, 34, 162, 410, 'Clear', 56, 'Tempo', 'Personal best pace!'),

-- Mike's runs (Runner 2)
(2, 4, 3, '2025-01-06', 2.0, 18, 165, 215, 'Clear', 50, 'Interval', '8 x hill repeats'),
(2, 5, 3, '2025-01-08', 10.0, 82, 148, 1020, 'Sunny', 58, 'Long', 'Smooth long run'),
(2, 6, 3, '2025-01-11', 4.0, 28, 172, 425, 'Cloudy', 52, 'Interval', 'Track intervals'),
(2, 4, 3, '2025-01-13', 2.0, 17, 168, 220, 'Sunny', 55, 'Interval', 'Hill workout'),
(2, 5, 3, '2025-01-16', 10.0, 80, 150, 1015, 'Partly Cloudy', 60, 'Long', 'Great run'),
(2, 6, 4, '2025-01-18', 5.0, 35, 170, 530, 'Clear', 57, 'Interval', '400m repeats'),
(2, 4, 3, '2025-01-21', 2.0, 18, 166, 218, 'Windy', 48, 'Interval', 'Tough hills'),
(2, 5, 3, '2025-01-24', 10.0, 81, 152, 1025, 'Sunny', 62, 'Long', 'Fantastic weather'),
(2, 6, 4, '2025-01-26', 3.5, 25, 174, 375, 'Cloudy', 54, 'Interval', 'Speed work'),
(2, 4, 3, '2025-01-29', 2.0, 17, 169, 222, 'Clear', 59, 'Interval', 'Strong hills'),
(2, 5, 3, '2025-02-02', 10.0, 79, 149, 1010, 'Sunny', 65, 'Long', 'Best long run yet'),

-- Emily's runs (Runner 3)
(3, 7, 5, '2025-01-04', 3.0, 28, 138, 285, 'Clear', 52, 'Easy', 'Morning run'),
(3, 8, 5, '2025-01-09', 6.5, 68, 155, 685, 'Partly Cloudy', 48, 'Long', 'Trail adventure'),
(3, 7, 5, '2025-01-11', 3.0, 27, 140, 280, 'Sunny', 58, 'Easy', 'Quick neighborhood loop'),
(3, 8, 5, '2025-01-14', 6.5, 66, 158, 695, 'Cloudy', 45, 'Long', 'Challenging terrain'),
(3, 7, 5, '2025-01-16', 3.0, 26, 142, 290, 'Clear', 60, 'Recovery', 'Easy recovery'),
(3, 8, 5, '2025-01-19', 6.5, 65, 160, 700, 'Sunny', 55, 'Long', 'Getting stronger'),
(3, 7, 5, '2025-01-23', 3.0, 28, 139, 282, 'Rainy', 50, 'Easy', 'Wet but good'),
(3, 8, 5, '2025-01-26', 6.5, 64, 157, 690, 'Clear', 58, 'Long', 'Amazing trail run'),
(3, 7, 5, '2025-01-28', 3.0, 27, 141, 287, 'Sunny', 62, 'Easy', 'Perfect weather'),
(3, 8, 5, '2025-01-31', 6.5, 67, 159, 698, 'Partly Cloudy', 54, 'Long', 'Solid trail run'),

-- James's runs (Runner 4)
(4, 9, 7, '2025-01-03', 4.8, 38, 142, 505, 'Clear', 45, 'Easy', 'Commute run'),
(4, 10, 7, '2025-01-06', 8.0, 64, 150, 845, 'Sunny', 52, 'Long', 'Greenway exploration'),
(4, 9, 7, '2025-01-09', 4.8, 36, 145, 515, 'Cloudy', 48, 'Tempo', 'Faster commute'),
(4, 10, 7, '2025-01-12', 8.0, 62, 152, 855, 'Clear', 55, 'Long', 'Good distance'),
(4, 9, 7, '2025-01-15', 4.8, 37, 148, 520, 'Partly Cloudy', 50, 'Easy', 'Regular commute'),
(4, 10, 8, '2025-01-18', 5.0, 35, 165, 560, 'Sunny', 58, 'Race', 'Testing race shoes'),
(4, 9, 7, '2025-01-21', 4.8, 36, 146, 512, 'Windy', 46, 'Tempo', 'Windy but fast'),
(4, 10, 7, '2025-01-24', 8.0, 63, 151, 850, 'Clear', 60, 'Long', 'Strong finish'),
(4, 9, 7, '2025-01-27', 4.8, 38, 144, 508, 'Sunny', 62, 'Easy', 'Easy Monday'),
(4, 10, 8, '2025-01-30', 5.0, 34, 168, 565, 'Clear', 65, 'Race', 'Race pace practice'),

-- Alex's runs (Runner 5)
(5, 11, 9, '2025-01-05', 5.5, 50, 152, 575, 'Cloudy', 50, 'Easy', 'Cemetery hills'),
(5, 12, 10, '2025-01-08', 7.2, 68, 148, 765, 'Sunny', 55, 'Long', 'Lake loop complete'),
(5, 11, 9, '2025-01-11', 5.5, 48, 155, 585, 'Clear', 58, 'Tempo', 'Good hill work'),
(5, 12, 10, '2025-01-14', 7.2, 66, 150, 775, 'Partly Cloudy', 52, 'Long', 'Trail running'),
(5, 11, 9, '2025-01-17', 5.5, 49, 153, 580, 'Rainy', 48, 'Easy', 'Rainy hill run'),
(5, 12, 10, '2025-01-20', 7.2, 65, 152, 785, 'Sunny', 60, 'Long', 'Beautiful lake day'),
(5, 11, 9, '2025-01-23', 5.5, 47, 156, 590, 'Clear', 62, 'Tempo', 'Strong tempo'),
(5, 12, 10, '2025-01-26', 7.2, 67, 149, 770, 'Cloudy', 54, 'Long', 'Good endurance'),
(5, 11, 9, '2025-01-29', 5.5, 50, 154, 578, 'Sunny', 65, 'Easy', 'Easy hills'),
(5, 12, 10, '2025-02-01', 7.2, 64, 151, 780, 'Clear', 68, 'Long', 'Perfect conditions');

-- Insert Training Goals (8 goals)
INSERT INTO training_goals (runner_id, goal_type, target_value, current_value, target_date, status, description) VALUES
(1, 'Weekly_Mileage', 25.0, 18.5, '2025-03-01', 'Active', 'Build up weekly mileage safely'),
(1, 'Race', 210.0, 0, '2025-05-15', 'Active', 'Run half marathon under 3:30:00'),
(2, 'Distance', 13.1, 10.0, '2025-04-01', 'Active', 'Complete first half marathon'),
(2, 'Pace', 7.5, 8.2, '2025-06-01', 'Active', 'Improve average pace to 7:30/mile'),
(3, 'Weekly_Mileage', 30.0, 22.0, '2025-04-15', 'Active', 'Increase weekly volume for trail ultra'),
(3, 'Distance', 26.2, 15.0, '2025-07-04', 'Active', 'Complete first marathon'),
(4, 'Time', 90.0, 120.0, '2025-03-01', 'Active', 'Run 10K in under 90 minutes'),
(5, 'Race', 240.0, 0, '2025-08-15', 'Active', 'Finish marathon under 4 hours');

-- Update shoe mileage based on runs (this is a simplified update)
UPDATE running_shoes rs
SET total_miles = (
    SELECT COALESCE(SUM(r.distance_miles), 0)
    FROM runs r
    WHERE r.shoe_id = rs.shoe_id
);

-- Show row counts to verify data insertion
SELECT 'Runners' AS table_name, COUNT(*) AS row_count FROM runners
UNION ALL
SELECT 'Running Shoes', COUNT(*) FROM running_shoes
UNION ALL
SELECT 'Routes', COUNT(*) FROM routes
UNION ALL
SELECT 'Runs', COUNT(*) FROM runs
UNION ALL
SELECT 'Training Goals', COUNT(*) FROM training_goals
UNION ALL
SELECT 'TOTAL', 
    (SELECT COUNT(*) FROM runners) +
    (SELECT COUNT(*) FROM running_shoes) +
    (SELECT COUNT(*) FROM routes) +
    (SELECT COUNT(*) FROM runs) +
    (SELECT COUNT(*) FROM training_goals);

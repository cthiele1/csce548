-- Running Tracker Verification Queries
-- Use these queries to verify data and create screenshots

USE running_tracker;

-- 1. Verify total row count (should be 95+ total)
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
SELECT '--- TOTAL ---', 
    (SELECT COUNT(*) FROM runners) +
    (SELECT COUNT(*) FROM running_shoes) +
    (SELECT COUNT(*) FROM routes) +
    (SELECT COUNT(*) FROM runs) +
    (SELECT COUNT(*) FROM training_goals);

-- 2. Show all tables in database
SHOW TABLES;

-- 3. Verify runs table has 50+ rows (actually has 60)
SELECT COUNT(*) AS total_runs FROM runs;

-- 4. Show recent runs with all details
SELECT * FROM recent_runs LIMIT 10;

-- 5. Show runner statistics
SELECT * FROM runner_statistics;

-- 6. Show sample data from each table

-- Runners
SELECT runner_id, CONCAT(first_name, ' ', last_name) AS name, email, 
       weight_lbs, height_inches 
FROM runners;

-- Running Shoes
SELECT shoe_id, runner_id, CONCAT(brand, ' ', model) AS shoe, 
       purchase_date, total_miles, 
       CASE WHEN retired THEN 'Retired' ELSE 'Active' END AS status
FROM running_shoes
ORDER BY total_miles DESC;

-- Routes  
SELECT route_id, runner_id, route_name, distance_miles, 
       elevation_gain_ft, surface_type
FROM routes
ORDER BY distance_miles DESC;

-- Runs (showing variety of data)
SELECT run_id, runner_id, run_date, distance_miles, duration_minutes,
       pace_min_per_mile, run_type, weather, temperature_f
FROM runs
ORDER BY run_date DESC
LIMIT 20;

-- Training Goals
SELECT goal_id, runner_id, goal_type, target_value, current_value,
       CONCAT(ROUND((current_value/target_value)*100, 1), '%') AS progress,
       target_date, status
FROM training_goals
ORDER BY status, target_date;

-- 7. Advanced analytics queries

-- Total miles per runner
SELECT 
    r.runner_id,
    CONCAT(r.first_name, ' ', r.last_name) AS runner_name,
    COUNT(ru.run_id) AS total_runs,
    ROUND(SUM(ru.distance_miles), 2) AS total_miles,
    ROUND(AVG(ru.pace_min_per_mile), 2) AS avg_pace_min_per_mile,
    ROUND(MIN(ru.pace_min_per_mile), 2) AS best_pace,
    ROUND(MAX(ru.distance_miles), 2) AS longest_run
FROM runners r
LEFT JOIN runs ru ON r.runner_id = ru.runner_id
GROUP BY r.runner_id, r.first_name, r.last_name
ORDER BY total_miles DESC;

-- Shoe mileage report
SELECT 
    rs.shoe_id,
    CONCAT(r.first_name, ' ', r.last_name) AS runner_name,
    CONCAT(rs.brand, ' ', rs.model) AS shoe,
    rs.purchase_date,
    ROUND(rs.total_miles, 2) AS total_miles,
    CASE 
        WHEN rs.retired THEN 'Retired'
        WHEN rs.total_miles >= 400 THEN 'Replace Soon'
        ELSE 'Active'
    END AS status
FROM running_shoes rs
JOIN runners r ON rs.runner_id = r.runner_id
ORDER BY rs.total_miles DESC;

-- Most popular routes
SELECT 
    rt.route_name,
    rt.distance_miles,
    COUNT(ru.run_id) AS times_run,
    ROUND(AVG(ru.pace_min_per_mile), 2) AS avg_pace
FROM routes rt
LEFT JOIN runs ru ON rt.route_id = ru.route_id
GROUP BY rt.route_id, rt.route_name, rt.distance_miles
HAVING times_run > 0
ORDER BY times_run DESC;

-- Weekly mileage by runner (last 4 weeks)
SELECT 
    CONCAT(r.first_name, ' ', r.last_name) AS runner_name,
    YEARWEEK(ru.run_date) AS week,
    COUNT(ru.run_id) AS runs_this_week,
    ROUND(SUM(ru.distance_miles), 2) AS weekly_miles
FROM runners r
JOIN runs ru ON r.runner_id = ru.runner_id
WHERE ru.run_date >= DATE_SUB(CURDATE(), INTERVAL 4 WEEK)
GROUP BY r.runner_id, r.first_name, r.last_name, YEARWEEK(ru.run_date)
ORDER BY week DESC, weekly_miles DESC;

-- Goal progress report
SELECT 
    CONCAT(r.first_name, ' ', r.last_name) AS runner_name,
    tg.goal_type,
    tg.target_value,
    tg.current_value,
    CONCAT(ROUND((tg.current_value/tg.target_value)*100, 1), '%') AS progress,
    tg.target_date,
    tg.status,
    CASE 
        WHEN tg.status = 'Completed' THEN 'Goal Achieved!'
        WHEN tg.target_date < CURDATE() THEN 'Past Due'
        WHEN DATEDIFF(tg.target_date, CURDATE()) <= 30 THEN 'Due Soon'
        ELSE 'On Track'
    END AS urgency
FROM training_goals tg
JOIN runners r ON tg.runner_id = r.runner_id
ORDER BY tg.status, tg.target_date;

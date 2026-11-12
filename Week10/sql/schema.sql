CREATE DATABASE IF NOT EXISTS capstone_week10 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE capstone_week10;
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    status ENUM('계획','진행','완료') NOT NULL DEFAULT '계획'
);
-- 아래 데이터는 비어 있는 테이블에서 최초 1회만 추가합니다.
INSERT INTO projects(title,status)
SELECT '스마트 화분','계획' WHERE NOT EXISTS (SELECT 1 FROM projects);
INSERT INTO projects(title,status)
SELECT '교실 환경 모니터','진행' WHERE NOT EXISTS (SELECT 1 FROM projects WHERE title='교실 환경 모니터');

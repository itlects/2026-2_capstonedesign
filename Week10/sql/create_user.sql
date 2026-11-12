-- CHANGE_ME를 본인의 실습 암호로 변경하고 root로 실행합니다.
CREATE USER IF NOT EXISTS 'capstone_app'@'127.0.0.1' IDENTIFIED BY 'CHANGE_ME';
GRANT SELECT, INSERT, UPDATE, DELETE ON capstone_week10.* TO 'capstone_app'@'127.0.0.1';
-- 이미 존재하는 계정은 CREATE USER로 암호가 변경되지 않습니다.
-- 필요 시 ALTER USER 'capstone_app'@'127.0.0.1' IDENTIFIED BY '새암호';

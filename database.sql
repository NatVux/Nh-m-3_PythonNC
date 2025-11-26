CREATE DATABASE IF NOT EXISTS StudentInforManagement;
USE StudentInforManagement;

-- 1️⃣ Department
CREATE TABLE IF NOT EXISTS Department (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

INSERT INTO Department (department_name)
VALUES ('Công nghệ thông tin'), ('Kinh tế'), ('Điện tử');

-- 2️⃣ Major
CREATE TABLE IF NOT EXISTS Major (
    major_id INT AUTO_INCREMENT PRIMARY KEY,
    major_name VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Major (major_name, department_id)
VALUES
('Công nghệ thông tin',1),
('Kĩ thuật phần mềm',1),
('Kinh tế quốc tế',2),
('Kinh doanh quốc tế',2),
('Điện tử viễn thông', 3),
('Tự động hóa', 3);

-- 3️⃣ Class
CREATE TABLE IF NOT EXISTS Class (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    major_id INT NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (major_id) REFERENCES Major(major_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Class (class_name, major_id, department_id)
VALUES
('2022CNTT01',1,1),
('2022CNTT05',1,1),
('2022KTPM01',2,1),
('2022KTPM02',2,1),
('2022KTQT01',3,2),
('2022KTQT02',3,2),
('2022KDQT01',4,2),
('2022KDQT02',4,2),
('2022DTVT01',5,3),
('2022DTVT02',5,3),
('2022TDH01',6,3),
('2022TDH02',6,3);

-- 4️⃣ Student
CREATE TABLE IF NOT EXISTS Student (
    student_id CHAR(10) PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL,
    student_birth DATE NOT NULL,
    student_address VARCHAR(150),
    student_cccd CHAR(12) UNIQUE,
    student_phone VARCHAR(20),
    student_email VARCHAR(100) UNIQUE,
    student_gender ENUM('Nam','Nữ','Khác'),
    student_generation VARCHAR(10),
    student_image VARCHAR(500),
    class_id INT NOT NULL,
    major_id INT NOT NULL,
    FOREIGN KEY (major_id) REFERENCES Major(major_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 5️⃣ Subject
CREATE TABLE IF NOT EXISTS Subject (
    subject_id CHAR(10) PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    subject_credit INT NOT NULL
);

INSERT INTO Subject (subject_id, subject_name, subject_credit)
VALUES
('PE6021','Bóng rổ',1),
('FL6085','Tiếng anh CNTT cơ bản 1',5),
('BS6002','Giải tích',3),
('LP6010','Triết học Mác-Lênin',3),
('BM6091','Quản lý dự án',2);

-- 6️⃣ Subject_Student
CREATE TABLE IF NOT EXISTS Subject_Student (
    subject_id CHAR(10) NOT NULL,
    student_id CHAR(10) NOT NULL,
    ss_semester VARCHAR(50) NOT NULL,
    score_regular FLOAT,
    score_midterm FLOAT,
    score_final FLOAT,
    PRIMARY KEY (subject_id, student_id, ss_semester),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 7️⃣ Account
CREATE TABLE IF NOT EXISTS Account (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    account_username VARCHAR(30) UNIQUE,
    account_password VARCHAR(50),
    account_name VARCHAR(50)
);

INSERT INTO Account (account_username, account_password, account_name)
VALUES
('xuanbac','123456','Mai Xuân Bắc'),
('trongtan','18052024','Vũ Trọng Tấn');

-- ✅ Index test
CREATE INDEX idx_student_name ON Student(student_name);
EXPLAIN SELECT * FROM Student WHERE student_name = '';

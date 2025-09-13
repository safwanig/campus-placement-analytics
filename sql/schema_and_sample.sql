-- Schema for placement_db
CREATE DATABASE IF NOT EXISTS placement_db;
USE placement_db;

-- branches
CREATE TABLE IF NOT EXISTS branch (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

-- companies
CREATE TABLE IF NOT EXISTS company (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL
);

-- students
CREATE TABLE IF NOT EXISTS student (
  id INT AUTO_INCREMENT PRIMARY KEY,
  roll_no VARCHAR(20) UNIQUE,
  name VARCHAR(150),
  branch_id INT,
  cgpa DECIMAL(3,2),
  batch_year INT,
  FOREIGN KEY (branch_id) REFERENCES branch(id)
);

-- placements
CREATE TABLE IF NOT EXISTS placement (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT,
  company_id INT,
  package_lpa DECIMAL(6,2),
  role VARCHAR(150),
  offer_date DATE,
  CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES student(id),
  CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES company(id)
);

-- Sample data (small)
INSERT INTO branch (name) VALUES ('CSE'), ('ECE'), ('ME'), ('CE');

INSERT INTO company (name) VALUES ('Infosys'), ('TCS'), ('Amazon'), ('Google'), ('Accenture'), ('Flipkart');

INSERT INTO student (roll_no, name, branch_id, cgpa, batch_year) VALUES
('NITD001','Aman Kumar',1,8.20,2025),
('NITD002','Riya Sharma',2,7.60,2025),
('NITD003','Rahul Das',1,7.90,2025),
('NITD004','Pooja Singh',3,8.50,2025),
('NITD005','Sahil Roy',1,6.80,2024);

INSERT INTO placement (student_id, company_id, package_lpa, role, offer_date) VALUES
(1,1,5.00,'Software Engineer','2025-06-10'),
(3,2,4.80,'Developer','2025-06-12'),
(4,5,6.50,'Analyst','2025-06-11'),
(2,6,10.00,'SDE','2025-06-15'),
(5,2,3.50,'Trainee','2024-05-21');

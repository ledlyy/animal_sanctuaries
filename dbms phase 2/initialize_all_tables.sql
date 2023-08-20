--CREATE DATABASE animal_sanctuaries;
--DELETE DATABASE IF EXISTS animal_sanctuaries;

-- creating departments table adding attrinute dept_id as primary key
CREATE TABLE departments (
  dept_id VARCHAR(10) PRIMARY KEY,
  dept_name VARCHAR(255) NOT NULL
);

-- creating locations table adding attrinute location_id as primary key
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    zip_code VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL
);

-- creating shelters table adding attrinute shelter_id as primary key, location_id as foreign key
CREATE TABLE shelters (
    shelter_id SERIAL PRIMARY KEY,
    capacity INT NOT NULL,
    location_id INT NOT NULL,
    shelter_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- creating users table
-- adding user_id as a primary key, email as unique, is_employee as not null
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    address VARCHAR(255),
    address2 VARCHAR(255),
    is_employee BOOLEAN DEFAULT FALSE NOT NULL
);

-- creating animals table
-- adding animal_id attribute as a primary key, shelter_id as foreign key

CREATE TABLE animals (
    animal_id SERIAL PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    color VARCHAR(50) ARRAY[5] DEFAULT '{}'::VARCHAR(50)[],
    age INT,
    species VARCHAR(50),
    breed VARCHAR(50),
    shelter_id INT,
    adoption_status BOOLEAN NOT NULL,
    vaccination_status BOOLEAN,
    microchip_id VARCHAR(50) UNIQUE,
    arrival_date DATE NOT NULL,
    FOREIGN KEY (shelter_id) REFERENCES shelters(shelter_id)
);
-- creating employees table
-- adding emp_id attribute as a primary key, dept_id as foreign key
CREATE TABLE employees (
    emp_id INT PRIMARY KEY REFERENCES users(user_id),
    dept_id VARCHAR(10) NOT NULL,
    job_title VARCHAR(255),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
-- creating salaries table
-- adding emp_id attribute as a foreign key
CREATE TABLE salaries (
    emp_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE DEFAULT '9999-01-01' NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- creating user_phones table
-- adding user_id attribute as a foreign key
CREATE TABLE user_phones (
    user_id INT NOT NULL,
    phone VARCHAR(30) NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- creating adopters table
-- adding adopter_id and animal_id attribute as a foreign key

CREATE TABLE adopters (
    adopter_id INT NOT NULL,
    animal_id INT NOT NULL,
    adoption_date DATE NOT NULL,
    occupation VARCHAR(255) NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (adopter_id) REFERENCES users(user_id)
);

-- creating donations table
-- adding donation_id as a primary key and user_id attribute as a foreign key
CREATE TABLE donations (
    donation_id SERIAL PRIMARY KEY,
    donation_date DATE NOT NULL,
    user_id INT NOT NULL,
    donation_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- creating adoptions_application table
-- adding application_id as a primary key and (animal_id, user_id) as a foreign key
CREATE TABLE adoptions_application (
    application_id SERIAL PRIMARY KEY,
    animal_id INT NOT NULL,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- creating care_records table
-- adding care_id as a primary key and (animal_id, emp_id) as a foreign key
CREATE TABLE care_records (
    care_id SERIAL PRIMARY KEY,
    health_status VARCHAR(255),
    animal_id INT NOT NULL,
    date DATE NOT NULL,
    emp_id INT NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- creating employment_history table
-- adding (emp_id, dept_id) as a foreign key
CREATE TABLE employment_history (
from_date DATE NOT NULL,
to_date DATE DEFAULT '9999-01-01' NOT NULL,
emp_id INT NOT NULL,
dept_id VARCHAR(10) NOT NULL,
FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
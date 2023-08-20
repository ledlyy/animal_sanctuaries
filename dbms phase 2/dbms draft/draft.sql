-- Create user table
CREATE TABLE "users" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    address VARCHAR(255),
    address2 VARCHAR(255),
    is_employee BOOLEAN DEFAULT FALSE
);

-- Create donation table
CREATE TABLE donations (
    donation_id SERIAL PRIMARY KEY,
    donation_date DATE,
    user_id INT,
    donati
    donation_amount DECIMAL(10, 2)
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create adoption_application table
CREATE TABLE adoptions_application (
    application_id SERIAL PRIMARY KEY,
    animal_id INT,
    user_id INT,
    date DATE,
    status DEFAULT 'pending',
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create adopter table
CREATE TABLE adopters (
    adopter_id INT,
    animal_id INT,
    adoption_date DATE,
    occupation VARCHAR(255),
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (adopter_id) REFERENCES users(user_id)
);

-- Create animal table
CREATE TABLE animals (
    animal_id SERIAL PRIMARY KEY,
    gender VARCHAR(10),
    color VARCHAR(50) ARRAY[5] DEFAULT '{}'::VARCHAR(50)[],
    age INT,
    adoption_date DATE DEFAULT '9999-01-01',
    type VARCHAR(50),
    shelter_id INT,
    FOREIGN KEY (shelter_id) REFERENCES shelters(shelter_id)
);


-- Create shelter table
CREATE TABLE shelters (
    shelter_id SERIAL PRIMARY KEY,
    capacity INT,
    location_id INT,
    shelter_name VARCHAR(255)
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Create location table
CREATE TABLE locations (
  location_id SERIAL PRIMARY KEY,
  zip_code VARCHAR(10),
  country VARCHAR(50),
  city VARCHAR(50),
  address VARCHAR(255)
);

-- Create care_record table
CREATE TABLE care_records (
    care_id SERIAL PRIMARY KEY,
    health_status VARCHAR(255),
    animal_id INT,
    date DATE,
    emp_id INT,
    cost DECIMAL(10, 2),
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);


-- Create employee table
CREATE TABLE employees (
    emp_id PRIMARY KEY REFERENCES users(user_id),
    dept_id INT,
    job_title VARCHAR(255),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);


-- Create employment_history table
CREATE TABLE employment_history (
  from_date DATE,
  to_date DATE,
  emp_id INT,
  dept_id INT,
  FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Create table departments
CREATE TABLE departments (
  dept_id INT PRIMARY KEY,
  dept_name VARCHAR(255)
);

-- Create table salaries
CREATE TABLE salaries (
  emp_id INT,
  from_date DATE,
  to_date DATE,
  salary NUMERIC(10, 2),
  FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- Create table user_phones
CREATE TABLE user_phones (
  user_id INT,
  phone VARCHAR(20),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
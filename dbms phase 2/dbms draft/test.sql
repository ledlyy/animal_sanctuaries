CREATE TABLE departments (
  dept_id VARCHAR(10) PRIMARY KEY,
  dept_name VARCHAR(255) NOT NULL
);

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    zip_code VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE shelters (
    shelter_id SERIAL PRIMARY KEY,
    capacity INT NOT NULL,
    location_id INT NOT NULL,
    shelter_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);


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

CREATE TABLE animals (
    animal_id SERIAL PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    color VARCHAR(50) ARRAY[5] DEFAULT '{}'::VARCHAR(50)[],
    age INT,
    --adoption_date DATE DEFAULT '9999-01-01' NOT NULL,
    species VARCHAR(50),
    breed VARCHAR(50),
    shelter_id INT,
    adoption_status BOOLEAN NOT NULL,
    vaccination_status BOOLEAN,
    microchip_id VARCHAR(50) UNIQUE,
    arrival_date DATE NOT NULL,
    FOREIGN KEY (shelter_id) REFERENCES shelters(shelter_id)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY REFERENCES users(user_id),
    dept_id VARCHAR(10) NOT NULL,
    job_title VARCHAR(255),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE salaries (
    emp_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE DEFAULT '9999-01-01' NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

CREATE TABLE user_phones (
    user_id INT NOT NULL,
    phone VARCHAR(30) NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE adopters (
    adopter_id INT NOT NULL,
    animal_id INT NOT NULL,
    adoption_date DATE NOT NULL,
    occupation VARCHAR(255) NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (adopter_id) REFERENCES users(user_id)
);
CREATE TABLE donations (
    donation_id SERIAL PRIMARY KEY,
    donation_date DATE NOT NULL,
    user_id INT NOT NULL,
    donation_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE adoptions_application (
    application_id SERIAL PRIMARY KEY,
    animal_id INT NOT NULL,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

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

CREATE TABLE employment_history (
from_date DATE NOT NULL,
to_date DATE DEFAULT '9999-01-01' NOT NULL,
emp_id INT NOT NULL,
dept_id VARCHAR(10) NOT NULL,
FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- deleting tables
DROP TABLE employment_history, care_records, adoptions_application, donations, adopters, user_phones, salaries, employees, animals, users, shelters, locations, departments;

/* 
Create tables without any foreign key dependencies first. These are typically the tables that serve as the base entities in your database schema. In your case, the following tables can be created first:

departments
locations
Next, create tables that have foreign key dependencies on the previously created tables. For example:

shelters (depends on locations)
users
animals (depends on shelters)
employees (depends on departments and users)
salaries (depends on employees)
user_phones (depends on users)
Finally, create tables that have dependencies on both previously created tables and tables yet to be created. For example:

adopters (depends on users and animals)
donations (depends on users)
adaptions_application (depends on animals and users)
care_records (depends on animals and employees)
employment_histories (depends on users and departments)
    Create care_record table
    This table is used to track the care history of each animal
*/
-- from_date = fake.date_between_dates(date_start=datetime.date(2010, 1, 1), date_end=datetime.date(2023, 1, 1)) 
-- to_date = fake.date_between_dates(date_start=from_date, date_end=datetime.date(2023, 1, 1)) if fake.random_int(min=1, max = 5) == 3 else datetime.date(9999, 1, 1)

/*
Department: 'ACW01' - Animal Care and Welfare

Animal Caretaker
Wildlife Rehabilitator
Animal Behaviorist
Department: 'ADR01' - Adoption and Rehoming

Adoption Counselor
Animal Placement Coordinator
Pet Adoption Specialist
Department: 'VET01' - Veterinary Services

Veterinarian
Veterinary Technician
Veterinary Receptionist
Department: 'AD01' - Administration

Office Administrator
Administrative Assistant
Operations Manager
Department: 'STF01' - Staff

Staff Coordinator
Staff Training Specialist
Staff Development Manager
Department: 'HR01' - Human Resources

Human Resources Manager
HR Generalist
Recruitment Specialist
Department: 'IT01' - Information Technology

IT Support Specialist
Systems Administrator
Software Developer
Department: 'FIN01' - Finance

Financial Analyst
Accounting Manager
Payroll Specialist
Department: 'VOL01' - Volunteers

Volunteer Coordinator
Volunteer Engagement Specialist
Volunteer Program Manager
Department: 'SEC01' - Security

Security Officer
Security Supervisor
Security Operations Manager
*/
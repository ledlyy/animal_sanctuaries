const express = require('express');
const { Pool } = require('pg');
const path = require('path');
const bodyParser = require('body-parser');
const session = require('express-session');
const flash = require('express-flash');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'animal_sanctuaries',
  password: 'postgres',
  port: 5433, // Default PostgreSQL port
});

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'publi c'))); // Serve static files from the 'public' directory

app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true,
}));
app.use(flash());

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Login page route
app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { email, password } = req.body;

  pool.query('SELECT * FROM users WHERE email = $1', [email], (error, result) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      if (result.rows.length === 0) {
        res.sendStatus(401); // User not found
      } else {
        const user = result.rows[0];
        const userID = user.user_id;

        if (user.password === password) {
          if (user.is_employee) {
            // Store the user_id in the session
            req.session.userID = userID;

            // Redirect to employee page
            res.redirect('/employee');
          } else {
            // Store the user_id in the session
            req.session.userID = userID;

            // Redirect to user page
            res.redirect('/home');
          }
        } else {
          res.sendStatus(401); // Incorrect password
        }
      }
    }
  });
});

// home.ejs route
app.get('/home', (req, res) => {
  const userID = req.session.userID; // Retrieve the User ID from the session

  // Retrieve the user details based on the userID
  pool.query('SELECT * FROM users WHERE user_id = $1', [userID], (error, result) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      const user = result.rows[0]; // Retrieve the user details

      // Retrieve the animal details
      pool.query('SELECT * FROM animals WHERE adoption_status = false ORDER BY animal_id DESC', (error, result) => {
        if (error) {
          console.error('Error executing query', error);
          res.sendStatus(500);
        } else {
          const animals = result.rows;
          res.render('home', { user, animals }); // Render the home page with user and animals data
        }
      });
    }
  });
});

app.get('/add-animal', (req, res) => {
  res.render('add-animal.ejs');
});



app.post('/add-animal', (req, res) => {
  const { species, breed, age, shelter_id, vaccination_status, microchip_id, gender } = req.body;
  const current_date = formatDate(new Date());

  pool.query(
    'INSERT INTO animals (species, breed, age, shelter_id, vaccination_status, microchip_id, arrival_date, gender, adoption_status) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
    [species, breed, age, shelter_id, vaccination_status, microchip_id, current_date, gender, false],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        res.redirect('/employee'); // Redirect to the login page
      }
    }
  );
});











app.get('/register', (req, res) => {
  res.render('register');
});

// Registration route
app.post('/register', (req, res) => {
  const { email, first_name, last_name, password, gender, address, address2 } = req.body;

  pool.query(
    'INSERT INTO users (email, first_name, last_name, password, gender, address, address2) VALUES ($1, $2, $3, $4, $5, $6, $7)',
    [email, first_name, last_name, password, gender, address, address2],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        res.redirect('/login'); // Redirect to the login page
      }
    }
  );
});



app.post('/donate', (req, res) => {
  const { amount } = req.body;
  const userId = req.session.userID; // Retrieve the User ID from the session
  const donation_date = formatDate(new Date());
  pool.query(
    'INSERT INTO donations (donation_date, user_id, donation_amount) VALUES ($1, $2, $3)',
    [donation_date, userId, amount],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        req.flash('successMessage', 'Donation made successfully!');
        res.redirect('/home');
      }
    }
  );
});



app.post('/update-information', (req, res) => {
  // Extract the form data from the request body
  const userId = req.session.userID; // Retrieve the User ID from the session
  const { first_name, last_name, password, address, address2, phone } = req.body;

  // Perform any necessary validation or processing of the form data
  // ...
  pool.query(
    'UPDATE users SET first_name = $1, last_name = $2, password = $3, address = $4, address2 = $5 WHERE user_id = $6',
    [first_name, last_name, password, address, address2, userId],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        pool.query('INSERT INTO user_phones (user_id, phone) VALUES ($1, $2)', [userId, phone], (error) => {
          if (error) {
            console.error('Error executing query', error);
            res.sendStatus(500);
          } else {
            req.flash('successMessage', 'User information updated successfully!');
            res.redirect('/user');
          }
        });
      }
    }
  );
});




// Adoption application route
app.post('/adoption', (req, res) => {
  const { animalId, userId, date, status } = req.body;

  pool.query(
    'INSERT INTO adoptions_application (animal_id, user_id, date, status) VALUES ($1, $2, $3, $4)',
    [animalId, userId, date, status],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        res.sendStatus(201); // Successful adoption application
      }
    }
  );
});

app.post('/join-us', (req, res) => {
  const { user_id, first_name, last_name, email, gender, address, phone, motivation_letter, position } = req.body;

  pool.query('INSERT INTO join_us (user_id, first_name, last_name, email, gender, address, phone, motivation_letter, position) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
    [user_id, first_name, last_name, email, gender, address, phone, motivation_letter, position],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        res.redirect('/user'); // Redirect to the login page
      }
    }
  );
});



// Get animal shelters

// Get animal details
app.get('/animals', (req, res) => {

  pool.query('SELECT * FROM animals WHERE adoption_status = false LIMIT 100', (error, result) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      const animals = result.rows;
      res.render('home.ejs', { animals }); // Render the animals page using a template engine
    }
  });
});



app.get('/animals/:id', async (req, res) => {
  const animalId = req.params.id;

  try {
    const animalQuery = 'SELECT * FROM animals WHERE animal_id = $1';
    const animalResult = await pool.query(animalQuery, [animalId]);
    const animal = animalResult.rows[0];
    shelterID = animal.shelter_id;
    const sheltersQuery = 'SELECT * FROM shelters WHERE shelter_id = $1';
    const sheltersResult = await pool.query(sheltersQuery, [shelterID]);
    const shelters = sheltersResult.rows[0];
    locationID = shelters.location_id;
    const locationQuery = 'SELECT * FROM locations WHERE location_id = $1';
    const locationsResult = await pool.query(locationQuery, [locationID]);
    const locations = locationsResult.rows[0];
    const care_stuffQuery = "SELECT * FROM employees WHERE dept_id IN ('ACW01', 'VET01', 'ADR01');";
    const care_stuffResult = await pool.query(care_stuffQuery);
    const care_stuff = care_stuffResult.rows;
    const adoptionQuery = 'SELECT * FROM adoptions_application WHERE animal_id = $1';
    const adoptionResult = await pool.query(adoptionQuery, [animalId]);
    const adoption_applications = adoptionResult.rows;
    const careRecordsQuery = 'SELECT * FROM care_records WHERE animal_id = $1 ORDER BY date DESC';
    const careRecordsResult = await pool.query(careRecordsQuery, [animalId]);
    const care_records = careRecordsResult.rows;



    res.render('animal', { animal, locations, shelters, care_stuff, adoption_applications, care_records });


    //res.render('animal', { animal, locations, shelters, care_stuff,adoption_applications, care_records, join_us });
  } catch (error) {
    console.error('Error retrieving data from the database:', error);
    res.status(500).send('Internal Server Error');
  }
});

app.post('/update-shelter-location', (req, res) => {
  const { shelter_id, animal_id } = req.body;
  pool.query(
    'UPDATE animals SET shelter_id = $1 WHERE animal_id = $2',
    [shelter_id, animal_id],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        req.flash('successMessage', 'Shelter location updated successfully!');
        res.redirect(`/animals/${animal_id}`);
      }
    }
  );
});

app.post('/update-vaccination-status', (req, res) => {
  const { vaccinationStatus, animal_id } = req.body;
  pool.query(
    'UPDATE animals SET vaccination_status = $1 WHERE animal_id = $2',
    [vaccinationStatus, animal_id],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        req.flash('successMessage', 'Vaccination status updated successfully!');
        res.redirect(`/animals/${animal_id}`);
      }
    }
  );
});

app.post('/create-care-records', (req, res) => {
  const { animalID, empID, date, healthStatus, cost } = req.body;

  pool.query(
    'INSERT INTO care_records (health_status,animal_id, date, emp_id, cost) VALUES ($1, $2, $3, $4, $5)',
    [healthStatus, animalID, date, empID, cost],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        req.flash('successMessage', 'Care record created successfully!');
        res.redirect(`/animals/${animalID}`);
      }
    }
  );
});

app.get('/see-animal', (req, res) => {
  const { animal_id } = req.query;
  res.redirect(`/animals/${animal_id}`);
});


app.get('/user', (req, res) => {
  const userId = req.session.userID;
  pool.query('SELECT * FROM users WHERE user_id = $1', [userId], (error, userResult) => {
    if (error) {
      console.error('Error executing user query', error);
      res.sendStatus(500);
    } else {
      const user = userResult.rows[0];
      pool.query('SELECT * FROM adoptions_application WHERE user_id = $1', [userId], (error, applicationResult) => {
        if (error) {
          console.error('Error executing adoption applications query', error);
          res.sendStatus(500);
        } else {
          const applications = applicationResult.rows;
          pool.query('SELECT * FROM donations WHERE user_id = $1', [userId], (error, donationResult) => {
            if (error) {
              console.error('Error executing donations query', error);
              res.sendStatus(500);
            } else {
              const donations = donationResult.rows;
              pool.query('SELECT * FROM user_phones WHERE user_id = $1', [userId], (error, phoneResult) => {
                if (error) {
                  console.error('Error executing user phones query', error);
                  res.sendStatus(500);
                } else {
                  const userPhones = phoneResult.rows;
                  res.render('user.ejs', { user, applications, donations, userPhones });
                }
              });
            }
          });
        }
      });
    }
  });
});


app.post('/cancel-application', (req, res) => {
  const { application_id } = req.body;
  pool.query('DELETE FROM adoptions_application WHERE application_id = $1', [application_id], (error) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      res.redirect('/user');
    }
  });
});

app.post('/evaluate-employee', (req, res) => {
  const { user_id, application_id, position, status } = req.body;

  pool.query('UPDATE join_us SET status = $1 WHERE id = $2', [status, application_id], (error) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      if (status === 'approved') {
        pool.query('UPDATE users SET is_employee = $1 WHERE user_id = $2', [true, user_id], (error) => {
          if (error) {
            console.error('Error executing query', error);
            res.sendStatus(500);
          } else {
            pool.query('INSERT INTO employees (emp_id, dept_id, job_title) VALUES ($1, $2, $3)', [user_id, position, "junior"], (error) => {
              if (error) {
                console.error('Error executing query', error);
                res.sendStatus(500);
              } else {
                res.redirect('/employee');
              }
            });
          }
        });
      } else {
        res.redirect('/employee');
      }
    }
  });
});


app.get('/index', (req, res) => {
  const path = require('path');
  const indexPath = path.join(__dirname, 'views/index.html');
  res.sendFile(indexPath);
});



app.get('/employee', async (req, res) => {
  const userId = req.session.userID;
  let count_list = [];

  try {
    let careRecordsQuery = 'SELECT * FROM care_records';
    let adoptionApplicationsQuery = 'SELECT * FROM adoptions_application WHERE status = $1';
    let queryParams = ['pending'];
    let employeesQuery = 'SELECT * FROM employees';
    let salariesQuery = 'SELECT * FROM salaries';
    let current_userQuery = 'SELECT * FROM users WHERE user_id = $1';
    let current_employeeQuery = 'SELECT * FROM employees WHERE emp_id = $1';
    let getlastSalary = 'SELECT * FROM salaries WHERE emp_id = $1 ORDER BY to_date DESC LIMIT 1';


    const careRecordsResult = await pool.query(careRecordsQuery);
    const adoptionApplicationsResult = await pool.query(adoptionApplicationsQuery, queryParams);
    const employeesResult = await pool.query(employeesQuery);
    const salariesResult = await pool.query(salariesQuery);
    const current_user_result = await pool.query(current_userQuery, [userId]);
    const current_employee_result = await pool.query(current_employeeQuery, [userId]);
    const lastSalary = await pool.query(getlastSalary, [userId]);

    const careRecords = careRecordsResult.rows;
    const adoptionApplications = adoptionApplicationsResult.rows;
    const employees = employeesResult.rows;
    const salaries = salariesResult.rows;
    const current_user = current_user_result.rows[0];
    const current_employee = current_employee_result.rows[0];
    const last_salary = lastSalary.rows[0];
    const join_usQuery = 'SELECT * FROM join_us';
    const join_usResult = await pool.query(join_usQuery);
    const join_us = join_usResult.rows;

    const countDistinctEmployees = await pool.query('SELECT COUNT(DISTINCT emp_id) AS count FROM employees');
    const countDistinctAdopters = await pool.query('SELECT COUNT(DISTINCT adopter_id) AS count FROM adopters');
    const countDistinctAnimals = await pool.query('SELECT COUNT(DISTINCT animal_id) AS count FROM animals');
    const countDistinctDonors = await pool.query('SELECT COUNT(DISTINCT donation_id) AS count FROM donations');
    const countTotalDonations = await pool.query('SELECT SUM(donation_amount) AS count FROM donations');
    const countTotalAdoptions = await pool.query('SELECT COUNT(*) AS count FROM adoptions_application');
    const countTotalEmployeeSalaries = await pool.query('SELECT SUM(salary) AS count FROM salaries');
    const countDistinctUsers = await pool.query('SELECT COUNT(DISTINCT user_id) AS count FROM users');
    const countNumberofAdoptions = await pool.query('SELECT COUNT(*) AS count FROM adoptions_application');
    const countNumberDonations = await pool.query('SELECT COUNT(*) AS count FROM donations');
    const countCostOfCare = await pool.query('SELECT SUM(cost) AS count FROM care_records');


    const countDistinctEmployeesResult = countDistinctEmployees.rows[0];
    const countDistinctAdoptersResult = countDistinctAdopters.rows[0];
    const countDistinctAnimalsResult = countDistinctAnimals.rows[0];
    const countDistinctDonorsResult = countDistinctDonors.rows[0];
    const countTotalDonationsResult = countTotalDonations.rows[0];
    const countTotalAdoptionsResult = countTotalAdoptions.rows[0];
    const countTotalEmployeeSalariesResult = countTotalEmployeeSalaries.rows[0];
    const countDistinctUsersResult = countDistinctUsers.rows[0];
    const countNumberofAdoptionsResult = countNumberofAdoptions.rows[0];
    const countNumberDonationsResult = countNumberDonations.rows[0];
    const countCostOfCareResult = countCostOfCare.rows[0];

    count_list[0] = countDistinctUsersResult;
    count_list[1] = countDistinctEmployeesResult;
    count_list[2] = countNumberDonationsResult;
    count_list[3] = countDistinctAdoptersResult;
    count_list[4] = countDistinctAnimalsResult;
    count_list[5] = countDistinctDonorsResult;
    count_list[6] = countTotalDonationsResult;
    count_list[7] = countCostOfCareResult;




    res.render('employee.ejs', { careRecords, adoptionApplications, employees, salaries, current_user, current_employee, last_salary, join_us, count_list });
  } catch (error) {
    console.error('Error retrieving data from the database:', error);
    res.status(500).send('Internal Server Error');
  }
});

app.post('/update-adoption', (req, res) => {
  const { user_id, application_id, status, animal_id } = req.body;
  pool.query('UPDATE adoptions_application SET status = $1 WHERE application_id = $2', [status, application_id], (error) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      if (status == 'approved') {
        const adoptionDate = formatDate(new Date());
        const occupation = 'unknown'; // Replace with the actual occupation value from the form or user input
        pool.query(
          'INSERT INTO adopters (adopter_id, animal_id, adoption_date, occupation) VALUES ($1, $2, $3, $4)',
          [user_id, animal_id, adoptionDate, occupation],
          (error) => {
            if (error) {
              console.error('Error executing query', error);
              res.sendStatus(500);
            } else {
              res.redirect('/employee');
            }
          }
        );
      }
      else {
        res.redirect('/employee');
      }
    }
  });
});









app.get('/application', (req, res) => {
  const animalId = req.query.animalId; // Get the animalId from the query parameter
  const userId = req.session.userID; // Retrieve the User ID from the session
  const currentDate = formatDate(new Date());

  // Retrieve the user details based on the userId
  pool.query('SELECT * FROM users WHERE user_id = $1', [userId], (error, result) => {
    if (error) {
      console.error('Error executing query', error);
      res.sendStatus(500);
    } else {
      const user = result.rows[0]; // Retrieve the user details
      // Retrieve the animal details based on the animalId
      pool.query('SELECT * FROM animals WHERE animal_id = $1', [animalId], (error, result) => {
        if (error) {
          console.error('Error executing query', error);
          res.sendStatus(500);
        } else {
          const animal = result.rows[0];
          res.render('application', { animal, user, currentDate }); // Render the adoption application page with the animal details, user details, and current date
        }
      });
    }
  });
});

// Submit adoption application
app.post('/application', (req, res) => {
  const { animalId, date, status } = req.body;
  const userId = req.session.userID; // Retrieve the User ID from the session

  pool.query(
    'INSERT INTO adoptions_application (animal_id, user_id, date) VALUES ($1, $2, $3)',
    [animalId, userId, date],
    (error) => {
      if (error) {
        console.error('Error executing query', error);
        res.sendStatus(500);
      } else {
        req.session.successMessage = 'Adoption application submitted successfully!';
        res.redirect('/home');
      }
    }
  );
});

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

app.get('/logout', (req, res) => {
  // Destroy the session to log out the user
  req.session.destroy((error) => {
    if (error) {
      console.error('Error destroying session', error);
      res.sendStatus(500);
    } else {
      // Redirect the user to the login page after logging out
      res.redirect('/login');
    }
  });
});

app.get("/", function (req, res) {
  res.render("login");
});




const PORT = process.env.PORT || 3000; // Use environment variable or port 3000 as default
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});


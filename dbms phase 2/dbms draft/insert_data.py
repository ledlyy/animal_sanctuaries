import datetime
import psycopg2
from faker import Faker
import psycopg2.extensions


fake = Faker()



def get_element_by_column_where(cursor, table_name, column, where):
    query = f"SELECT {column} FROM {table_name} WHERE {where};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
    

def get_count_by_column_distinct(cursor, table_name, column):
    query = f"SELECT COUNT(DISTINCT {column}) FROM {table_name};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

def get_count_distinct(cursor, table_name):
    query = f"SELECT COUNT(DISTINCT *) FROM {table_name};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
def get_count_by_column_where(cursor, table_name, column, where):
    query = f"SELECT COUNT({column}) FROM {table_name} WHERE {where};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
def get_count_where(cursor, table_name, where):
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {where};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
      
def get_count_by_column(cursor, table_name, column):
    query = f"SELECT COUNT({column}) FROM {table_name};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
def get_count(cursor, table_name): 
    query = f"SELECT COUNT(*) FROM {table_name};"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
def get_list(cursor, table, column):
    query = f"SELECT {column} FROM {table};"
    cursor.execute(query)
    result = cursor.fetchall()
    query_list = []
    for i in result:
        query_list.append(i[0])
    return query_list
def get_list_where(cursor, table, column, where):
    query = f"SELECT {column} FROM {table} WHERE {where};"
    cursor.execute(query)
    result = cursor.fetchall()
    query_list = []
    for i in result:
        query_list.append(i[0])
    return query_list
def insert_departments(cursor):
    departments = [
        ('ACW01', 'Animal Care and Welfare'),
        ('ADR01', 'Adoption and Rehoming'),
        ('VET01', 'Veterinary Services'),
        ('AD01', 'Administration'),
        ('STF01', 'Staff'),
        ('HR01', 'Human Resources'),
        ('IT01', 'Information Technology'),
        ('FIN01', 'Finance'),
        ('VOL01', 'Volunteers'),
        ('SEC01', 'Security') 
    ]

    try:
        for department in departments:
            insert_query = "INSERT INTO departments (dept_id, dept_name) VALUES (%s, %s);"
            cursor.execute(insert_query, department)

        print("Departments inserted successfully!")

    except Exception as e:
        print("Error inserting departments:", e)

def insert_locations(cursor):
    locations = [
        ('34000', 'Turkey', 'Istanbul', '123 Street, Kadıköy'),
        ('06000', 'Turkey', 'Ankara', '456 Street, Çankaya'),
        ('01000', 'Turkey', 'Eskişehir', '789 Street, Odunpazarı'),
    ]
    
    try:
        for location in locations:
            insert_query = "INSERT INTO locations (zip_code, country, city, address) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query, location)

        print("Locations inserted successfully!")
    
    except Exception as e:
        print("Error inserting locations:", e)
 
def insert_shelters(cursor):
    
    shelters = [
        (1000, 3, 'Shelter 1'),
        (2000, 1, 'Shelter 2'),
        (2000, 2, 'Shelter 3'),
    ]
    try:
        
        for shelter in shelters:
            insert_query = "INSERT INTO shelters (capacity, location_id, shelter_name) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, shelter)
            
        print("Shelters inserted successfully!")
        
    except Exception as e:
        print("Error inserting shelters:", e)
   
        
def insert_users(cursor):
    
    email_list = []
    try:
        for _ in range(5000):
            email = fake.email()
            while email in email_list:
                email = fake.email()
    
            email_list.append(email)
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password()
            gender = fake.random_element(elements=("Male", "Female"))
            address = fake.address()
            address2 = fake.random_element(elements=(None, fake.address()))
            print(f"Inserting user:, {email}")
            insert_query = """
                INSERT INTO "users" (email, first_name, last_name, password, gender, address, address2)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                 """
            cursor.execute(insert_query, (email, first_name, last_name, password, gender, address, address2))

        print("Users inserted successfully!")

    except Exception as e:
        print("Error inserting users:", e)

def insert_animals(cursor):
    dog_types = ["Golden Retriever", "Labrador Retriever", "German Shepherd", "Bulldog", "Poodle", "Beagle", "Boxer", "Rottweiler", "Dachshund", "Chihuahua", "Siberian Husky","Great Dane", "Doberman Pinscher", "Shih Tzu", "Boston Terrier", "Pomeranian","Yorkshire Terrier", "French Bulldog", "Corgi", "Australian Shepherd","Border Collie", "Cocker Spaniel", "Pug", "Basset Hound", "Malamute", "Saint Bernard", "Shiba Inu", "Australian Cattle Dog", "Papillon", "Bichon Frise"]
    cat_types = ["Siamese", "Persian", "Maine Coon", "Ragdoll", "Bengal", "Sphynx","British Shorthair", "Scottish Fold", "Russian Blue", "Abyssinian", "Burmese","Norwegian Forest", "Exotic Shorthair", "Devon Rex", "Oriental", "Siberian","Himalayan", "Tonkinese", "Cornish Rex", "American Shorthair", "Turkish Angora","Birman", "Manx", "Bombay", "Chartreux", "Somali", "Balinese", "Pixiebob","Savannah", "Toyger" ]
    pet_species = ["Dog", "Cat", "Rabbit", "Guinea Pig", "Hamster", "Bird", "Ferret", "Snake", "Turtle", "Lizard", "Fish", "Parrot", "Horse", "Goat", "Sheep", "Pig", "Alpaca", "Chicken", "Duck", "Gerbil", "Chinchilla", "Hedgehog", "Rat", "Mouse", "Fancy Rat", "Rabbit", "Budgerigar", "Cockatiel", "Finch", "Guppy", "Betta Fish"]
    microchip_list = []
    animal_colors = {
        "Dog": {
            "Golden Retriever": ["Golden"],
            "Labrador Retriever": ["Yellow", "Black", "Chocolate"],
            "German Shepherd": ["Black", "Tan", "Sable"],
            "Bulldog": ["White", "Fawn", "Brindle"],
            "Poodle": ["White", "Black", "Apricot", "Brown"],
            "Beagle": ["Tri-color", "White and Tan"],
            "Boxer": ["Fawn", "Brindle"],
            "Rottweiler": ["Black", "Tan"],
            "Dachshund": ["Red", "Black", "Tan"],
            "Chihuahua": ["Black", "Tan", "Fawn", "White"],
            "Siberian Husky": ["Black", "White", "Gray", "Red"],
            "Great Dane": ["Black", "Fawn", "Brindle", "Harlequin"],
            "Doberman Pinscher": ["Black", "Red", "Blue", "Fawn"],
            "Shih Tzu": ["Black", "White", "Brown", "Gold"],
            "Boston Terrier": ["Black", "Brindle", "Seal"],
            "Pomeranian": ["Orange", "Red", "White", "Black"],
            "Yorkshire Terrier": ["Black", "Tan"],
            "French Bulldog": ["Brindle", "Fawn", "White"],
            "Corgi": ["Red", "Sable", "Fawn", "Black and Tan"],
            "Australian Shepherd": ["Black", "Blue", "Red", "Red Merle", "Blue Merle"],
            "Border Collie": ["Black", "White", "Blue Merle", "Red Merle"],
            "Cocker Spaniel": ["Black", "Tan", "Brown", "White"],
            "Pug": ["Fawn", "Black"],
            "Basset Hound": ["Tri-color", "Tan and White"],
            "Malamute": ["Black", "White", "Gray"],
            "Saint Bernard": ["Red", "White", "Red and White"],
            "Shiba Inu": ["Red", "Black and Tan", "White"],
            "Australian Cattle Dog": ["Blue", "Red", "Blue Speckled", "Red Speckled"],
            "Papillon": ["White", "Black and White", "Sable and White", "Red and White"],
            "Bichon Frise": ["White"]
        },
        "Cat": {
            "Siamese": ["Seal Point", "Chocolate Point", "Blue Point", "Lilac Point"],
            "Persian": ["White", "Black", "Blue", "Red", "Cream", "Chocolate",],
            "Maine Coon": ["Brown Tabby", "Black", "Red", "Cream", "Silver"],
            "Ragdoll": ["Seal Point", "Blue Point", "Chocolate Point", "Lilac Point"],
            "Bengal": ["Spotted", "Marbled"],
            "Sphynx": ["White", "Black", "Blue", "Pink"],
            "British Shorthair": ["Blue", "Black", "White", "Cream", "Silver"],
            "Scottish Fold": ["White", "Black", "Blue", "Cream", "Tabby"],
            "Russian Blue": ["Blue"],
            "Abyssinian": ["Ruddy", "Red", "Blue", "Fawn"],
            "Burmese": ["Sable", "Champagne", "Blue", "Platinum"],
            "Norwegian Forest": ["Brown Tabby", "Black", "Red", "Blue", "Cream"],
            "Exotic Shorthair": ["White", "Black", "Blue", "Cream", "Tabby"],
            "Devon Rex": ["White", "Black", "Blue", "Cream", "Tabby"],
            "Oriental": ["White", "Black", "Blue", "Cream", "Tabby"],
            "Siberian": ["Brown Tabby", "Black", "Red", "Blue", "Cream"],
            "Himalayan": ["Seal Point", "Blue Point", "Chocolate Point", "Lilac Point"],
            "Tonkinese": ["Natural", "Mink", "Solid"],
            "Cornish Rex": ["White", "Black", "Blue", "Cream", "Tabby"],
            "American Shorthair": ["Brown Tabby", "Black", "Silver Tabby"],
            "Turkish Angora": ["White"],
            "Birman": ["Seal Point", "Blue Point", "Chocolate Point", "Lilac Point"],
            "Manx": ["Rumpy", "Riser", "Stumpy"],
            "Bombay": ["Black"],
            "Chartreux": ["Blue"],
            "Somali": ["Ruddy", "Red", "Blue", "Fawn"],
            "Balinese": ["Seal Point", "Blue Point", "Chocolate Point", "Lilac Point"],
            "Pixiebob": ["Brown Tabby", "Black", "Red", "Blue", "Cream"] 
        },
        "Other": {
        "Rabbit": ["White", "Brown", "Black", "Gray"],
        "Guinea Pig": ["White", "Black", "Brown", "Tan"],
        "Hamster": ["Golden", "White", "Brown", "Gray"],
        "Bird": ["Green", "Blue", "Red", "Yellow"],
        "Ferret": ["Sable", "White", "Black"],
        "Snake": ["Green", "Brown", "Black", "Yellow"],
        "Turtle": ["Green", "Brown", "Black"],
        "Lizard": ["Green", "Brown", "Black"],
        "Fish": ["Red", "Blue", "Yellow", "Orange"],
        "Parrot": ["Green", "Blue", "Red", "Yellow"],
        "Horse": ["Brown", "Black", "White", "Gray"],
        "Goat": ["Brown", "Black", "White", "Gray"],
        "Sheep": ["White", "Black", "Brown", "Gray"],
        "Pig": ["Pink", "Black", "Spotted"],
        "Alpaca": ["White", "Brown", "Black", "Gray"],
        "Chicken": ["White", "Brown", "Black"],
        "Duck": ["White", "Brown", "Black"],
        "Gerbil": ["Gray", "Brown", "Black", "White"],
        "Chinchilla": ["Gray", "Brown", "Black", "White"],
        "Hedgehog": ["Brown", "Gray", "White"],
        "Rat": ["White", "Brown", "Black", "Gray"],
        "Mouse": ["White", "Brown", "Black", "Gray"],
        "Fancy Rat": ["White", "Brown", "Black", "Gray"],
        "Budgerigar": ["Blue", "Green", "Yellow"],
        "Cockatiel": ["Gray", "White", "Yellow"],
        "Finch": ["Yellow", "Red", "Black", "White"],
        "Guppy": ["Red", "Blue", "Yellow", "Orange"],
        "Betta Fish": ["Red", "Blue", "Black", "White"]
        }
    }         
    try:
        for _ in range(5000):
            gender = fake.random_element(elements=("Male", "Female"))
            animal_type = fake.random_element(elements=(pet_species + ["Cat", "Dog"] * 30));
            if animal_type == "Dog":
                animal_breed = fake.random_element(elements=dog_types)
                colors = animal_colors.get(animal_type, {}).get(animal_breed, [])
            elif animal_type == "Cat":
                animal_breed = fake.random_element(elements=cat_types)
                colors = animal_colors.get(animal_type, {}).get(animal_breed, [])
            else:
                animal_breed = None
                colors = animal_colors.get("Other", {}).get(animal_type, [])
        
        
            if colors:
                sample_length = min(fake.random_int(min=1, max=5), len(colors))
                colors = fake.random_elements(elements=colors, length=sample_length, unique=True)
                
                
            age = fake.random_int(min=1, max=10)
            shelter_id = fake.random_int(min=1, max=3)
            shelter_capacity = get_element_by_column_where(cursor,"shelters", "capacity",f"shelter_id = {shelter_id}")
            current_shelter_capacity = get_count_where(cursor,"animals", f"shelter_id = {shelter_id}")
            while current_shelter_capacity >= shelter_capacity:
                shelter_id = fake.random_int(min=1, max=3)
                shelter_capacity = get_element_by_column_where(cursor,"shelters", "capacity",f"shelter_id = {shelter_id}")
                current_shelter_capacity = get_count_where(cursor,"animals", f"shelter_id = {shelter_id}")
            
            adoption_status = fake.random_element(elements=(True, False))
            arrival_date = fake.date_between_dates(date_start=datetime.date(2010,1,1), date_end=datetime.date(2023, 1, 1))
               
                
            if adoption_status == True:
                vaccination_status = True
            else:
                vaccination_status = fake.random_element(elements=(True, False))
                   
            microchip_id = fake.unique.random_number(digits=9, fix_len=True)
            while microchip_id in microchip_list:
                microchip_id = fake.unique.random_number(digits=9, fix_len=True)
            microchip_list.append(microchip_id)
            print("inserting animal")
            insert_query = """
                INSERT INTO animals(gender, color, age, species, breed, shelter_id,  adoption_status, vaccination_status, microchip_id, arrival_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
            cursor.execute(insert_query, (gender, colors, age, animal_type, animal_breed, shelter_id, adoption_status, vaccination_status, microchip_id, arrival_date))
        print("Successfully inserted animals")                               
    
    except Exception as e:
        print("Error inserting animals:", e)

def insert_employees(cursor):
    number_of_employees = 300
    employees_list = []
    users_list = get_list(cursor, "users", "user_id")
    dept_id_list = get_list(cursor, "departments", "dept_id")
    title_list = {'ACW01':('Animal Caretaker', 'Wildlife Rehabilitator', 'Animal Behaviorist'),
                  'ADR01':('Adoption Counselor', 'Animal Placement Coordinator', 'Pet Adoption Specialist'),
                  'VET01':('Veterinarian', 'Veterinary Technician', 'Veterinary Receptionist'),
                  'AD01':('Office Administrator', 'Administrative Assistant', 'Operations Manager'),
                  'STF01':('Staff Coordinator', 'Staff Training Specialist', 'Staff Development Manager'),
                  'HR01':('Human Resources Manager', 'HR Generalist', 'Recruitment Specialist'),
                  'IT01':('IT Support Specialist', 'Systems Administrator', 'Software Developer'),
                  'FIN01':('Financial Analyst', 'Accounting Manager', 'Payroll Specialist'),
                  'VOL01':('Volunteer Coordinator', 'Volunteer Engagement Specialist', 'Volunteer Program Manager'),
                  'SEC01':('Security Officer', 'Security Supervisor')}    
        
    try:
        for i in range(number_of_employees):
            employee_id = fake.random_element(elements=users_list)
            while employee_id in employees_list:
                employee_id = fake.random_element(elements=users_list)
                
            employees_list.append(employee_id)
        
        
        for id in employees_list[:number_of_employees]:
            insert_query = "UPDATE users SET is_employee = True WHERE user_id = %s;"
            cursor.execute(insert_query, (id,))
            dept_id = fake.random_element(elements=dept_id_list)
            job_title = fake.random_element(elements=title_list.get(dept_id))
            selected_dept_id_count = get_count_where(cursor, "employees", f"dept_id = '{dept_id}'")
            selected_job_title_count = get_count_where(cursor, "employees", f"job_title = '{job_title}'")
            while selected_dept_id_count > (number_of_employees/len(dept_id_list)) or selected_job_title_count > (number_of_employees/(len(dept_id_list)*len(title_list.get(dept_id)))):
                dept_id = fake.random_element(elements=dept_id_list)
                job_title = fake.random_element(elements=title_list.get(dept_id))
                selected_dept_id_count = get_count_where(cursor, "employees", f"dept_id = '{dept_id}'")
                selected_job_title_count = get_count_where(cursor, "employees", f"job_title = '{job_title}'")   
                
            insert_query = "INSERT INTO employees(emp_id, dept_id, job_title) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (id, dept_id, job_title))
            
        print("Inserting employees...")
        
    except Exception as e:
        print("Error inserting employees:", e)


def insert_salaries(cursor):
    emloyees_list = get_list(cursor, "employees", "emp_id")
    try:
        for id in emloyees_list:
            salary_change_count = fake.random_int(min=1, max=4)
            for i in range(salary_change_count):
                salary = fake.random_int(min=30000, max=120000)
                if i == 0:
                    from_date = fake.date_between_dates(date_start=datetime.date(2010, 1, 1), date_end=datetime.date(2023, 1, 1))
                else:
                    biggest_last_date = get_element_by_column_where(cursor, "salaries", "to_date", f"emp_id = '{id}' ORDER BY to_date DESC LIMIT 1")
                    from_date = datetime.datetime.strptime(str(biggest_last_date), "%Y-%m-%d").date()
                if(i != (salary_change_count-1)):
                    to_date = fake.date_between_dates(date_start=from_date, date_end=datetime.date(2023, 1, 1))
                else:
                    to_date = datetime.date(9999, 1, 1)
                insert_query = "INSERT INTO salaries(emp_id, from_date, to_date, salary) VALUES (%s, %s, %s, %s);"
                cursor.execute(insert_query, (id, from_date, to_date, salary))
        
        print("Inserted salaries")
    except Exception as e:
        print("Error inserting salaries:", e)      
def insert_user_phones(cursor):
    users_list = get_list(cursor, "users", "user_id")
    phone_list = get_list(cursor, "user_phones", "phone")
    try:
        for id in users_list:
            phone_number_count = fake.random_int(min=1, max=2)
            for i in range(phone_number_count):
                phone = fake.phone_number()
                while phone in phone_list:
                    phone = fake.phone_number()
                phone_list.append(phone)
                insert_query = "INSERT INTO user_phones(user_id, phone) VALUES (%s, %s);"
                cursor.execute(insert_query, (id, phone))
             
        print("Inserted user phones")
    except Exception as e:
        print("Error inserting user phones:", e)               

def insert_adopters(cursor):
    adopter_list = []
    user_list = get_list(cursor, "users", "user_id")
    unadopted_animals = get_list_where(cursor, "animals", "animal_id", "adoption_status = False")
    adaopted_animals = []
    try:
        for i in range(600):
            adopter_id = fake.random_element(elements=user_list)
            while adopter_id in adopter_list:
                adopter_id = fake.random_element(elements=user_list)
            adopter_list.append(adopter_id)
            animal_id = fake.random_element(elements=unadopted_animals)
            while animal_id in adaopted_animals:
                animal_id = fake.random_element(elements=unadopted_animals)
            adaopted_animals.append(animal_id)
            occupation = fake.job()
            animal_arrival_date = get_element_by_column_where(cursor, "animals", "arrival_date", f"animal_id = {animal_id}")
            adoption_date = fake.date_between_dates(date_start=animal_arrival_date, date_end=datetime.date(2023, 1, 1))
            insert_query = "INSERT INTO adopters(adopter_id, animal_id, occupation, adoption_date) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query, (adopter_id, animal_id, occupation, adoption_date))
            # make adoption status true
            update_query = "UPDATE animals SET adoption_status = True WHERE animal_id = %s;"
            cursor.execute(update_query, (animal_id,))
            
        
        print("Inserted adopters.")
    
    except Exception as e:
        print("Error inserting adopters:", e)

def insert_donations(cursor):
    donated_users = []
    users_list = get_list(cursor, "users", "user_id")
    try:
        for _ in range(400):
            user_id = fake.random_element(elements=users_list)
            while user_id in donated_users:
                user_id = fake.random_element(elements=users_list)
            donated_users.append(user_id)
            donation_count = fake.random_int(min=1, max=5)
            for _ in range(donation_count):
                print("inserting donations")
                donation_amount = fake.random_int(min=10, max=10000)
                insert_query = "INSERT INTO donations(user_id, donation_date, donation_amount) VALUES (%s, %s, %s);"
                donation_date = fake.date_between_dates(date_start=datetime.date(2010, 1, 1), date_end=datetime.date(2023, 1, 1))
                cursor.execute(insert_query, (user_id, donation_date, donation_amount))
    
        print("Inserted donations.")
    
    except Exception as e:
        print("Error inserting donations:", e)     

def insert_adoptions_application(cursor):
    users_list = get_list(cursor, "users", "user_id")
    # unadopted_animals = get_list_where(cursor, "animals", "animal_id", "adoption_status = False")
    users_applied_for_adoption = []
    application_status = ["pending", "approved", "rejected"]
    try:
        for _ in range(300):
            user_id = fake.random_element(elements=users_list)
            while user_id in users_applied_for_adoption:
                user_id = fake.random_element(elements=users_list)
            users_applied_for_adoption.append(user_id)
            adoption_count = fake.random_int(min=1, max=3)
            for _ in range(adoption_count):
               unadopted_animals = get_list_where(cursor, "animals", "animal_id", "adoption_status = False")
               animal_id = fake.random_element(elements=unadopted_animals)
               status = fake.random_element(elements=application_status)
               if status == "approved":
                     update_query = "UPDATE animals SET adoption_status = True WHERE animal_id = %s;"
                     cursor.execute(update_query, (animal_id,))
                     occupation = fake.job()
                     insert_query= "INSERT INTO adopters(adopter_id, animal_id, occupation, adoption_date) VALUES (%s, %s, %s, %s);"
                     cursor.execute(insert_query, (user_id, animal_id, occupation, datetime.date.today()))
               animal_arrival_date = get_element_by_column_where(cursor, "animals", "arrival_date", f"animal_id = {animal_id}")
               application_date = fake.date_between_dates(date_start=animal_arrival_date, date_end=datetime.date(2023, 1, 1))
               insert_query = "INSERT INTO adoptions_application(user_id, animal_id, date, status) VALUES (%s, %s, %s, %s);"
               cursor.execute(insert_query, (user_id, animal_id, application_date, status))
             
        print("Inserted adoptions applications.")
        
    except Exception as e:
        print("Error inserting adoptions applications:", e)

def insert_care_records(cursor):
    employees_list = get_list_where(cursor, "employees", "emp_id", "dept_id = 'VET01'")
    animals_list = get_list(cursor, "animals", "animal_id")
    health_status_list = ["Healthy", "Sick", "Injured", "Unknown"]
    try:
        for _ in range(1000):
            employee_id = fake.random_element(elements=employees_list)
            animal_id = fake.random_element(elements=animals_list)
            animal_arrival_date = get_element_by_column_where(cursor, "animals", "arrival_date", f"animal_id = {animal_id}")
            times = fake.random_int(min=1, max=4)
            for _ in range(times):
                #print("inserting care records")
                care_date = fake.date_between_dates(date_start=animal_arrival_date, date_end=datetime.date(2023, 1, 1))
                cost = fake.random_int(min=20, max=2000)
                health_status = fake.random_element(elements=health_status_list)
                insert_query = "INSERT INTO care_records(health_status, date, animal_id, emp_id, cost) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(insert_query, (health_status, care_date, animal_id, employee_id, cost))
            
        print("Inserted care records.")
        
    except Exception as e:
        print("Error inserting care records:", e)
  
def insert_employment_history(cursor):
    departments_list = get_list(cursor, "departments", "dept_id")
    employees_list = get_list(cursor, "employees", "emp_id")
    try:
        for emp_id in employees_list:
            worked_dept = []
            current_dept = get_element_by_column_where(cursor, "employees", "dept_id", f"emp_id = '{emp_id}'")
            is_dep_changed = fake.boolean(chance_of_getting_true=30)
            if is_dep_changed:
                how_many_times = fake.random_int(min=2, max=3)
                for i in range(how_many_times-1):
                    dept_id = fake.random_element(elements=departments_list)
                    while dept_id == current_dept and dept_id in worked_dept:
                        dept_id = fake.random_element(elements=departments_list)
                    worked_dept.append(dept_id)
                    if i == 0:
                        from_date = fake.date_between_dates(date_start=datetime.date(2010, 1, 1), date_end=datetime.date(2023, 1, 1))
                    else:
                        biggest_last_date = get_element_by_column_where(cursor, "employment_history", "to_date", f"emp_id = '{emp_id}' ORDER BY to_date DESC LIMIT 1")
                        from_date = datetime.datetime.strptime(str(biggest_last_date), "%Y-%m-%d").date()
                    
                    to_date = fake.date_between_dates(date_start=from_date, date_end=datetime.date(2023, 1, 1))   
                    insert_query = "INSERT INTO employment_history(emp_id, dept_id, from_date, to_date) VALUES (%s, %s, %s, %s);"
                    cursor.execute(insert_query, (emp_id, dept_id, from_date, to_date))
                    
               
                biggest_last_date = get_element_by_column_where(cursor, "employment_history", "to_date", f"emp_id = '{emp_id}' ORDER BY to_date DESC LIMIT 1")
                from_date = datetime.datetime.strptime(str(biggest_last_date), "%Y-%m-%d").date()
                
            else:
                from_date = fake.date_between_dates(date_start=datetime.date(2010, 1, 1), date_end=datetime.date(2023, 1, 1))
            #print("inserting employment history")        
            to_date = datetime.date(9999, 1, 1)
            dept_id = current_dept
            insert_query = "INSERT INTO employment_history(emp_id, dept_id, from_date, to_date) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query, (emp_id, dept_id, from_date, to_date)) 
        print("Inserted employment history.")
    
    except Exception as e:
        print("Error inserting employment history:", e)
def drop_all_tables(cursor):
    try:
        tables =["employment_history", "care_records", "adoptions_application", "donations", "adopters", "user_phones", "salaries", "employees", "animals", "users", "shelters", "locations", "departments"]
        for table in tables:
            print(f"Dropping {table}...")
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
        print("Dropped tables.")
    except Exception as e:
        print("Error dropping tables:", e)    
        
def delete_table(cursor, table):
    try:
        print(f"Deleting {table}...")
        cursor.execute(f"DELETE FROM {table};")
        print(f"Deleted {table}.")
    except Exception as e:
        print("Error deleting table:", e)
        
def initialize_all_tables(cursor):
    try:
        print("Initializing tables...")
        cursor.execute(open("initialize_all_tables.sql", "r").read())
        print("Initialized tables.")
    except Exception as e:
        print("Error initializing tables:", e)
    
def insert_all_data(cursor):
    try:
        print("Inserting all data...")
        insert_departments(cursor)
        insert_locations(cursor)
        insert_shelters(cursor)
        insert_users(cursor)
        insert_animals(cursor)
        insert_employees(cursor)
        insert_salaries(cursor)
        insert_user_phones(cursor)
        insert_adopters(cursor)
        insert_donations(cursor)
        insert_adoptions_application(cursor)
        insert_care_records(cursor)
        insert_employment_history(cursor)
        print("Inserted all data.")
    except Exception as e:
        print("Error inserting data:", e)
    

def create_new_random_data(cursor):
    try:
        print("Creating new random data...")
        drop_all_tables(cursor)
        initialize_all_tables(cursor)
        insert_all_data(cursor)
        print("Created new random data.")
    except Exception as e:
        print("Error creating new random data:", e)
        
def close_connections(cursor):
    # Terminate all active connections to the 'test' database
    cursor.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pid <> pg_backend_pid();
    """)    
def create_database(cursor):
    try:
        print("Creating database...")
        cursor.execute(f'CREATE DATABASE "test";')
        print("Created database.")
    except Exception as e:
        print("Error creating database:", e)                   
def delete_database(cursor):
    try:
        print("Deleting database...")
        cursor.execute(f'DROP DATABASE IF EXISTS "test";')
        print("Deleted database.")
    except Exception as e:
        print("Error deleting database:", e)
def import_database_for_animal_sanctuaries_database_sql(cursor):
    try:
        print("Importing database...")
        cursor.execute(open("animal_sanctuaries_database.sql", "r").read())
        print("Imported database.")
    except Exception as e:
        print("Error importing database:", e)                     

def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        user="postgres",
        password="postgres",
        database="test"
    )

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    

    try:
        # close_connections(cursor)
        # delete_database(cursor)
        #create_database(cursor)
        import_database_for_animal_sanctuaries_database_sql(cursor)
        #create_new_random_data(cursor)
        #create_new_random_data(cursor)
        
        conn.commit()

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        
        cursor.close()
        conn.close()


main()


# Human Resources Management System (Django + MongoDB)

This is a comprehensive Human Resources (HR) Management System built with the Django framework and powered by a MongoDB database. The project is designed to handle employee information, company structure, payroll, leave requests, and more. It serves as a robust demonstration of building a full-stack web application with a non-relational database backend.

The system features separate login portals for administrators and employees, each with a dedicated dashboard and specific functionalities. The project is pre-configured with a custom management command to seed the database with a full set of sample data, allowing for immediate testing and exploration of all features.

## Key Features

*   **Secure User Authentication:** Separate login systems for Administrators and Employees.
*   **Administrator Dashboard:** Centralized view to manage all employees, departments, and companies.
*   **Employee Management:** Admins can add, view, and manage detailed employee profiles.
*   **Leave Management:** Employees can apply for leave, and administrators can approve or reject requests.
*   **Detailed Models:** Well-structured models for Companies, Departments, Employee Grades, Addresses, Pay, and Achievements.
*   **Custom Seeding Command:** A reliable management command (`seed_database`) to populate the database with a complete set of test data.
*   **Secure Credentials:** Uses environment variables (`.env` file) to keep sensitive information like database connection strings safe and out of version control.

## Technology Stack

*   **Backend:** Python, Django
*   **Database:** MongoDB
*   **Connector:** Djongo (Django-MongoDB Connector)
*   **Environment Variables:** `python-dotenv`

---

## Setup and Installation

Follow these steps carefully to get the project running on your local machine.

### 1. Clone the Repository
First, clone the project from GitHub to your local machine.



### 2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.



### 3. Install Dependencies
Install all the required Python packages using the `requirements.txt` file.



### 4. Set Up Environment Variables (Crucial Step)
This project uses a `.env` file to securely manage the MongoDB connection string. You must create this file for the application to work.

*   In the root directory of the project, create a new file named `.env`.
*   Open the `.env` file and add your MongoDB Atlas connection string like this:

    ```
    # In your .env file
    MONGO_DB_URL="mongodb+srv://your_username:your_password@your_cluster.mongodb.net/your_database_name?retryWrites=true&w=majority"
    ```
*   **Important:** Replace the placeholder string with your actual connection string from MongoDB Atlas. This file is listed in `.gitignore` and will not be committed to the repository.

### 5. Run Database Migrations
This command connects to your MongoDB database and creates the necessary collections (the equivalent of tables) based on the Django models.



### 6. Seed the Database with Sample Data
Next, run the custom management command to populate the database. This will create the admin user, 11 sample employees, and all associated company data.


You will see output in the terminal confirming that the data is being created.

### 7. Start the Development Server
You are all set! Start the Django server to run the application.


The application will now be running at `http://127.0.0.1:8000/`.

---

## Demo Credentials

You can log in with the following pre-configured accounts to explore the system.

### Admin Account
The administrator can view all employees, add new ones, and approve/reject leave requests.
*   **Login Page:** `http://127.0.0.1:8000/admin_login/`
*   **User ID:** `999`
*   **Password:** `adminpassword`

### Employee Accounts
Employees can log in to view their own dashboard and apply for leave.

| Name / Role            | User ID | Password      |
| ---------------------- | ------- | ------------- |
| Rajesh Raushan (HOD)   | `1`     | `rajesh123`   |
| Vinay Verma (HOD)      | `2`     | `vinay123`    |
| Divya Doijod (Sr)      | `3`     | `divya123`    |
| Manisha Mangal (Sr)    | `4`     | `manisha123`  |
| Payal Pandey (HOD)     | `5`     | `payal123`    |
| Nandana Nair (Sr)      | `6`     | `nandana123`  |
| Anant Agarwal (Jr)     | `7`     | `anant123`    |
| Kanan Kapoor (Jr)      | `8`     | `kanan123`    |
| Tanmay Tandon (Jr)     | `9`     | `tanmay123`   |
| Farah Fisher (Jr)      | `10`    | `farah123`    |
| Howard Herman (Janitor)| `11`    | `howard123`   |


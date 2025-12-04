# Café Menu and Order Management System

A 3-tier database management system project built with Python, Streamlit, and MySQL.

## Project Overview

This system allows café staff to manage menu items, process customer orders, and view sales reports. It is designed to demonstrate a robust 3-tier architecture:
1.  **Presentation Layer**: Streamlit (Web UI)
2.  **Logic Layer**: Python Services & Repositories
3.  **Data Layer**: MySQL Database (BCNF Normalized)

## Architecture

-   **Frontend**: Streamlit `app.py`
-   **Backend**: Python modules in `core/`
    -   `services.py`: Business logic
    -   `repositories.py`: Data access (SQL)
    -   `models.py`: Data transfer objects
    -   `db_connection.py`: Database connectivity
-   **Database**: MySQL
    -   Schema defined in `db/create_schema.sql`
    -   Sample data in `db/initialize_data.sql`

## Setup Instructions

### 1. Database Setup
1.  Ensure you have MySQL installed and running.
2.  Create a database named `cafe_db`.
3.  Run the schema script:
    ```sql
    SOURCE db/create_schema.sql;
    ```
4.  Run the initialization script:
    ```sql
    SOURCE db/initialize_data.sql;
    ```

### 2. Configuration
1.  Copy `config.example.toml` to `config.toml`.
2.  Edit `config.toml` with your MySQL credentials:
    ```toml
    [database]
    host = "localhost"
    port = 3306
    user = "your_user"
    password = "your_password"
    database = "cafe_db"
    ```

### 3. Application Setup
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage Demo

1.  **Login**: Use `admin` / `admin123` (Manager) or `cashier_bob` / `bob123` (Cashier).
2.  **Dashboard**: View daily sales stats.
3.  **Orders**: 
    -   Go to "New Order" tab to create a simulated POS order.
    -   Go to "Manage Orders" to update status (e.g., set to READY or SERVED).
4.  **Menu Management** (Manager only): Add or edit categories and items.
5.  **Reports**: View sales visualization.

## Database Design

The database uses a BCNF normalized schema with the following entities:
-   `Users`: Staff credentials and roles.
-   `MenuCategories` & `MenuItems`: Product catalog.
-   `Orders` & `OrderItems`: Transactional data.

See `docs/final_report_outline.md` for the detailed project report structure.


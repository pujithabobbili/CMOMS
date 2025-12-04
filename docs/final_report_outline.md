# Final Report Outline: Café Menu and Order Management System

## 1. Title Page
- **Project Title**: Café Menu and Order Management System
- **Course**: DBMS [Course Code]
- **Team Members**: Pujitha, Sanya
- **Date**: Dec 4th, 2025

## 2. Introduction
- **Overview**: A web-based POS system for a small café to handle orders, menu management, and sales tracking.
- **Motivation**: To replace manual paper ticketing with a digital, consistent database system.
- **Scope**: Covers menu CRUD, order processing lifecycle, and basic reporting.

## 3. Objectives
- **Primary Goals**:
    - Implement a fully normalized relational database (BCNF).
    - Develop a user-friendly interface for cashiers and managers.
    - Ensure data integrity with foreign keys and constraints.
- **Key Features**: Role-based access, real-time order updates, sales analytics.

## 4. System Architecture
- **3-Tier Design**:
    1.  **Presentation**: Streamlit (Python) for rapid UI development.
    2.  **Logic**: Python Service layer handling business rules (e.g., calculating totals).
    3.  **Data**: Python Repository layer executing raw SQL against MySQL.
- **Tech Stack**: Python 3.10+, Streamlit, MySQL Connector, MySQL 8.0.

## 5. Database Design
- **ER Diagram Description**: 
    - Users manage Orders.
    - Orders contain OrderItems.
    - OrderItems reference MenuItems.
    - MenuItems belong to MenuCategories.
- **Logical Schema**:
    - `Users(user_id, username, password, role)`
    - `MenuCategories(category_id, name, ...)`
    - `MenuItems(item_id, category_id, ...)`
    - `Orders(order_id, user_id, ...)`
    - `OrderItems(order_item_id, order_id, item_id, ...)`
- **Normalization (BCNF)**:
    - Explanation of functional dependencies for each table showing no partial or transitive dependencies.
    - Example: `MenuItems` depends only on `item_id`, not on `category_name`.
- **Constraints**:
    - Primary Keys (Auto Increment).
    - Foreign Keys (referential integrity).
    - `NOT NULL` constraints for mandatory fields.
    - `ENUM` for finite sets (Roles, Status).

## 6. Functional Requirements
- **User Roles**:
    - **Manager**: Full access (Menu editing + all cashier functions).
    - **Cashier**: Order creation and status updates only.
- **Features**:
    - **Authentication**: Secure login/logout.
    - **Menu CRUD**: Create, Read, Update, Delete categories and items.
    - **Order Processing**: Create order -> Add items -> Update status -> Close.
    - **Reporting**: Daily sales aggregation.

## 7. Non-Functional Requirements
- **Performance**: Indexed lookups for orders; efficient joins for reports.
- **Scalability**: Capable of handling hundreds of daily orders.
- **Security**: Password authentication (plaintext for demo, hash recommended for prod), Role-based UI restriction.
- **Usability**: Simple button-driven interface requiring minimal training.

## 8. Implementation Details
- **Code Structure**:
    - `app.py`: Main entry point.
    - `core/`: Modularized backend logic.
    - `db/`: SQL scripts.
- **Key Code Snippets**:
    - *Include `get_connection()` function explanation.*
    - *Include `create_order` transaction logic.*
    - *Include a complex SQL query from `repositories.py`.*

## 9. Testing and Validation
- **Methodology**: Manual testing of all UI flows.
- **Test Cases**:
    - Successful Login vs Invalid Login.
    - Creating an order and verifying DB insertion.
    - Deleting a category with active items (constraint check).
- **Sample Data**: Utilized ~15 rows per table to simulate a realistic operating day.

## 10. Challenges and Solutions
- **Challenge**: Managing state in Streamlit (stateless web framework).
    - **Solution**: Used `st.session_state` to persist user login and active order draft.
- **Challenge**: Handling complex joins for reports.
    - **Solution**: Wrote optimized SQL views/queries in the repository layer.

## 11. Future Enhancements
- Password hashing (bcrypt).
- Inventory management (ingredient tracking).
- Customer loyalty program.
- Receipt printing integration.

## 12. Conclusion
- Summary of project success in meeting BCNF and functional requirements.
- Lessons learned regarding database design and Python integration.

## Appendices
- **A. SQL Schema**: (Refer to `db/create_schema.sql`)
- **B. Sample Queries**: (Refer to `db/sample_queries.sql`)


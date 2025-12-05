from typing import List, Optional, Tuple
from datetime import date
from core.db_connection import get_connection
from core.models import User, MenuCategory, MenuItem, Order, OrderItem

# --- Users ---

def get_user_by_credentials(username: str, password: str) -> Optional[User]:
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        row = cursor.fetchone()
        if row:
            return User(**row)
        return None
    finally:
        if conn:
            conn.close()

# --- Menu Categories ---

def list_categories() -> List[MenuCategory]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MenuCategories ORDER BY display_order")
        rows = cursor.fetchall()
        return [MenuCategory(**row) for row in rows]
    finally:
        if conn:
            conn.close()

def get_category(category_id: int) -> Optional[MenuCategory]:
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MenuCategories WHERE category_id = %s", (category_id,))
        row = cursor.fetchone()
        if row:
            return MenuCategory(**row)
        return None
    finally:
        if conn:
            conn.close()

def create_category(name: str, display_order: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "INSERT INTO MenuCategories (name, display_order) VALUES (%s, %s)"
        cursor.execute(query, (name, display_order))
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_category(category_id: int, name: str, display_order: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "UPDATE MenuCategories SET name = %s, display_order = %s WHERE category_id = %s"
        cursor.execute(query, (name, display_order, category_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_category(category_id: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM MenuCategories WHERE category_id = %s"
        cursor.execute(query, (category_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()

# --- Menu Items ---

def list_menu_items(include_inactive: bool = False) -> List[MenuItem]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT m.*, c.name as category_name 
            FROM MenuItems m
            JOIN MenuCategories c ON m.category_id = c.category_id
        """
        if not include_inactive:
            query += " WHERE m.is_active = 1"
        query += " ORDER BY c.display_order, m.name"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        items = []
        for row in rows:
            # Convert decimal to float for Python
            row['price'] = float(row['price'])
            items.append(MenuItem(**row))
        return items
    finally:
        if conn:
            conn.close()

def get_menu_item(item_id: int) -> Optional[MenuItem]:
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM MenuItems WHERE item_id = %s"
        cursor.execute(query, (item_id,))
        row = cursor.fetchone()
        if row:
            row['price'] = float(row['price'])
            return MenuItem(**row)
        return None
    finally:
        if conn:
            conn.close()

def create_menu_item(category_id: int, name: str, price: float, is_active: bool):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "INSERT INTO MenuItems (category_id, name, price, is_active) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (category_id, name, price, int(is_active)))
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_menu_item(item_id: int, category_id: int, name: str, price: float, is_active: bool):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "UPDATE MenuItems SET category_id = %s, name = %s, price = %s, is_active = %s WHERE item_id = %s"
        cursor.execute(query, (category_id, name, price, int(is_active), item_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_menu_item(item_id: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM MenuItems WHERE item_id = %s"
        cursor.execute(query, (item_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()

# --- Orders & Order Items ---

def create_order(user_id: int, table_number: str, notes: str) -> int:
    conn = get_connection()
    if not conn:
        return -1
    try:
        cursor = conn.cursor()
        query = "INSERT INTO Orders (user_id, table_number, notes, order_status) VALUES (%s, %s, %s, 'PENDING')"
        cursor.execute(query, (user_id, table_number, notes))
        conn.commit()
        return cursor.lastrowid
    finally:
        if conn:
            conn.close()

def add_order_item(order_id: int, item_id: int, quantity: int, note: str):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Get price first
        cursor.execute("SELECT price FROM MenuItems WHERE item_id = %s", (item_id,))
        row = cursor.fetchone()
        if not row:
            return 
        price = float(row[0])
        line_total = price * quantity
        
        query = "INSERT INTO OrderItems (order_id, item_id, quantity, note, line_total) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (order_id, item_id, quantity, note, line_total))
        conn.commit()
    finally:
        if conn:
            conn.close()

def list_orders_by_status(status: Optional[str] = None) -> List[Order]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o.*, u.username as cashier_name, 
                   COALESCE(SUM(oi.line_total), 0) as total_amount
            FROM Orders o
            JOIN Users u ON o.user_id = u.user_id
            LEFT JOIN OrderItems oi ON o.order_id = oi.order_id
        """
        params = []
        if status:
            query += " WHERE o.order_status = %s"
            params.append(status)
            
        query += " GROUP BY o.order_id ORDER BY o.created_at DESC"
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            row['total_amount'] = float(row['total_amount'])
            orders.append(Order(**row))
        return orders
    finally:
        if conn:
            conn.close()

def get_order_with_items(order_id: int) -> Optional[Order]:
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        # Get Order info
        query_order = """
            SELECT o.*, u.username as cashier_name
            FROM Orders o
            JOIN Users u ON o.user_id = u.user_id
            WHERE o.order_id = %s
        """
        cursor.execute(query_order, (order_id,))
        order_row = cursor.fetchone()
        if not order_row:
            return None
        
        # Get Items
        query_items = """
            SELECT oi.*, m.name as item_name
            FROM OrderItems oi
            JOIN MenuItems m ON oi.item_id = m.item_id
            WHERE oi.order_id = %s
        """
        cursor.execute(query_items, (order_id,))
        item_rows = cursor.fetchall()
        
        items = []
        total = 0.0
        for i_row in item_rows:
            i_row['line_total'] = float(i_row['line_total'])
            total += i_row['line_total']
            items.append(OrderItem(**i_row))
            
        order_row['items'] = items
        order_row['total_amount'] = total
        return Order(**order_row)
    finally:
        if conn:
            conn.close()

def update_order_status(order_id: int, new_status: str):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        closed_at_clause = ""
        if new_status in ['SERVED', 'CANCELLED']:
            closed_at_clause = ", closed_at = NOW()"
            
        query = f"UPDATE Orders SET order_status = %s {closed_at_clause} WHERE order_id = %s"
        cursor.execute(query, (new_status, order_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_order_item(order_item_id: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM OrderItems WHERE order_item_id = %s"
        cursor.execute(query, (order_item_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()

# --- Reports ---

def get_today_sales_total() -> float:
    conn = get_connection()
    if not conn:
        return 0.0
    try:
        cursor = conn.cursor()
        query = """
            SELECT SUM(oi.line_total) 
            FROM Orders o
            JOIN OrderItems oi ON o.order_id = oi.order_id
            WHERE DATE(o.created_at) = CURDATE() 
            AND o.order_status != 'CANCELLED'
        """
        cursor.execute(query)
        row = cursor.fetchone()
        return float(row[0]) if row and row[0] else 0.0
    finally:
        if conn:
            conn.close()

def get_top_item_today() -> Optional[str]:
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        query = """
            SELECT m.name 
            FROM OrderItems oi
            JOIN Orders o ON oi.order_id = o.order_id
            JOIN MenuItems m ON oi.item_id = m.item_id
            WHERE DATE(o.created_at) = CURDATE()
            AND o.order_status != 'CANCELLED'
            GROUP BY m.item_id
            ORDER BY SUM(oi.quantity) DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0] if row else "N/A"
    finally:
        if conn:
            conn.close()

def get_sales_by_category() -> List[Tuple[str, float]]:
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT c.name, SUM(oi.line_total)
            FROM OrderItems oi
            JOIN MenuItems m ON oi.item_id = m.item_id
            JOIN MenuCategories c ON m.category_id = c.category_id
            JOIN Orders o ON oi.order_id = o.order_id
            WHERE o.order_status != 'CANCELLED'
            GROUP BY c.category_id
            ORDER BY SUM(oi.line_total) DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return [(row[0], float(row[1])) for row in rows]
    finally:
        if conn:
            conn.close()

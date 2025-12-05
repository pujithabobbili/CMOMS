from typing import Optional, List, Tuple
from core.models import User, Order, MenuItem, MenuCategory
import core.repositories as repo

# --- Authentication ---

def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticates a user by username and password.
    Returns User object if successful, None otherwise.
    """
    return repo.get_user_by_credentials(username, password)

# --- Menu Management ---

def get_all_categories() -> List[MenuCategory]:
    return repo.list_categories()

def create_category(name: str, display_order: int):
    repo.create_category(name, display_order)

def update_category(category_id: int, name: str, display_order: int):
    repo.update_category(category_id, name, display_order)

def delete_category(category_id: int):
    # This might raise a ValueError if category has items (Foreign Key constraint)
    # The caller (app.py) should handle this.
    repo.delete_category(category_id)

def get_menu_items(active_only: bool = True) -> List[MenuItem]:
    return repo.list_menu_items(not active_only)

def add_menu_item(category_id: int, name: str, price: float, is_active: bool):
    repo.create_menu_item(category_id, name, price, is_active)

def edit_menu_item(item_id: int, category_id: int, name: str, price: float, is_active: bool):
    repo.update_menu_item(item_id, category_id, name, price, is_active)

def remove_menu_item(item_id: int): # Soft delete usually preferred, but requirement implies CRUD
    repo.delete_menu_item(item_id) 

def toggle_item_active(item_id: int):
    item = repo.get_menu_item(item_id)
    if item:
        repo.update_menu_item(item.item_id, item.category_id, item.name, item.price, not item.is_active)

# --- Order Management ---

def create_new_order(user_id: int, table_number: str, notes: str) -> int:
    return repo.create_order(user_id, table_number, notes)

def add_item_to_order(order_id: int, item_id: int, quantity: int, note: str):
    if quantity > 0:
        repo.add_order_item(order_id, item_id, quantity, note)

def remove_item_from_order(order_item_id: int):
    repo.delete_order_item(order_item_id)

def get_order_details(order_id: int) -> Optional[Order]:
    return repo.get_order_with_items(order_id)

def get_orders(status_filter: Optional[str] = None) -> List[Order]:
    return repo.list_orders_by_status(status_filter)

def change_order_status(order_id: int, new_status: str):
    repo.update_order_status(order_id, new_status)

# --- Reports ---

def get_dashboard_stats() -> dict:
    return {
        "today_sales": repo.get_today_sales_total(),
        "top_item": repo.get_top_item_today(),
        "sales_by_category": repo.get_sales_by_category()
    }

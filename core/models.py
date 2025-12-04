from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    user_id: int
    username: str
    password: str
    role: str

@dataclass
class MenuCategory:
    category_id: int
    name: str
    display_order: int

@dataclass
class MenuItem:
    item_id: int
    category_id: int
    name: str
    price: float
    is_active: bool
    category_name: Optional[str] = None # Helper for display

@dataclass
class OrderItem:
    order_item_id: int
    order_id: int
    item_id: int
    quantity: int
    note: str
    line_total: float
    item_name: Optional[str] = None # Helper for display

@dataclass
class Order:
    order_id: int
    user_id: int
    table_number: str
    order_status: str
    notes: str
    created_at: datetime
    closed_at: Optional[datetime]
    items: List[OrderItem] = None
    total_amount: float = 0.0
    cashier_name: Optional[str] = None # Helper for display
    
    def __post_init__(self):
        if self.items is None:
            self.items = []


import streamlit as st
import pandas as pd
from core import services
from core.models import User

# --- Page Configuration ---
st.set_page_config(
    page_title="CMOMS - Café Menu & Order Management",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Café Theme ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;500;600&display=swap');
    
    /* Root Variables */
    :root {
        --beige-light: #F5F0E6;
        --beige: #E8DFD0;
        --cream: #FFF8E7;
        --brown-light: #8D6E63;
        --brown: #5D4037;
        --brown-dark: #3E2723;
        --espresso: #2C1810;
        --gold: #C9A227;
        --success: #6B8E23;
        --warning: #D4A574;
        --danger: #8B4513;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #F5F0E6 0%, #E8DFD0 100%);
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* All text defaults */
    html, body, [class*="css"] {
        font-family: 'Lato', sans-serif;
        color: var(--brown-dark);
    }
    
    /* Headers */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--brown-dark) !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        letter-spacing: 1px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--brown-dark) 0%, var(--brown) 100%);
        border-right: 3px solid var(--gold);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--cream) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--gold) !important;
        font-family: 'Playfair Display', serif !important;
    }
    
    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] .stRadio > label {
        color: var(--cream) !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
        color: var(--cream) !important;
    }
    
    /* Primary Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--brown) 0%, var(--brown-dark) 100%);
        color: var(--cream) !important;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-family: 'Lato', sans-serif;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(62, 39, 35, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--brown-light) 0%, var(--brown) 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(62, 39, 35, 0.4);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--gold) 0%, #A68B1F 100%);
        color: var(--brown-dark) !important;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: var(--cream) !important;
        border: 2px solid var(--beige) !important;
        border-radius: 10px !important;
        color: var(--brown-dark) !important;
        font-family: 'Lato', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--brown) !important;
        box-shadow: 0 0 0 2px rgba(93, 64, 55, 0.2) !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, var(--cream) 0%, #FFF5E0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(62, 39, 35, 0.1);
        border-left: 4px solid var(--gold);
    }
    
    [data-testid="stMetric"] label {
        color: var(--brown) !important;
        font-family: 'Lato', sans-serif !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--brown-dark) !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important;
    }
    
    /* DataFrames and Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(62, 39, 35, 0.1);
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background-color: var(--cream);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--cream) !important;
        border-radius: 10px !important;
        border: 1px solid var(--beige) !important;
        font-family: 'Lato', sans-serif !important;
        font-weight: 500 !important;
        color: var(--brown-dark) !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--cream) !important;
        border: 1px solid var(--beige) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--beige);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-family: 'Lato', sans-serif;
        font-weight: 500;
        color: var(--brown);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--cream) !important;
        color: var(--brown-dark) !important;
        border-bottom: 3px solid var(--gold) !important;
    }
    
    /* Forms */
    [data-testid="stForm"] {
        background-color: var(--cream);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid var(--beige);
        box-shadow: 0 2px 10px rgba(62, 39, 35, 0.08);
    }
    
    /* Info/Success/Warning/Error boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    /* Dividers */
    hr {
        border-color: var(--beige);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--beige-light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--brown-light);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--brown);
    }
    
    /* Status Badge Styles */
    .status-pending { 
        background-color: #FFF3CD; 
        color: #856404; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-weight: 500;
        font-size: 0.85rem;
    }
    .status-in-prep { 
        background-color: #D4EDDA; 
        color: #155724; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-weight: 500;
        font-size: 0.85rem;
    }
    .status-ready { 
        background-color: #CCE5FF; 
        color: #004085; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-weight: 500;
        font-size: 0.85rem;
    }
    .status-served { 
        background-color: #D1ECF1; 
        color: #0C5460; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-weight: 500;
        font-size: 0.85rem;
    }
    .status-cancelled { 
        background-color: #F8D7DA; 
        color: #721C24; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Logo/Title styling */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--brown-dark);
        text-align: center;
        margin-bottom: 0;
        letter-spacing: 3px;
    }
    
    .tagline {
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        color: var(--brown);
        text-align: center;
        font-weight: 300;
        letter-spacing: 2px;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    
    .sidebar-brand {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--gold) !important;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(201, 162, 39, 0.3);
        margin-bottom: 1rem;
    }
    
    .coffee-icon {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# --- Helper Functions ---
def get_status_badge(status):
    """Returns HTML for a styled status badge"""
    status_class = f"status-{status.lower().replace('_', '-')}"
    return f'<span class="{status_class}">{status}</span>'

def login():
    # Centered login with branding
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="coffee-icon">☕</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">CMOMS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline">Café Menu & Order Management System</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        with st.form("login_form"):
            st.markdown("#### Welcome Back")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submitted = st.form_submit_button("☕ Sign In", use_container_width=True)
            
            if submitted:
                user = services.authenticate_user(username, password)
                if user:
                    st.session_state["current_user"] = user
                    st.success(f"Welcome back, {user.username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

def logout():
    st.session_state["current_user"] = None
    st.rerun()

# --- Main Views ---

def view_dashboard():
    st.markdown("## 📊 Dashboard")
    st.markdown("---")
    
    stats = services.get_dashboard_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Today's Sales", f"${stats['today_sales']:.2f}")
    with col2:
        st.metric("🏆 Top Item Today", stats['top_item'] or "N/A")
    with col3:
        # Count orders by getting all orders
        orders = services.get_orders()
        active_orders = len([o for o in orders if o.order_status in ['PENDING', 'IN_PREP', 'READY']])
        st.metric("📋 Active Orders", active_orders)
    
    st.markdown("---")
    st.markdown("### 📈 Sales by Category")
    
    if stats['sales_by_category']:
        df = pd.DataFrame(stats['sales_by_category'], columns=['Category', 'Total Sales'])
        st.bar_chart(df.set_index('Category'), color="#5D4037")
    else:
        st.info("☕ No sales data available yet. Start taking orders!")

def view_menu_management():
    st.markdown("## 🍽️ Menu Management")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📁 Categories", "☕ Menu Items"])
    
    with tab1:
        st.markdown("### Manage Categories")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Add New Category")
            with st.form("add_category"):
                new_cat_name = st.text_input("Category Name", placeholder="e.g., Hot Beverages")
                new_cat_order = st.number_input("Display Order", min_value=1, value=1)
                if st.form_submit_button("➕ Add Category", use_container_width=True):
                    if new_cat_name:
                        services.create_category(new_cat_name, new_cat_order)
                        st.success("✓ Category added successfully!")
                        st.rerun()
        
        with col2:
            st.markdown("#### Current Categories")
            categories = services.get_all_categories()
            if categories:
                df_cat = pd.DataFrame([{
                    "ID": c.category_id,
                    "Name": c.name,
                    "Display Order": c.display_order
                } for c in categories])
                st.dataframe(df_cat, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    cat_to_delete = st.selectbox(
                        "Select Category to Delete", 
                        options=categories, 
                        format_func=lambda x: x.name
                    )
                with col_b:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️ Delete Category"):
                        services.delete_category(cat_to_delete.category_id)
                        st.warning("Category deleted")
                        st.rerun()
    
    with tab2:
        st.markdown("### Manage Menu Items")
        categories = services.get_all_categories()
        
        with st.expander("➕ Add New Menu Item", expanded=False):
            with st.form("add_item"):
                col1, col2 = st.columns(2)
                with col1:
                    cat_options = {c.name: c.category_id for c in categories}
                    selected_cat_name = st.selectbox("Category", options=list(cat_options.keys()))
                    item_name = st.text_input("Item Name", placeholder="e.g., Cappuccino")
                with col2:
                    item_price = st.number_input("Price ($)", min_value=0.01, format="%.2f", value=4.50)
                    item_active = st.checkbox("Active", value=True)
                
                if st.form_submit_button("➕ Create Item", use_container_width=True):
                    if item_name and selected_cat_name:
                        services.add_menu_item(cat_options[selected_cat_name], item_name, item_price, item_active)
                        st.success("✓ Item created successfully!")
                        st.rerun()

        # Edit Item Section
        items_for_edit = services.get_menu_items(active_only=False)
        if items_for_edit:
            with st.expander("✏️ Edit Menu Item", expanded=False):
                with st.form("edit_item"):
                    item_to_edit = st.selectbox(
                        "Select Item to Edit",
                        options=items_for_edit,
                        format_func=lambda x: f"{x.name} (Current: ${x.price:.2f})"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        cat_options_edit = {c.name: c.category_id for c in categories}
                        # Find current category name
                        current_cat_name = next((c.name for c in categories if c.category_id == item_to_edit.category_id), list(cat_options_edit.keys())[0])
                        new_category = st.selectbox(
                            "Category",
                            options=list(cat_options_edit.keys()),
                            index=list(cat_options_edit.keys()).index(current_cat_name) if current_cat_name in cat_options_edit else 0
                        )
                        new_name = st.text_input("Item Name", value=item_to_edit.name)
                    with col2:
                        new_price = st.number_input("New Price ($)", min_value=0.01, format="%.2f", value=float(item_to_edit.price))
                        new_active = st.checkbox("Active", value=item_to_edit.is_active)
                    
                    if st.form_submit_button("💾 Update Item", use_container_width=True):
                        services.edit_menu_item(
                            item_to_edit.item_id,
                            cat_options_edit[new_category],
                            new_name,
                            new_price,
                            new_active
                        )
                        st.success("✓ Item updated successfully!")
                        st.rerun()

        st.markdown("#### Current Menu")
        items = services.get_menu_items(active_only=False)
        if items:
            data = []
            for i in items:
                data.append({
                    "ID": i.item_id,
                    "Category": i.category_name,
                    "Name": i.name,
                    "Price": f"${i.price:.2f}",
                    "Status": "✓ Active" if i.is_active else "✗ Inactive"
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                item_to_toggle = st.selectbox(
                    "Select Item to Toggle Status", 
                    options=items, 
                    format_func=lambda x: f"{x.name} (${x.price:.2f})"
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Toggle Active Status"):
                    services.toggle_item_active(item_to_toggle.item_id)
                    st.rerun()

def view_orders():
    st.markdown("## 📝 Orders")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🛒 New Order (POS)", "📋 Manage Orders"])
    
    # --- POS Tab ---
    with tab1:
        st.markdown("### Create New Order")
        
        if "current_order_id" not in st.session_state:
            st.session_state["current_order_id"] = None
            
        if st.session_state["current_order_id"] is None:
            with st.form("init_order"):
                col1, col2 = st.columns(2)
                with col1:
                    table_num = st.text_input("Table Number / Name", placeholder="e.g., T1, Takeout")
                with col2:
                    notes = st.text_input("Order Notes (optional)", placeholder="e.g., Birthday celebration")
                
                if st.form_submit_button("🚀 Start Order", use_container_width=True):
                    if table_num:
                        user_id = st.session_state["current_user"].user_id
                        new_id = services.create_new_order(user_id, table_num, notes)
                        st.session_state["current_order_id"] = new_id
                        st.rerun()
                    else:
                        st.warning("Please enter a table number")
        else:
            order_id = st.session_state["current_order_id"]
            order = services.get_order_details(order_id)
            
            st.info(f"📋 **Order #{order_id}** for **Table: {order.table_number}**")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### Add Items")
                active_items = services.get_menu_items(active_only=True)
                selected_item = st.selectbox(
                    "Menu Item", 
                    options=active_items, 
                    format_func=lambda x: f"{x.name} (${x.price:.2f})"
                )
                qty = st.number_input("Quantity", min_value=1, value=1)
                note = st.text_input("Item Note", placeholder="e.g., no sugar")
                
                if st.button("➕ Add to Order", use_container_width=True):
                    services.add_item_to_order(order_id, selected_item.item_id, qty, note)
                    st.rerun()
                
                st.markdown("---")
                
                if st.button("✅ Send to Kitchen", type="primary", use_container_width=True):
                    services.change_order_status(order_id, "IN_PREP")
                    st.session_state["current_order_id"] = None
                    st.success("Order submitted!")
                    st.rerun()
                    
                if st.button("❌ Cancel Order", use_container_width=True):
                    services.change_order_status(order_id, "CANCELLED")
                    st.session_state["current_order_id"] = None
                    st.rerun()

            with col2:
                st.markdown("#### Order Summary")
                if order and order.items:
                    order_data = []
                    for item in order.items:
                        order_data.append({
                            "Item": item.item_name,
                            "Qty": item.quantity,
                            "Note": item.note or "-",
                            "Total": f"${item.line_total:.2f}"
                        })
                    st.table(order_data)
                    
                    st.markdown("---")
                    st.metric("💵 Grand Total", f"${order.total_amount:.2f}")
                else:
                    st.info("No items added yet. Select items from the menu.")

    # --- Manage Orders Tab ---
    with tab2:
        st.markdown("### Kitchen / Management View")
        
        status_filter = st.selectbox(
            "Filter by Status", 
            ["ALL", "PENDING", "IN_PREP", "READY", "SERVED", "CANCELLED"],
            index=0
        )
        
        orders = services.get_orders(None if status_filter == "ALL" else status_filter)
        
        if not orders:
            st.info("No orders found with the selected filter.")
        
        for o in orders:
            status_emoji = {
                "PENDING": "⏳",
                "IN_PREP": "👨‍🍳",
                "READY": "✅",
                "SERVED": "🍽️",
                "CANCELLED": "❌"
            }.get(o.order_status, "")
            
            with st.expander(f"{status_emoji} Order #{o.order_id} - {o.table_number} | ${o.total_amount:.2f}"):
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**Cashier:** {o.cashier_name}")
                col2.markdown(f"**Time:** {o.created_at.strftime('%H:%M')}")
                col3.markdown(f"**Status:** {get_status_badge(o.order_status)}", unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Status Change
                new_status = st.selectbox(
                    "Update Status", 
                    options=['PENDING', 'IN_PREP', 'READY', 'SERVED', 'CANCELLED'],
                    key=f"status_{o.order_id}",
                    index=['PENDING', 'IN_PREP', 'READY', 'SERVED', 'CANCELLED'].index(o.order_status)
                )
                
                if new_status != o.order_status:
                    services.change_order_status(o.order_id, new_status)
                    st.rerun()
                
                # Order Details
                full_order = services.get_order_details(o.order_id)
                if full_order and full_order.items:
                    st.markdown("**Items:**")
                    st.table([
                        {"Item": i.item_name, "Qty": i.quantity, "Note": i.note or "-"}
                        for i in full_order.items
                    ])

def view_reports():
    st.markdown("## 📊 Reports & Analytics")
    st.markdown("---")
    
    stats = services.get_dashboard_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Today's Revenue", f"${stats['today_sales']:.2f}")
    with col2:
        st.metric("🏆 Best Seller Today", stats['top_item'] or "N/A")
    
    st.markdown("---")
    st.markdown("### 📈 Revenue by Category")
    
    if stats['sales_by_category']:
        df = pd.DataFrame(stats['sales_by_category'], columns=['Category', 'Total Sales'])
        st.bar_chart(df.set_index('Category'), color="#5D4037")
        
        st.markdown("---")
        st.markdown("### 📋 Detailed Breakdown")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("☕ No sales data available yet.")

# --- Main App Logic ---

def main():
    if not st.session_state["current_user"]:
        login()
        return

    # Sidebar Navigation with Branding
    with st.sidebar:
        st.markdown('<div class="coffee-icon">☕</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-brand">CMOMS</div>', unsafe_allow_html=True)
        
        user = st.session_state["current_user"]
        st.markdown(f"**{user.username}**")
        st.caption(f"Role: {user.role}")
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "📝 Orders", "🍽️ Menu Management", "📈 Reports"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # Main Content
    if "Dashboard" in page:
        view_dashboard()
    elif "Orders" in page:
        view_orders()
    elif "Menu Management" in page:
        if user.role == "MANAGER":
            view_menu_management()
        else:
            st.error("🔒 Access Denied: Manager privileges required.")
    elif "Reports" in page:
        view_reports()

if __name__ == "__main__":
    main()

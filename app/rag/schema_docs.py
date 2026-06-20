SCHEMA_DOCS = [
    """
    Table: customers

    Description:
    Stores customer information.

    Primary Key:
    customer_id

    Columns:
    customer_id (INTEGER)
    name (TEXT)
    city (TEXT)
    signup_date (DATE)

    Relationships:
    customers.customer_id -> orders.customer_id

    Example Questions:
    - List all customers
    - Customers from Chennai
    - Customers who placed orders
    - Top customers by spending
    """,
    """
    Table: orders

    Description:
    Stores customer orders.

    Primary Key:
    order_id

    Foreign Keys:
    customer_id -> customers.customer_id

    Columns:
    order_id (INTEGER)
    customer_id (INTEGER)
    order_date (DATE)
    total_amount (NUMERIC)

    Relationships:
    orders.customer_id -> customers.customer_id
    orders.order_id -> order_items.order_id
    orders.order_id -> payments.order_id

    Example Questions:
    - Total revenue
    - Number of orders
    - Average order value
    - Orders placed this month
    """,
    """
    Table: products

    Description:
    Stores products available for purchase.

    Primary Key:
    product_id

    Columns:
    product_id (INTEGER)
    product_name (TEXT)
    category (TEXT)
    price (NUMERIC)

    Relationships:
    products.product_id -> order_items.product_id

    Example Questions:
    - List all products
    - Products by category
    - Most expensive products
    - Product revenue
    """,
    """
    Table: order_items

    Description:
    Stores products included in each order.

    Primary Key:
    id

    Foreign Keys:
    order_id -> orders.order_id
    product_id -> products.product_id

    Columns:
    id (INTEGER)
    order_id (INTEGER)
    product_id (INTEGER)
    quantity (INTEGER)

    Relationships:
    order_items.order_id -> orders.order_id
    order_items.product_id -> products.product_id

    Example Questions:
    - Most sold products
    - Product sales quantity
    - Revenue by product
    - Products purchased in an order
    """,
    """
    Table: payments

    Description:
    Stores payment records for orders.

    Primary Key:
    payment_id

    Foreign Keys:
    order_id -> orders.order_id

    Columns:
    payment_id (INTEGER)
    order_id (INTEGER)
    payment_method (TEXT)
    amount (NUMERIC)

    Relationships:
    payments.order_id -> orders.order_id

    Example Questions:
    - Revenue by payment method
    - Total payments
    - UPI transactions
    - Credit card transactions
    """,
]

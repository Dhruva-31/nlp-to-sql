from faker import Faker
from sqlalchemy import text

from app.db.connection import engine

import random

fake = Faker()


NUM_CUSTOMERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 200

cities = [
    "Chennai",
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Coimbatore",
    "Jaipur",
]

categories = [
    "Mobile",
    "Laptop",
    "Audio",
    "Accessories",
    "Gaming",
]


def create_tables():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                signup_date DATE NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price NUMERIC(10,2) NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                order_date DATE NOT NULL,
                total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
                CONSTRAINT fk_orders_customer
                    FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
                    ON DELETE CASCADE
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                CONSTRAINT fk_order_items_order
                    FOREIGN KEY (order_id)
                    REFERENCES orders(order_id)
                    ON DELETE CASCADE,
                CONSTRAINT fk_order_items_product
                    FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                amount NUMERIC(12,2) NOT NULL,
                CONSTRAINT fk_payments_order
                    FOREIGN KEY (order_id)
                    REFERENCES orders(order_id)
                    ON DELETE CASCADE
            )
        """))

    print("Tables created")


def clear_tables():

    with engine.begin() as conn:

        conn.execute(
            text(
                "TRUNCATE TABLE payments, order_items, orders, products, customers RESTART IDENTITY CASCADE"
            )
        )

    print("Tables cleared")


def seed_customers():

    with engine.begin() as conn:

        for _ in range(NUM_CUSTOMERS):

            conn.execute(
                text("""
                    INSERT INTO customers
                    (
                        name,
                        city,
                        signup_date
                    )
                    VALUES
                    (
                        :name,
                        :city,
                        :signup_date
                    )
                    """),
                {
                    "name": fake.name(),
                    "city": random.choice(cities),
                    "signup_date": fake.date_between(
                        start_date="-3y",
                        end_date="today",
                    ),
                },
            )

    print(f"{NUM_CUSTOMERS} customers inserted")


def seed_products():

    with engine.begin() as conn:

        for i in range(NUM_PRODUCTS):

            conn.execute(
                text("""
                    INSERT INTO products
                    (
                        product_name,
                        category,
                        price
                    )
                    VALUES
                    (
                        :product_name,
                        :category,
                        :price
                    )
                    """),
                {
                    "product_name": f"Product-{i+1}",
                    "category": random.choice(categories),
                    "price": round(
                        random.uniform(500, 100000),
                        2,
                    ),
                },
            )

    print(f"{NUM_PRODUCTS} products inserted")


def seed_orders():

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
    ]

    with engine.begin() as conn:

        for _ in range(NUM_ORDERS):

            customer_id = random.randint(
                1,
                NUM_CUSTOMERS,
            )

            order_date = fake.date_between(
                start_date="-1y",
                end_date="today",
            )

            order_result = conn.execute(
                text("""
                    INSERT INTO orders
                    (
                        customer_id,
                        order_date,
                        total_amount
                    )
                    VALUES
                    (
                        :customer_id,
                        :order_date,
                        0
                    )
                    RETURNING order_id
                    """),
                {
                    "customer_id": customer_id,
                    "order_date": order_date,
                },
            )

            order_id = order_result.scalar_one()

            total_amount = 0

            num_items = random.randint(1, 5)

            for _ in range(num_items):

                product_id = random.randint(
                    1,
                    NUM_PRODUCTS,
                )

                quantity = random.randint(
                    1,
                    5,
                )

                price_result = conn.execute(
                    text("""
                        SELECT price
                        FROM products
                        WHERE product_id = :product_id
                        """),
                    {
                        "product_id": product_id,
                    },
                )

                product_price = price_result.scalar_one()

                total_amount += product_price * quantity

                conn.execute(
                    text("""
                        INSERT INTO order_items
                        (
                            order_id,
                            product_id,
                            quantity
                        )
                        VALUES
                        (
                            :order_id,
                            :product_id,
                            :quantity
                        )
                        """),
                    {
                        "order_id": order_id,
                        "product_id": product_id,
                        "quantity": quantity,
                    },
                )

            conn.execute(
                text("""
                    UPDATE orders
                    SET total_amount = :total_amount
                    WHERE order_id = :order_id
                    """),
                {
                    "total_amount": round(
                        total_amount,
                        2,
                    ),
                    "order_id": order_id,
                },
            )

            conn.execute(
                text("""
                    INSERT INTO payments
                    (
                        order_id,
                        payment_method,
                        amount
                    )
                    VALUES
                    (
                        :order_id,
                        :payment_method,
                        :amount
                    )
                    """),
                {
                    "order_id": order_id,
                    "payment_method": random.choice(payment_methods),
                    "amount": round(
                        total_amount,
                        2,
                    ),
                },
            )

    print(f"{NUM_ORDERS} orders inserted")


if __name__ == "__main__":

    create_tables()

    clear_tables()

    seed_customers()

    seed_products()

    seed_orders()

    print("\nDatabase seeded successfully")

from faker import Faker
from sqlalchemy import text

from connection import engine

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


def clear_tables():

    with engine.begin() as conn:

        conn.execute(text("TRUNCATE TABLE payments RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE order_items RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE customers RESTART IDENTITY CASCADE"))

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

    clear_tables()

    seed_customers()

    seed_products()

    seed_orders()

    print("\nDatabase seeded successfully")

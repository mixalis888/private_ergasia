from datetime import datetime


class Customer:
    def __init__(self, full_name: str, phone: str, email: str):
        self.full_name = full_name
        self.phone = phone
        self.email = email


class EshopManager:
    def __init__(self, manager_id: int, username: str, password: str, email: str):
        self.manager_id = manager_id
        self.username = username
        self.password = password
        self.email = email


class Order:
    def __init__(self, order_id: str, customer: Customer, delivery_address: str):
        self.order_id = order_id
        self.customer = customer
        self.date = datetime.now()
        self.delivery_address = delivery_address
        self.status = "registered"

    def __str__(self):
        return (
            f"Order ID: {self.order_id}\n"
            f"Customer: {self.customer.full_name}\n"
            f"Delivery Address: {self.delivery_address}\n"
            f"Status: {self.status}\n"
        )
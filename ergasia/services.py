import re
from .models import Customer, Order


class OrderService:
    def __init__(self):
        self.orders = []
        self.order_counter = 1

    def validate(self, full_name, phone, email, address):
        if not full_name or not phone or not email or not address:
            return False, "Σφάλμα: Κενά πεδία."

        if "@" not in email:
            return False, "Σφάλμα: Μη έγκυρο email."

        if not phone.isdigit():
            return False, "Σφάλμα: Το τηλέφωνο πρέπει να περιέχει μόνο αριθμούς."

        return True, ""

    def save_order(self, customer, address):
        order_id = f"ORD-{self.order_counter:04d}"
        self.order_counter += 1

        order = Order(order_id, customer, address)
        self.orders.append(order)
        return order

    def send_notification(self, order):
        print("\n--- ΕΙΔΟΠΟΙΗΣΗ ---")
        print(f"Η παραγγελία {order.order_id} καταχωρήθηκε.")
        print("-------------------\n")
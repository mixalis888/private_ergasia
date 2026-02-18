from ergasia.models import EshopManager, Customer
from ergasia.services import OrderService


def main():
    manager = EshopManager(1, "admin", "1234", "admin@eshop.gr")
    service = OrderService()

    while True:
        print("===== Σύστημα Καταχώρησης Παραγγελίας =====")
        print("1. Νέα Παραγγελία")
        print("2. Προβολή Παραγγελιών")
        print("0. Έξοδος")

        choice = input("Επιλογή: ")

        if choice == "1":
            full_name = input("Όνομα Πελάτη: ")
            phone = input("Τηλέφωνο: ")
            email = input("Email: ")
            address = input("Διεύθυνση Παράδοσης: ")

            valid, message = service.validate(full_name, phone, email, address)

            if not valid:
                print(message)
                continue

            customer = Customer(full_name, phone, email)
            order = service.save_order(customer, address)
            service.send_notification(order)

            print("Επιτυχής καταχώρηση!")
            print(order)

        elif choice == "2":
            for order in service.orders:
                print(order)

        elif choice == "0":
            print("Αντίο!")
            break

        else:
            print("Μη έγκυρη επιλογή.")


if __name__ == "__main__":
    main()
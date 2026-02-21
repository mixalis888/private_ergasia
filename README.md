# 📦 Σύστημα Καταχώρησης Παραγγελίας

## 🌐 Live Deployment

🔗 **Production URL:**
http://15.237.105.165/

---

# 1️⃣ Περιγραφή

Η παρούσα εργασία υλοποιεί το use case:

> **Καταχώρηση Παραγγελίας (με έλεγχο σφαλμάτων)**

Η εργασία αποτελεί συνέχεια της προηγούμενης ανάλυτικής εργασίας (UML), όπου σχεδιάστηκαν:

- Use Case Diagram
- Class Diagram
- Sequence Diagram

Στο παρόν repository γίνεται η μετάβαση:

**UML Ανάλυση → Python Υλοποίηση**

Σύμφωνα με τις οδηγίες της εκφώνησης.

---

# 2️⃣ Use Case Περιγραφή (από την αρχική εργασία)

![Use Case Description](use_case_description.png)

---

## 🔹 Use Case: Καταχώρηση Παραγγελίας

| Στοιχείο | Περιγραφή |
|----------|-----------|
| **Use Case - Τίτλος** | Καταχώρηση Παραγγελίας |
| **Σύντομη περιγραφή** | Το e-shop καταχωρεί την παραγγελία στο σύστημα |
| **Actors / Δρώντες** | e-shop |

### 🔸 Ροή / Βήματα (Happy Path)

| Βήματα / Tasks | Δεδομένα |
|----------------|----------|
| Το e-shop εισάγει τα στοιχεία της παραγγελίας | order_id, Clients_FullName, phone_number, email, DateOfOrder, Delivery_Address_Or_clever_point_code |
| Ο πελάτης λαμβάνει email/sms τον κωδικό παραγγελίας | Order_Confirmation_To_Client(order_id, phone_number, email) |

### 🔸 Εναλλακτική Ροή

| Ενέργεια | Δεδομένα |
|----------|----------|
| Ο πελάτης αλλάζει την τοποθεσία της παραγγελίας | Order_Modification(order_id, Delivery_Address_Or_clever_point_code) |
| Ο πελάτης ακυρώνει την παραγγελία | Order_Cancelation(order_id) |

---

# 3️⃣ Περιορισμένο Class Diagram

Το class diagram περιορίστηκε μόνο στις κλάσεις που συμμετέχουν στο συγκεκριμένο use case.

![Class Diagram](limited_class_diagram.png)

### Υλοποιούνται οι κλάσεις:

- `Customer`
- `Order`
- `EshopManager`

Σχέσεις:

- Κάθε `Order` συνδέεται με 1 `Customer`
- Ένας `EshopManager` μπορεί να καταχωρεί 0..* παραγγελίες

---

# 4️⃣ Sequence Diagram – Καταχώρηση Παραγγελίας

![Sequence Diagram](sequence.png)

## Αντιστοίχιση UML → Κώδικα

| UML Component | Υλοποίηση |
|---------------|-----------|
| UI | `main.py` (CLI) & `web_app.py` |
| Σύστημα | `OrderService` |
| Βάση Δεδομένων | in-memory list |
| Ειδοποιήσεις | `print()` simulation |
| validate(orderData) | `validate()` |
| saveOrder(orderData) | `save_order()` |
| sendNotification(orderID) | `send_notification()` |

Η ροή που υλοποιείται στον κώδικα είναι ακριβώς:

```text
submit → validate
↳ alt (invalid) → error
↳ valid → save → notify → success
```

---

# 5️⃣ Δομή Project

```text
private_ergasia/
│
├── erga sia/
│   ├── models.py
│   └── services.py
│
├── main.py
├── web_app.py
└── README.md
```

## Περιγραφή Αρχείων

- `models.py`
  - Domain classes (Customer, Order, EshopManager)

- `services.py`
  - Επιχειρησιακή λογική (validate, save, notify)

- `main.py`
  - CLI υλοποίηση use case

- `web_app.py`
  - Web version (deployment-ready)

---

# 6️⃣ Πώς τρέχω το πρόγραμμα

Προτεινόμενο: χρήση `uv run`.

## 🔹 CLI Version

```bash
uv run main.py
```

Εναλλακτικά (χωρίς uv):

```bash
python main.py
```

## 🔹 Web Version

```bash
uv run uvicorn web_app:app --reload
```

Εναλλακτικά (χωρίς uv, μέσα σε venv):

```bash
uvicorn web_app:app --reload
```

και άνοιγμα:

http://localhost:8000

ή χρήση production:

http://15.237.105.165/

Health check (production):

http://15.237.105.165/health

Health check (dev):

http://localhost:8000/health

---

# 7️⃣ Παράδειγμα Εκτέλεσης (CLI)

```text
===== Σύστημα Καταχώρησης Παραγγελίας =====
1. Νέα Παραγγελία
2. Προβολή Παραγγελιών
0. Έξοδος
Επιλογή: 1

Όνομα Πελάτη: Γιάννης Παπαδόπουλος
Τηλέφωνο: 6971234567
Email: giannis@email.gr
Διεύθυνση Παράδοσης: Αθήνα, Οδός 1

--- ΕΙΔΟΠΟΙΗΣΗ ---
Η παραγγελία ORD-0001 καταχωρήθηκε.
-------------------

Επιτυχής καταχώρηση!
```

---

# 8️⃣ Τεχνικές Πληροφορίες

- Python 3.10+
- Δεν χρησιμοποιείται εξωτερική βάση δεδομένων
- Αποθήκευση in-memory
- Προσομοίωση ειδοποιήσεων
- Το `main.py` εκτελεί το CLI εργαλείο
- Το `web_app.py` εκθέτει Web UI + API μέσω FastAPI/uvicorn
- Endpoint υπηρεσίας υγείας: `/health`

---

# 9️⃣ Σύνδεση με την Αρχική UML Εργασία

Η παρούσα υλοποίηση αποτελεί πρακτική εφαρμογή της ανάλυσης απαιτήσεων.

Από το συνολικό σύστημα (διανομές, οδηγοί, βάρδιες κ.λπ.) επιλέχθηκε και υλοποιήθηκε:

Ένα πλήρες, οριοθετημένο use case από άκρη σε άκρη.

Η μετάβαση έγινε ως εξής:

```text
Use Case Diagram
      ↓
Class Diagram
      ↓
Sequence Diagram
      ↓
Python Classes
      ↓
CLI / Web Implementation
```

Καλύπτεται πλήρως ο στόχος της εκφώνησης:

Σύνδεση UML ανάλυσης με λειτουργικό πρόγραμμα σε Python.

---

## 👥 Μέλη Ομάδας

- Βασιλική Καλαντζή - ΑΜ:25010
- Μιχάλης Λάζαρης – ΑΜ:25029

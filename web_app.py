from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ergasia.models import Customer
from ergasia.services import OrderService


app = FastAPI(title="Eshop Orders API")
service = OrderService()


class OrderCreateRequest(BaseModel):
    full_name: str
    phone: str
    email: str
    address: str


def order_to_dict(order):
    return {
        "order_id": order.order_id,
        "customer_name": order.customer.full_name,
        "phone": order.customer.phone,
        "email": order.customer.email,
        "delivery_address": order.delivery_address,
        "status": order.status,
        "date": order.date.isoformat(timespec="seconds"),
    }


@app.get("/", response_class=HTMLResponse)
def home_page():
    return """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Eshop Orders</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; max-width: 920px; }
      h1, h2 { margin-bottom: 0.75rem; }
      form { display: grid; gap: 0.75rem; margin-bottom: 1.25rem; }
      input, button { padding: 0.55rem; font-size: 0.95rem; }
      button { cursor: pointer; }
      .row { display: grid; gap: 0.75rem; grid-template-columns: 1fr 1fr; }
      table { width: 100%; border-collapse: collapse; }
      th, td { text-align: left; border: 1px solid #ddd; padding: 0.5rem; }
      .msg { margin: 0.75rem 0; min-height: 1.2rem; }
      @media (max-width: 640px) { .row { grid-template-columns: 1fr; } }
    </style>
  </head>
  <body>
    <h1>Order Registration</h1>
    <form id="order-form">
      <div class="row">
        <input id="full_name" placeholder="Full name" required />
        <input id="phone" placeholder="Phone" required />
      </div>
      <div class="row">
        <input id="email" type="email" placeholder="Email" required />
        <input id="address" placeholder="Delivery address" required />
      </div>
      <button type="submit">Create Order</button>
    </form>

    <div id="message" class="msg"></div>

    <h2>Orders</h2>
    <table>
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Customer</th>
          <th>Phone</th>
          <th>Email</th>
          <th>Address</th>
          <th>Status</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody id="orders-body"></tbody>
    </table>

    <script>
      const bodyEl = document.getElementById("orders-body");
      const msgEl = document.getElementById("message");
      const form = document.getElementById("order-form");

      function renderOrders(orders) {
        bodyEl.innerHTML = "";
        for (const order of orders) {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${order.order_id}</td>
            <td>${order.customer_name}</td>
            <td>${order.phone}</td>
            <td>${order.email}</td>
            <td>${order.delivery_address}</td>
            <td>${order.status}</td>
            <td>${order.date}</td>
          `;
          bodyEl.appendChild(row);
        }
      }

      async function fetchOrders() {
        const res = await fetch("/api/orders");
        const data = await res.json();
        renderOrders(data);
      }

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        msgEl.textContent = "";

        const payload = {
          full_name: document.getElementById("full_name").value,
          phone: document.getElementById("phone").value,
          email: document.getElementById("email").value,
          address: document.getElementById("address").value,
        };

        const res = await fetch("/api/orders", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!res.ok) {
          const err = await res.json();
          msgEl.textContent = err.detail || "Request failed.";
          return;
        }

        msgEl.textContent = "Order created successfully.";
        form.reset();
        await fetchOrders();
      });

      fetchOrders();
    </script>
  </body>
</html>
    """


@app.get("/api/orders")
def list_orders():
    return [order_to_dict(order) for order in service.orders]

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/orders", status_code=201)
def create_order(payload: OrderCreateRequest):
    valid, message = service.validate(
        payload.full_name,
        payload.phone,
        payload.email,
        payload.address,
    )

    if not valid:
        raise HTTPException(status_code=400, detail=message)

    customer = Customer(payload.full_name, payload.phone, payload.email)
    order = service.save_order(customer, payload.address)
    return order_to_dict(order)

# private_ergasia

Simple command-line order registration system for an e-shop.

## Overview

This project provides a small CLI application where a manager can:

- Create new customer orders
- Validate input fields (required fields, email format, phone digits)
- View all registered orders in memory
- Receive a terminal notification when an order is registered

## Requirements

- Python 3.13+
- One of the following package managers:
  - uv (recommended)
  - pip + venv

## Quick Start (uv)

1. Install dependencies and create environment:

	uv sync

2. Run the application:

	uv run main.py

3. Run the web app:

	uv run uvicorn web_app:app --reload

## Quick Start (pip)

1. Create virtual environment:

	python3 -m venv .venv

2. Activate it:

	source .venv/bin/activate

3. Run the application:

	python main.py

4. Run the web app:

	uvicorn web_app:app --reload

## How to Use

After launch, choose from the menu:

- 1: Create a new order
- 2: View all orders
- 0: Exit

For a new order, provide:

- Customer full name
- Phone
- Email
- Delivery address

If validation passes, the app generates an order ID in format ORD-0001, ORD-0002, etc.

## Web Interface & API

When the FastAPI server runs, open:

- http://127.0.0.1:8000 for the web page
- http://127.0.0.1:8000/docs for interactive API docs

Available endpoints:

- GET /api/orders: list all orders
- POST /api/orders: create a new order

## Deploy (Cheapest)

Recommended lowest-cost option: Vercel Hobby (typically free for personal projects; limits may change).

## Deploy on AWS EC2 (Current Production)

This project is currently deployed on an Ubuntu EC2 instance using `uvicorn` + `nginx` + `systemd`.

### 1) Launch EC2 instance

- AMI: Ubuntu 24.04 LTS
- Instance type: t3.micro
- Storage: 8 GiB
- Security Group inbound rules:
	- SSH (22) from your IP
	- HTTP (80) from 0.0.0.0/0

### 2) Connect to instance

```bash
chmod 400 /path/to/key.pem
ssh -i /path/to/key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 3) Install server dependencies

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx git
```

### 4) Clone and install app

```bash
git clone git@github.com:mixalis888/private_ergasia.git
cd private_ergasia
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt uvicorn
```

### 5) Create systemd service

Create `/etc/systemd/system/private-ergasia.service`:

```ini
[Unit]
Description=private_ergasia FastAPI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/private_ergasia
Environment="PATH=/home/ubuntu/private_ergasia/.venv/bin"
ExecStart=/home/ubuntu/private_ergasia/.venv/bin/uvicorn web_app:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable/start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now private-ergasia
```

### 6) Configure nginx reverse proxy

Create `/etc/nginx/sites-available/private-ergasia`:

```nginx
server {
	listen 80;
	server_name _;

	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

Enable and reload:

```bash
sudo ln -sf /etc/nginx/sites-available/private-ergasia /etc/nginx/sites-enabled/private-ergasia
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 7) Live endpoint

- Web app: http://15.237.105.165
- API: http://15.237.105.165/api/orders

### 8) Redeploy after pushing new code

After you push changes to `main`, redeploy on EC2 from your local machine.

Full redeploy (includes dependency sync):

```bash
ssh -i /Users/michalis/Downloads/ergasia.pem ubuntu@15.237.105.165 \
	'cd ~/private_ergasia && \
	 git pull --ff-only && \
	 source .venv/bin/activate && \
	 pip install -r requirements.txt && \
	 sudo systemctl restart private-ergasia && \
	 sudo systemctl status private-ergasia --no-pager -l | head -n 20'
```

Quick redeploy (code-only changes, no new dependencies):

```bash
ssh -i /Users/michalis/Downloads/ergasia.pem ubuntu@15.237.105.165 \
	'cd ~/private_ergasia && git pull --ff-only && sudo systemctl restart private-ergasia'
```

Health check:

```bash
curl -sS http://15.237.105.165/api/orders
```

### Option A: Deploy from GitHub (no CLI needed)

1. Open Vercel and import repository `mixalis888/private_ergasia`
2. Framework preset: Other
3. Leave build settings as default (project includes `vercel.json`)
4. Deploy

### Option B: Deploy with Vercel CLI

1. Install CLI:

	npm i -g vercel

2. Login and deploy from project folder:

	vercel

3. Promote to production:

	vercel --prod

### Important note

Current app stores orders in memory, so serverless instances will not persist data between cold starts/redeploys.
For persistent storage, next step is adding a small database (e.g., SQLite/Postgres).

## Project Structure

- main.py: Application entry point and CLI loop
- web_app.py: FastAPI app with page route and API routes
- ergasia/models.py: Domain models (Customer, EshopManager, Order)
- ergasia/services.py: Business logic (validation, save order, notifications)
- pyproject.toml: Project metadata and dependency configuration
- requirements.txt: Deployment dependencies for Vercel Python runtime
- vercel.json: Vercel build and route configuration

## Notes

- Orders are stored in memory only (not persisted to a database).
- No external dependencies are currently required.


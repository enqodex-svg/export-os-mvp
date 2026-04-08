# Export OS MVP (India → UAE) — Export Enablement Platform

This repository contains a **production-grade MVP skeleton** for an **Export Enablement Platform (Export OS)** focused on enabling a first-time Indian SME exporter to:

> **List a product → Get quotes → Book shipment → Auto-generate documents → Track shipment → Get paid**

**Corridor:** India → UAE  
**Category:** Handicrafts / Home Décor / Textiles

---

## What's included

### Backend (FastAPI)
- OTP login (mocked OTP: `123456`)
- Product listing (with HS code suggestion)
- Export readiness score
- Shipping quotes + booking (mock courier integrator)
- Document generation (PDFs: invoice, packing list, label)
- Tracking timeline (mock tracking engine)
- Payments (mock payment link + FX transparency)
- WhatsApp notifications (mock logger with architecture hooks)

### Frontend
- Minimal PWA placeholder (kept intentionally light for MVP)
- Offline product draft storage design notes

### DevOps
- Docker Compose (Postgres + Backend)
- GitHub Actions CI (lint + tests)

---

## Quickstart (local)

> **Prereqs**: Python 3.11+, Docker (optional)

### Option A — Run with Docker (recommended)

```bash
cd backend
docker compose up --build
```

Backend will start on: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

### Option B — Run backend locally (SQLite)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## What is real vs mocked?

✅ Real in MVP:
- Data model + persistence
- End-to-end flow APIs
- PDF generation
- Readiness scoring

🧪 Mocked (swappable adapters):
- OTP delivery
- Courier API integrations
- WhatsApp messaging
- Payment gateway
- FX rates

---

## How to push to GitHub

I cannot create the GitHub repo directly from here (no GitHub network access), but you can push this project in minutes:

```bash
git init
git add .
git commit -m "Initial Export OS MVP skeleton"

# Create a new repo on GitHub called export-os-mvp, then:
git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```

---

## Next steps to production

- Replace mock courier service with Aramex/DHL integration using the same `CourierAdapter` interface.
- Replace mock payments with Razorpay/Stripe/Payoneer.
- Add real WhatsApp via Meta Cloud API.
- Add background jobs (Celery/RQ) for retries + webhook handling.
- Add audit trails + role-based access.

---

## License
MIT (see LICENSE).

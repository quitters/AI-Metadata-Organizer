# AI Image Manager WebApp

A full-stack application for uploading images and extracting AI-generated metadata, featuring a modern Next.js frontend and a FastAPI backend.

---

## Features
- Upload images and extract AI metadata (Midjourney, etc)
- Light/Dark mode toggle
- Responsive, accessible UI
- FastAPI backend for metadata extraction

---

## Local Development

### 1. Frontend (Next.js)
```bash
cd webapp-image-manager
npm install
npm run dev
```
Visit [http://localhost:3000](http://localhost:3000) to use the app.

### 2. Backend (FastAPI)
```bash
cd webapp-image-manager
pip install -r requirements.txt
python -m uvicorn src.app.api.extract-metadata:app --reload --port 8000
```
The backend will be available at [http://localhost:8000](http://localhost:8000).

---

## Deployment

### Frontend (Vercel)
- Deploy this directory to Vercel as a Next.js app (no extra config needed).

### Backend (FastAPI)
- **Vercel does NOT natively support FastAPI/Python backends.**
- Deploy your FastAPI backend to a Python-friendly host (e.g. [Render](https://render.com), [Railway](https://railway.app), [Fly.io](https://fly.io)).
- Update your frontend API URL to point to the deployed backend (not localhost).

---

## Environment Variables
- If you use environment variables, add them to `.env.local` (for Next.js) and `.env` (for FastAPI), and ensure they are listed in `.gitignore`.

---

## Notes
- `.gitignore` is set up for Node.js, Next.js, and Python.
- Both frontend and backend code are in this directory for convenience, but only the frontend will run on Vercel.
- For production, you must deploy the backend separately and configure the frontend to use the correct API URL.

---

## License
MIT

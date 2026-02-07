# Hamdard Library

## About Hamdard Library

**Hamdard Library** is an open-source project aimed at providing students of **Jamia Hamdard** with a simple and reliable platform to share academic resources such as notes, lab files, and study material.

The project focuses on eliminating the friction of repeatedly requesting files over messaging platforms like WhatsApp by providing a centralized, persistent, and searchable repository of resources.

---

## Goals

- Centralized resource sharing for students
- Easy uploads and downloads of notes and lab files
- Department- and semester-based organization
- Long-term availability of shared resources
- Secure and abuse-resistant system design

---

## Key Features

- 📁 **File uploads with hashing** (duplicate file prevention)
- ⏱️ **Rate limiting** on uploads to prevent spam/abuse
- 🔐 **Secure file access** using signed URLs
- 🧾 **Approval workflow** for uploaded resources
- 📊 **Download tracking**
- 🔑 **Authentication & authorization**
- 🌐 **Server-side rendered frontend**
- 🔌 **REST API support** using Django REST Framework (DRF)

---

## Tech Stack

### Backend
- **Django** (core framework)
- **Django REST Framework (DRF)** for APIs
- **PostgreSQL** (hosted on Neon)
- **Gunicorn** (production WSGI server)

### Storage
- **Cloudinary** for file storage (PDFs and documents)
- File hashing (SHA-256) for deduplication

### Frontend
- **Django Templates (SSR)**
- **Bootstrap** for styling
- Custom CSS & JavaScript

### Infrastructure
- **Neon** – serverless PostgreSQL
- **Cloudinary** – cloud file storage
- **WhiteNoise** – static file serving
- **Rate limiting** via middleware/decorators
- **Environment-based configuration**

---

## Project Structure Highlights

- `library/` – core app (models, views, templates)
- `user/` – authentication and user management
- `static/` – custom CSS & JavaScript
- `templates/` – server-rendered HTML
- REST APIs exposed alongside SSR views

---
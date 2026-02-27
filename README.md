# 🚀 DevOps Project Setup

## 1. Clone Project

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

## 2. Setup Virtual Environment

### Linux / macOS

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

---

## 4. Create Environment File

### Linux / macOS

```bash
cp .env.example .env
```

### Windows

```bash
copy .env.example .env
```

Edit the `.env` file and configure your environment variables.

---

## 5. Start Docker Services

```bash
docker compose -f docker-compose.dev.yml up -d
```

Check running containers:

```bash
docker ps
```

---

## 6. Run Database Migrations

```bash
python manage.py migrate
```

---

## 7. Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Project will be available at:

```
http://127.0.0.1:8000
```
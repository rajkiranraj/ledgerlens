# Deployment Guide

## Frontend Deployment

### Vercel
1. Push your code to GitHub
2. Import the repo into Vercel
3. Set the build directory to `frontend/my-app/dist`
4. Set the root directory to `frontend/my-app`
5. Deploy

### Netlify
1. Push your code to GitHub
2. Import the repo into Netlify
3. Set build command: `npm run build`
4. Set publish directory: `frontend/my-app/dist`
5. Deploy

## Backend Deployment

### Heroku
1. Install Heroku CLI
2. Log in with `heroku login`
3. Create a new app: `heroku create your-app-name`
4. Add a PostgreSQL addon (or use SQLite for small deployments)
5. Set environment variables in Heroku dashboard:
   - `NVIDIA_NIM_API_KEY` (optional)
6. Push your code: `git push heroku main`
7. Run migrations: `heroku run python manage.py migrate`
8. Seed data: `heroku run python manage.py shell < seed_data.py`

### Docker
Create a Dockerfile for your backend and frontend, then deploy using Docker Compose or a container orchestration service.

## Database Configuration

### SQLite (Default)
No additional configuration needed for local development or small deployments.

### PostgreSQL
1. Install PostgreSQL
2. Create a database and user
3. Update backend/config/settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
4. Install psycopg2: `pip install psycopg2-binary`

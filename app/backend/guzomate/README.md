**Docker Setup**

Prerequisites:
 - Docker

Steps: 
```bash
 - cd backend/guzomate
```
Build the Docker image:
```bash
 - docker build -t guzomate .
```
Run the container:
```bash
 - docker run -p 8000:8000 guzomate
 - docker run -p 8000:8000 guzomate python manage.py migrate
```

## After u run it using: http://127.0.0.1:8000
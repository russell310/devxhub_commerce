# DEVXHUB COMMERCE

## Requirements
- Python: 3.12
- Django: 5.x
- Docker
- Docker Compose
- Stripe

## Installation
1. Clone the repository:
```sh
git clone git@github.com:russell310/devxhub_commerce.git
cd devxhub_commerce
```
2. Create `.env`
```sh
cp .env.example .env
```
3. Build and start the container
```sh
docker-compose up --build
```
4. Access the Application
```sh
http://localhost:8000/api/
```
We have 2 types of users: admins and regular users (employees)

## Prerequisites:
- Docker running & docker compose installed. Check: `docker-compose --version` & `service docker status`

## Instructions:


if rabbitmq fails to start:  
`sudo lsof -i :5672`  
`kill -9 <PID>`  

0. start postgres `docker run --name postgres -e POSTGRES_PASSWORD=postgres -d -p 5555:5432 postgres`
1. login to db: `psql -h 127.0.0.1 -p 5555 -U postgres`
2. create db: `CREATE DATABASE company_tasks;`
3. start rabbitmq running on default port `docker run -d -p 5672:5672 rabbitmq`
4. activate virtual env: `source ./venv/bin/activate`
5. install requirements: `pip install -r pip_requirements.txt`
6. start celery worker & scheduler `celery -A company_tasks worker -l info -B`
7. migrate: `python manage.py migrate`
8. run server: `python manage.py runserver`
9. create admin user so u can create employees and assign tasks `python manage.py createsuperuser`

### admin can:
- do everything with users
- do everything with tasks

### user can:
- list his tasks
- mark task as done / undone

## todo
- tests
- dockerize

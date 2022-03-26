We have 2 types of users: admins and regular users (employees)

## Instructions:
1. start rabbitmq running on default port `docker run -d -p 5672:5672 rabbitmq`
2. start celery worker `celery -A company_tasks worker -l info`
3. activate virtual env: `source ./venv/bin/activate`
4. install requirements: `pip install -r pip_requirements.txt`
5. migrate: `python manage.py migrate`
6. run server: `python manage.py runserver`
7. create admin user so u can create employees and assign tasks `python manage.py createsuperuser`

### admin can:
- do everything with users
- do everything with tasks

### user can:
- list his tasks
- mark task as done / undone

## todo
- schedule mails
- use postgres
- dockerize?
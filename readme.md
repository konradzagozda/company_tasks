We have 2 types of users: admins and regular users (employees)

## Prerequisites:
- Docker running & docker compose installed. Check: `docker-compose --version`

## Instructions:
- run `docker-compose up`
- go to `http://0.0.0.0:8000/api/` or `http://127.0.0.1:8000/api/`
- sign in with credentials: `admin/admin`, create users and create some tasks for them


### admin can:
- do everything with users
- do everything with tasks

### user can:
- list his tasks
- mark task as done / undone


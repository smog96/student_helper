### Migrations

+ create migration

```bash
$ alembic revision --autogenerate -m <msg>
```

+ migrate migrations to db

```bash
$ alembic upgrade head
```
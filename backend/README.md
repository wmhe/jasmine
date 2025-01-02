```bash
poetry run flask run --port 5001 --debug
```

```bash
poetry run flask db init
poetry run flask db migrate
poetry run flask db upgrade
```

```bash
poetry run aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```

```bash
poetry run python tests.py
```

```bash
curl -X POST -u [user:password] http://localhost:5001/api/v1/tokens 

curl -H "Authorization: bearer [token]" http://localhost:5001/api/v1/users
```
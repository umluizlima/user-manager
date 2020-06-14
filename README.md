# user-manager
A service to manage user information and authentication.

## Development

### Requirements
- [Python 3.8.1](https://realpython.com/intro-to-pyenv/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installing
Install dependencies
```console
make install
```

### Testing
```console
make test
```

### Running
Access the API documentation on http://localhost:8000/docs
```console
make run
```

### Migrating
Generate migration files automatically for changes to models. Make sure all models are imported on `models/__init__.py`
```console
make db_generate_migration description="your description"
```

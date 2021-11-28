# user-manager
A service to manage user information and authentication.

## Development

### Requirements
- [Python 3.10.0](https://realpython.com/intro-to-pyenv/)
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
Access the API documentation on http://localhost:8001/docs
```console
make run
```

### Migrating
Generate migration files automatically for changes to models. Make sure all models are imported on `models/__init__.py`
```console
make db_generate_migration description="your description"
```

## Deployment

### Heroku

The `app.json`, `Procfile`, and `runtime.txt` files on this repository are specific for deployment on [Heroku](https://www.heroku.com). It can be done by clicking the following button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

The CloudAMQP add-on must be shared between this service and [email-sender](https://github.com/umluizlima/email-sender) to ensure that the access code transactional gets sent.

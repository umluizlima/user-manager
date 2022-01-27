# user-manager
A service to manage user information and authentication.

## Development

### Requirements
- [Python 3.10.0](https://realpython.com/intro-to-pyenv/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installing
Install dependencies
```bash
make install
```

### Testing
```bash
make test
```

### Running
Run the following commands to create a [private/public key pair](https://cryptotools.net/rsagen). It's required for encoding and decoding the JWT tokens:

```bash
openssl genrsa -out private.pem
openssl rsa -in private.pem -pubout -out public.pem
```

Then, create a `.env` file and place the keys there. It should look like this:

```bash
JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAK..."
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
MIIBIjAN..."
```

After that you should be good to go:

```bash
make run
```

Access the API documentation on http://localhost:8001/docs

### Migrating
Generate migration files automatically for changes to models. Make sure all models are imported on `models/__init__.py`

```bash
make db_generate_migration description="your description"
```

## Deployment

### Heroku

The `app.json`, `Procfile`, and `runtime.txt` files on this repository are specific for deployment on [Heroku](https://www.heroku.com). It can be done by clicking the following button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

The CloudAMQP add-on must be shared between this service and [email-sender](https://github.com/umluizlima/email-sender) to ensure that the access code transactional gets sent.

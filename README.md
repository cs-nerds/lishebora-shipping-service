# lishebora-shipping-service

Lishe bora microservice for shipping products

### Quickstart[docker & docker-compose]

After cloning the repo and cd into the main dir with `docker-compose.yml` file,

1. Run `cat sample.env > .env`
1. Run `docker-compose build`
1. Run `docker-compose up -d`
1. Open http://localhost:4501/docs in you defaul browser to view api documentation

## Development

- To check linting of code run: `docker-compose exec backend scripts/lint.sh`
- To format your code run: `docker-compose exec backend scripts/format.sh`
- To make migration files run: `docker-compose exec backend alembic revision --autogenerate -m "your message"`
- To run migration files: `docker-compose exec backend alembic upgrade head`
- To run tests: `docker-compose exec backend scripts/test.sh`

### Quickstart[docker and kubernetes kubectl]

After cloning the repo and cd into the main dir with `docker-compose.yml` file,

1. Run `bash k8s-node-start.sh`

To access the app, use the External IP defined in the service or localhost and the external port.

# lishebora-shipping-service

Lishe bora microservice for shipping products

### Quickstart[docker & docker-compose]

After cloning the repo and cd into the main dir with `docker-compose.yml` file,

1. Run `cat sample.env > .env`
1. Run `docker-compose build`
1. Run `docker-compose up -d`
1. Open http://localhost:4501/docs in you defaul browser to view api documentation

### Quickstart[docker and kubernetes kubectl]

After cloning the repo and cd into the main dir with `docker-compose.yml` file,

1. Run `bash k8s-node-start.sh`

To access the app, use the External IP defined in the service or localhost and the external port.

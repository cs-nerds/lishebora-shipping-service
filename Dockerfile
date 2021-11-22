FROM python:3.8 as api 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements /app/shipping/requirements

RUN python3 -m pip install --upgrade pip

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN pip install -r /app/shipping/requirements/prod.txt

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r /app/shipping/requirements/dev.txt ; fi"

COPY ./ /app/shipping
WORKDIR /app/shipping/app

ENV PYTHONPATH=/app/shipping/app

EXPOSE 80

CMD ["bash", "scripts/start-app.sh"]


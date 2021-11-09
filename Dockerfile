FROM python:3.8 as api 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./ /app

WORKDIR /app

RUN python3 -m pip install --upgrade pip

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN pip install -r requirements/prod.txt

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r requirements/dev.txt ; fi"

ENV PYTHONPATH=/app


FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ARG ALLOWED_HOSTS
ENV ALLOWED_HOSTS $ALLOWED_HOSTS

ARG GMAIL_ID
ENV GMAIL_ID $GMAIL_ID

ARG GMAIL_PW
ENV GMAIL_PW $GMAIL_PW

ARG EMAIL_PAGE_DOMAIN
ENV EMAIL_PAGE_DOMAIN $EMAIL_PAGE_DOMAIN

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

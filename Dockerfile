FROM python:3.11.0-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code/
WORKDIR /code/

# install dependencies
RUN python -m pip install --upgrade pip
ADD requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /code/
# RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "-c", "./gunicorn/conf.py", "--bind", ":8000", "--chdir", "hh", "hh.wsgi:application"]
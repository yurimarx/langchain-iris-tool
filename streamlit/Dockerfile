FROM python:3.9

WORKDIR /usr/src/app

# dont write pyc files
# dont buffer to stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./streamlit/hello.py hello.py
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./src/python/rag /usr/src/app/

# dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./ /usr/src/app

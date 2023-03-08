FROM python:3.11-slim

COPY requirements.txt /tmp/pip-tmp/

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

ENV PYTHONPATH=/app

RUN adduser seeder
USER seeder

CMD ["python", "app/seeder.py"]
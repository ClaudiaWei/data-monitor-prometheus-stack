# builder image
FROM python:3.9-slim-buster as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# container image
FROM python:3.9-slim-buster
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY bq_sql bq_sql
COPY ds ds
COPY main.py main.py
COPY bq_template.py bq_template.py
COPY ds_template.py ds_template.py
EXPOSE 8000
ENTRYPOINT [ "python3" ]
CMD [ "/app/main.py" ]

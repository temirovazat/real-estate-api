FROM python:3.9

ENV PATH="${PATH}:/root/.poetry/bin"

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-interaction --no-dev --no-root --no-ansi -vvv

ENV PYTHONPATH=/app

WORKDIR /app

COPY . .
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh && \
    ln -s ./entrypoint.sh /

EXPOSE 8080

ENTRYPOINT ["sh", "./entrypoint.sh"]

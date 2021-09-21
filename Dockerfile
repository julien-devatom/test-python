FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src .

RUN chmod +x run.sh
CMD ["sh", "run.sh"]
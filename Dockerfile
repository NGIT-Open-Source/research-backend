FROM python:3.10.2-alpine3.15

COPY ./req.txt /app/req.txt

WORKDIR /app

RUN pip install -r req.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]


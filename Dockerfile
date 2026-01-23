FROM python:3.14-slim

WORKDIR /app

RUN pip install pandas
RUN pip install flask
RUN pip install flask-cors
RUN pip install yfinance
RUN pip install requests

COPY price.py .
COPY amounts.py .
COPY api.py .

RUN mkdir /data

CMD ["python", "api.py"]
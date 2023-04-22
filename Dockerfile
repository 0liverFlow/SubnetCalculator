FROM python:3.10
LABEL author="0liverFlow"

WORKDIR /app

COPY . /app 

RUN pip install -r requirements.txt

ENTRYPOINT ["python3.10", "./SubnetCalculator.py"]
 

FROM python:3.7.2

WORKDIR /app

RUN apt-get update && apt-get -y --force-yes install libgeos-c1v5 libgeos-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -rf .env

RUN pip install .

CMD [ "python", "-m", "aegir", "runserver"]

# syntax=docker/dockerfile:1
FROM python:3

# installe les dépendances externes
WORKDIR /scraper-discours
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# volume ou seront stockés logs et output
VOLUME /data

# copie le code dans le conteneur
COPY . .

# lance l'extraction
CMD ["python", "extract.py"]

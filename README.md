<div align="center" id="top"> 


  <!-- <a href="https://{{app_url}}.netlify.app">Demo</a> -->
</div>

<h1 align="center">scraper-vie-publique</h1>

<br>

## :dart: A propos ##

Ce projet est un scraper qui récupère et nettoie (un peu) l'ensemble des discours présents sur vie-publique.fr. 

"La Collection des discours publics rassemble près de 140 000 discours prononcés par les principaux acteurs de la vie publique française : discours du président de la République depuis 1974, du Premier ministre et des membres du gouvernement depuis le début des années 1980, communiqués du Conseil des ministres depuis 1974, etc..."

Le code est extrait et adapté depuis les travaux d'un partenaire de Datapolitics : [Mazancourt Conseil](https://mazancourtconseil.wordpress.com/2021/09/08/scraper-les-discours-politiques/) (merci à eux !)

## :white_check_mark: Requirements ##

- Python 3.7+
- Docker et un compte hub.docker.com (si vous souhaitez utiliser Docker)

## Output ##

Le projet génère 2 fichiers Json : 
1. all_discours.json contient l'ensemble des données des discours
2. all_discours_metadata.json contient uniquement les metadonnées des discours (pas le texte du discours lui-même)

Les champs récupérés sont :
- _url_: l'url du discours sur vie-publique.fr
- _title_: le titre du discours
- _raw_text_: le texte du discours
- _circumstance_ : les circonstances dans lesquelles le discours a été prononcé (par ex : déplacement du président de la république en Allemagne)
- _date_: la date du discours
- _what_keywords_: un ensemble de mots clés qui décrivent le sujet du discours, le "what"
- _who_keywords_: un ensemble de mots clés qui décrivent le ou les intervenant  discours, le "who" 
- _desc_: une courte description du discours

## Utilisation ##

Le projet peut être utilisé de 2 manières différentes : 
1. Dans un environnement python virtuel
2. Dans un conteneur Docker (recommandé pour un déploiement facilité sur un serveur)

### 1. Utilisation dans un environnement python virtuel ###

```
virtualenv venv
source venv/bin/activate
pip install requirements.txt
python extract.py
```

A la fin du scraping, les fichiers seront disponibles dans le dossier data/

### 2. Utilisation dans un conteneur docker (recommandé pour un déploiement facilité sur un serveur) ###

```
docker volume create scraper-discours-data # volume dans lequel on va stocker le résultat
docker build . -t scraper-discours
docker run --mount source=scraper-discours-data,target=/scraper-discours/data scraper-discours
```

Le résultat et les logs seront ensuite disponible dans le volume scraper-discours-data. [Plus d'infos sur les volumes](scraper-discours).

## Points d'attentions ##

Il arrive parfois que malgré toutes les précautions prises que le web service de vie-publique.fr renvoie une erreur.
Cette erreur, si elle se produit plusieurs fois, peut mettre fin au scrapping. 
Nous recommandons d'aller consulter le fichier de logs _logs-extract.log_ pour vérifier qu'il s'agit bien d'une erreur HTTP 500. 

Dans ce cas, pour pouvez relancer le scrapper à partir de l'URL en échec. 
La variable d'environnement suivante est prévue pour cela et peut être passée lors du Docker run.

```
docker run --mount source=scraper-discours-data,target=/scraper-discours/data -e START_URL=https://www.vie-publique.fr/discours?page=5766 scraper-discours
```


## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.

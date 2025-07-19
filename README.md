# PROJET IA2 - Système de Détection et Dashboard

## Présentation générale
Ce projet est un système complet de détection faciale avec enregistrement des passages et visualisation des statistiques via un dashboard web moderne.

Il se compose de trois parties principales :
- **app1.py** : script Python de détection faciale en temps réel (indépendant du frontend)
- **api.py** : API Flask qui expose les données de la base MySQL au frontend
- **project_ia2/** : application React pour l'affichage du dashboard et des statistiques


## 1. Script de détection : `app1.py`
- **But** :
  - Se connecte à une webcam
  - Détecte et reconnaît les visages en temps réel
  - Enregistre chaque passage (nom, date/heure) dans la base MySQL `detections_db`
- **Important** :
  - Ce script **n'est pas inclus ni exécuté dans l'application React**
  - Il fonctionne indépendamment et alimente la base de données utilisée par le dashboard
- **Lancement** :
  ```bash
  python app1.py
  ```


## 2. API Flask : `api.py`
- **But** :
  - Sert d'interface entre la base MySQL et le frontend React
  - Expose une route `/api/detections` qui retourne les passages enregistrés (nom, date/heure)
- **Lancement** :
  ```bash
  pip install flask flask-cors mysql-connector-python
  python api.py
  ```
- **À lancer en parallèle du frontend React**


## 3. Frontend React : `project_ia2/`
- **But** :
  - Affiche un dashboard moderne avec statistiques, filtres, et tableau des passages
  - Récupère les données en temps réel via l'API Flask
- **Lancement** :
  ```bash
  cd project_ia2
  npm install
  npm start
  ```
- **Accès** :
  - Ouvrir [http://localhost:3000](http://localhost:3000) dans un navigateur


## Dépendances principales
- Python : `opencv-python`, `face_recognition`, `deepface`, `pygame`, `flask`, `flask-cors`, `mysql-connector-python`
- Node.js/React : `react`, `react-chartjs-2`, `chart.js`
- Base de données : MySQL (ou MariaDB)


## Schéma de fonctionnement global

[Webcam] --(app1.py)--> [Base MySQL] <--(api.py)--> [React Dashboard]
```
- `app1.py` détecte et enregistre les passages dans la base
- `api.py` expose les données à React
- Le dashboard React affiche et filtre les données en temps réel


## Remarques
- Le script `app1.py` doit tourner pour alimenter la base, mais il n'est pas lié techniquement à l'application React.
- L'API Flask (`api.py`) doit être lancée pour que le dashboard fonctionne.
- Vous pouvez adapter la configuration MySQL (utilisateur, mot de passe, port) selon votre environnement.


## Auteur
- CHOUPO MALIEDJE MAEVA

NB: Reinstallez le dossier node_modules dans le sous dossier project_ia2 avec la commande 'npm install' , pour pouvoir lancer l'app

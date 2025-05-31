# Traitement d'images avec interface graphique

Cette application permet de traiter des images à partir d'une interface graphique moderne et modulaire, inspirée du style Apple.

## Fonctionnalités
- Interface graphique construite avec `ttkbootstrap` pour un style moderne
- Architecture modulaire avec séparation claire : interface (`gui/`), logique (`core/`), config
- Nettoyage automatique des noms de fichiers (accents, espaces, caractères spéciaux)
- Gestion des doublons (ajout _1, _2... si nécessaire)
- Application de traitements image avec `Pillow`
- Résultats nommés selon le format : `processed_<outil>_<nomimage>.jpg`
- Mémoire du dernier dossier d’entrée et de sortie pendant la session
- Option d'ouverture automatique du dossier après traitement

## Structure du projet
```
traitement_images_ui/
├── gui/
│   └── app.py                 # Interface utilisateur (ttkbootstrap)
├── core/
│   ├── utils.py              # Nettoyage, validation, copie des fichiers
│   ├── traitement.py         # Fonctions de traitement d'image
│   └── config.py             # Constantes et configuration centrale
├── input/                    # Dossier temporaire nettoyé à chaque traitement
├── main.py                   # Point d'entrée unique de l'application
├── requirements.txt
└── README.md
```

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer les tests unitaires
```bash
pytest
```

## Utilisation
```bash
python main.py
```

## Étapes dans l'application
1. **Sélectionner les images** à traiter
2. **Choisir le dossier de destination** pour les images traitées
3. **Sélectionner un traitement** (grayscale, rotation, etc.)
4. **Lancer le traitement**

## Traitements disponibles
- Niveau de gris
- Rotation 90°
- Redimensionnement à 50%
- Inversion des couleurs
- Flou léger

## Remarques
- Le dossier `input/` est recréé à chaque session et sert de tampon pour les fichiers nettoyés.
- Le projet est conçu pour évoluer facilement : il est possible d'ajouter de nouveaux traitements ou interfaces sans casser la logique centrale.
- Des tests unitaires automatiques sont en place pour `core/utils.py` avec `pytest` (voir dossier `tests/`).

## À venir (facultatif)
- Ajout d’un fichier `.config.json` pour conserver les préférences entre sessions
- Mode sombre / clair automatique selon l'OS
- Tests unitaires pour `core/utils.py` (déjà en place)

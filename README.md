# Traitement d'images avec interface graphique

Cette mini-application permet de traiter des images depuis une interface graphique minimaliste.

## Fonctionnalités
- Interface Tkinter simple (liste déroulante + bouton de sélection)
- Nettoyage automatique des noms de fichiers (accents, espaces, caractères spéciaux)
- Gestion des doublons (ajout _1, _2... si nécessaire)
- Application de traitements image avec `Pillow`
- Résultats nommés selon le format : `processed_<outil>_<nomimage>.jpg`

## Structure du projet
```
traitement_images_ui/
├── main.py
├── utils.py
├── traitement.py
├── requirements.txt
├── README.md
├── input/ # temporaire (vidé à chaque traitement)
└── output/ # images traitées
```

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation
```bash
python main.py
```
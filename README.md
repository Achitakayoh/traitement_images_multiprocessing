# Traitement d'images avec interface graphique

Cette mini-application permet de traiter des images depuis une interface graphique épurée.

## Fonctionnalités
- Interface Tkinter organisée en étapes claires
- Nettoyage automatique des noms de fichiers (accents, espaces, caractères spéciaux)
- Gestion des doublons (ajout _1, _2... si nécessaire)
- Application de traitements image avec `Pillow`
- Résultats nommés selon le format : `processed_<outil>_<nomimage>.jpg`
- Mémoire du dernier dossier d’entrée et de sortie utilisé pendant la session
- Option d'ouverture automatique du dossier une fois le traitement terminé

## Structure du projet
```
traitement_images_ui/
├── main.py                # Interface utilisateur
├── utils.py               # Nettoyage des noms et gestion des fichiers
├── traitement.py          # Fonctions de transformation des images
├── requirements.txt
├── README.md
├── input/                 # Temporaire (vidé automatiquement à chaque traitement)
└── (destination personnalisée sélectionnée à chaque fois)
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

## Étapes d'utilisation dans l'application
1. **Sélectionnez les images à traiter** via un bouton de navigation
2. **Choisissez le dossier de destination** où les images seront enregistrées
3. **Sélectionnez le traitement** à appliquer (grayscale, rotation, etc.)
4. Cliquez sur **Lancer le traitement**

L’application affiche des résumés dynamiques (ex. : "3 fichier(s) : image1.jpg, image2.jpg, ...") et propose d’ouvrir le dossier de sortie automatiquement après traitement.

## Remarques
- Les fichiers traités sont toujours enregistrés dans le dossier sélectionné par l'utilisateur.
- Les fichiers temporaires nettoyés sont stockés dans le dossier `input/`, vidé à chaque lancement.
- Pour l’instant, la mémoire des derniers chemins est maintenue pendant la session uniquement.

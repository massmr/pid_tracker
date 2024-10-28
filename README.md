# pid_tracker
Project Beta Adimaker 24/25 "pointeur rouge".

# Présentation

## Introduction
Le projet "pointeur rouge" a été réalisé dans le cadre de nos études.\
Le projet s'inscrit dans le domaine de la robotique et de la computer vision.\
Le but est de créer un pointeur laser qui puisse tracker un objet de notre choix
de manière autonome.\
L'objet à tracker est laissé libre afin que nous puissions explorer les
différentes solutions de computer vision.

## Objectifs
Domaine : robotique - computer vision\
But : tracker laser autonome\
Objet à traquer : au choix de l'équipe\
Décision de l'équipe : zone du corps - main ou tête : à adapter selon algorithme
de computer vision\

## Contraintes
Budget limite : 150€\

# Hardware et matériel

## Hardware
Système : Raspberry Pi 3, 4.\
OS : Raspbery Pi OS.

## Matériel
Motorisation : 2* servos 9g\
Laser : diode laser\
Caméra : Pi caméra V2\
Articulation : Pan-tilt impression\

# Software

## Prérequis
- Python 3\

## Bibliothèques nécessaires
- `imutils`\
- `opencv-python`\
 
```bash
pip install imutils opencv-python
```

## Arborescence du repository
```bash
├── README.md
├── haarcascade_frontalface_default.xml
├── pan_tilt_tracking.py
└── pyImageSearch
    ├── __init__.py
    ├── __pycache__
    ├── objCenter.py
    └── pid.py
```

## Description des fichiers

### haarcascade_frontalface_default.xml - Algorithme de détection des visages
#### Description
`haarcascade_frontalface_default.xml` contient les paramètres d'un classificateur en cascade Haar spécialement entraîné pour la détection de visages dans des images. Il fait partie des outils d'OpenCV pour la vision par ordinateur et repose sur les caractéristiques Haar : des motifs de luminosité permettant de détecter des formes distinctes (comme les yeux, le nez et la bouche) dans une région.
Description Technique

#### Avantages
Détection rapide et efficace : la cascade de Haar est optimisée pour être rapide, en passant par une série de filtres de plus en plus précis.

#### Limites
Ce modèle est sensible à l’orientation et à l'éclairage, ce qui signifie qu’il peut être moins efficace si les visages sont inclinés ou mal éclairés.

#### Fonctionnement
Chaque niveau du classificateur vérifie si une région de l’image présente des caractéristiques de visage, filtrant successivement les zones jusqu’à isoler le visage.

#### Utilisation
Ce fichier est chargé dans OpenCV pour initialiser un détecteur de visages, et il peut ensuite être appliqué sur chaque image ou image vidéo pour détecter des visages en temps réel.

#### Documentation
https://docs.opencv.org/3.4/d2/d99/tutorial_js_face_detection.html

### objCenter.py - Détection de Visages avec OpenCV
#### Description
`ObjCenter` est une classe Python conçue pour détecter des visages dans des images à l'aide de la bibliothèque OpenCV. Elle utilise un classificateur en cascade Haar pour identifier les visages et peut retourner les coordonnées du centre du visage détecté.

### pid.py - Régulateur PID "Proportionnel Intégral Dérivé"
#### Description

#### Ressources utiles
https://fr.wikipedia.org/wiki/R%C3%A9gulateur_PID

### pan_tilt_tracking.pyImageSearch
#### Description
Lorem Ipsum

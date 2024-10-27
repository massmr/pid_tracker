# pid_tracker
Project Beta Adimaker 24/25


## Arborescence des Fichiers
projet/ ├── README.md # Ce fichier ├── haarcascade_frontalface_default.xml # Classificateur Haar ├── pan_tilt_tracking.py # Fichier principal pour le suivi de la caméra └── pyImageSearch/ ├── init.py # Fichier d'initialisation du package ├── pycache/ # Dossier contenant les fichiers compilés ├── objCenter.py # Fichier contenant la classe ObjCenter └── pid.py # Fichier pour le contrôle PID

# ObjCenter - Détection de Visages avec OpenCV

## Description
`ObjCenter` est une classe Python conçue pour détecter des visages dans des images à l'aide de la bibliothèque OpenCV. Elle utilise un classificateur en cascade Haar pour identifier les visages et peut retourner les coordonnées du centre du visage détecté.

## Prérequis
- Python 3.x
- Bibliothèques :
  - `imutils`
  - `opencv-python`

Vous pouvez installer les bibliothèques requises via pip :

```bash
pip install imutils opencv-python

# Présentation

## Introduction
### Présentation
Le projet "pointeur rouge" a été réalisé dans le cadre de nos études.\
Il s'inscrit dans le domaine de la robotique et de la computer vision.\
Le but est de créer un pointeur laser qui puisse tracker un objet de notre choix
de manière autonome.\
L'objet à tracker est laissé libre. Ceci nous oblige à explorer les
différentes solutions de computer vision.

### Objectifs
Domaine : robotique - computer vision;\
But : tracker un objet par un laser de manière autonome;\
Objet à traquer : au choix de l'équipe;\
Décision de l'équipe : zone du corps - main ou tête : à adapter selon algorithme
de computer vision.

### Contraintes
Budget limite : 150€.

# Utilisation
## Lancement du programme
```bash
python3 pan_tilt_tracking.py [-c !ou! --cascade] [path_to_haar_file]
```
# Hardware et matériel

## Hardware
Système : Raspberry Pi 3, 4;\
OS : Raspbery Pi OS.

## Matériel
Motorisation : 2* servos 9g;\
Laser : diode laser;\
Caméra : Pi caméra V2;\
Articulation : Pan-tilt impression 3D.

# Software

## Prérequis
- python3

## Bibliothèques nécessaires
- `imutils` : Fournit des fonctions utilitaires pour manipuler les images et simplifier les opérations de traitement d'image avec OpenCV;
- `opencv-python` : Utilisé pour le traitement d'image, la détection d'objets et d'autres tâches liées à la vision par ordinateur;
- `pantilthat` (optionnel) : si un module Pan-Tilt Hat est utilisé pour contrôler la motorisation du laser. Ici le hat est imprimé "maison", sans PCB, et ne nécessite pas de bibliothèque.
 
```bash
pip install imutils opencv-python pantilthat
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
`haarcascade_frontalface_default.xml` contient les paramètres d'un classificateur en cascade Haar spécialement entraîné pour la détection de visages dans des images. Il fait partie des outils d'OpenCV pour la vision par ordinateur et repose sur les caractéristiques haar : des motifs de luminosité permettant de détecter des formes distinctes (comme les yeux, le nez et la bouche) dans une région.

#### Avantages
Détection rapide et efficace : la cascade de Haar est optimisée pour être rapide, en passant par une série de filtres de plus en plus précis.
Calcul peu énergivore : permet d'éviter une surcharge au niveau du processeur
du RPI 3, 4.

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
`ObjCenter` est une classe Python conçue pour détecter un objet dans des frames à l'aide de la bibliothèque OpenCV. Ici, elle utilise un classificateur en cascade Haar pour identifier les visages et retourne les coordonnées du centre du visage détecté.

### Fonctionnement 
La classe suit le processus suivant :
- Capture de Frame : récupère la frame actuelle.
- Détection des l’Objet : utilise un classificateur en cascade (chargé depuis le fichier Haar) pour détecter les zones correspondant à l'objet. Si plusieurs objets sont detectés, celui présentant les plus grandes dimensions est isolé. Le postulat suivant est établi : objet le plus grand = objet le plus proche.
- Calcul du Centre : si un objet est détecté, il calcule et renvoie les coordonnées centrales.

### Utilisation
Le fichier objCenter.py est appelé dans le script principal (pan_tilt_tracking.py), qui utilise la position du centre de l'objet pour diriger les servos de manière dynamique et ajuster la trajectoire du laser.

### pid.py - Régulateur PID "Proportionnel Intégral Dérivé"
#### Description
pid.py contient une classe de contrôleur PID (Proportionnel Intégral Dérivé) qui aide à stabiliser et à ajuster la position du laser pour suivre l'objet détecté de manière fluide. Le contrôleur PID corrige la position des servos en fonction des erreurs de position accumulées, permettant une réaction douce et progressive aux mouvements de l'objet suivi.

#### Fonctionnement
Le PID ajuste la position selon trois composants :
- Proportionnel (P) : ajuste proportionnellement à l'erreur actuelle (distance de l'objet par rapport au centre);
- Intégral (I) : cumul des erreurs passées pour réduire l'oscillation et atteindre une position stable;
- Dérivé (D) : tient compte de la variation de l'erreur pour anticiper les corrections nécessaires.

#### Utilisation
Le fichier est utilisé par le script principal pour appliquer la correction de position des servos en continu, en tenant compte des données fournies par objCenter.py.

#### Ressources utiles
https://fr.wikipedia.org/wiki/R%C3%A9gulateur_PID

### pan_tilt_tracking.pyImageSearch
#### Description
pan_tilt_tracking.py est le script principal du projet qui orchestre le processus complet de suivi de l’objet. Il initialise la caméra, configure les objets de détection et de PID, et met à jour la position des servos pour maintenir l’objet centré en continu.

#### Fonctionnement

- Initialisation : charge les bibliothèques, initialise les paramètres de suivi, et configure la caméra.
- Détection de l’Objet : récupère la frame de la caméra, détecte la position de l'objet avec objCenter.
- Mise à Jour des Servos : applique les corrections PID pour ajuster la position des servos.
- Affichage Vidéo : montre la vidéo en temps réel avec la zone de suivi.
- Nettoyage : ferme et libère les ressources à la fin.

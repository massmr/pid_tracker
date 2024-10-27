# pid_tracker
Project Beta Adimaker 24/25 "pointeur rouge".

## Objectifs
But : tracker laser autonome\
Objet à traquer : non défini\
Choix de l'équipe : zone du corps - main ou tête

## Prérequis
- Python 3

## Bibliothèques
- `imutils`
- `opencv-python`
 
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

### ObjCenter - Détection de Visages avec OpenCV

#### Description
`ObjCenter` est une classe Python conçue pour détecter des visages dans des images à l'aide de la bibliothèque OpenCV. Elle utilise un classificateur en cascade Haar pour identifier les visages et peut retourner les coordonnées du centre du visage détecté.



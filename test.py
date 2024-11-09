import cv2
import numpy as np

# Charger le classificateur Haarcascade pour la détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Paramétrer GStreamer pour envoyer le flux via UDP
gst_pipeline = (
    "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
    "rtph264pay config-interval=1 pt=96 ! udpsink host=<IP_DU_DESTINATAIRE> port=5000"
)

# Remplacez <IP_DU_DESTINATAIRE> par l'adresse IP de l'appareil de réception (ex. IP de votre Mac)
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut
out = cv2.VideoWriter(gst_pipeline, cv2.CAP_GSTREAMER, 0, 20, (640, 480), True)

if not cap.isOpened() or not out.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra ou le pipeline GStreamer.")
    exit()

print("Envoi du flux vidéo avec détection de visage. Appuyez sur Ctrl+C pour arrêter.")

try:
    while True:
        # Capture de la frame
        ret, frame = cap.read()
        if not ret:
            print("Erreur lors de la capture de l'image.")
            break

        # Convertir en niveaux de gris pour la détection de visage
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Dessiner les rectangles autour des visages détectés
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Envoyer le frame traité au pipeline GStreamer
        out.write(frame)

        # Affichage local (optionnel)
        cv2.imshow("Flux local avec détection de visage", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Flux vidéo arrêté.")

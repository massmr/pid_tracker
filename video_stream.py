import cv2
import subprocess

# Lancer le flux `libcamera` avec une basse résolution et niveaux de gris
command = [
    "libcamera-vid", 
    "--width", "640", 
    "--height", "480", 
    "--greyscale",
    "--framerate", "15", 
    "--output", "pipe:1"
]
# Ouvrir le flux
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    # Lire les images depuis le flux
    raw_frame = process.stdout.read(640 * 480)
    if len(raw_frame) != 640 * 480:
        print("Erreur de lecture du flux vidéo.")
        break

    # Convertir en numpy array pour opencv
    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640))

    # Traitement avec OpenCV
    cv2.imshow("Flux Niveaux de Gris", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

process.terminate()
cv2.destroyAllWindows()

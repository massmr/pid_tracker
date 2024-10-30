
import board
import busio
from adafruit_pca9685 import PCA9685
import time

# Définir les valeurs minimales et maximales pour les servos
SERVO_MIN = 150  # Ajuster selon les spécifications du servo
SERVO_MAX = 600  # Ajuster selon les spécifications du servo

# Fonction pour convertir un angle en impulsion PWM
def angle_to_pwm(angle):
    return int(SERVO_MIN + (SERVO_MAX - SERVO_MIN) * (angle + 90) / 180)

# Initialiser la communication I2C et le contrôleur PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

try:
    # Définir les servos en position médiane (0°)
    pan_center = angle_to_pwm(0)  # Centre pour le servo de pan
    tilt_center = angle_to_pwm(0)  # Centre pour le servo de tilt

    pca.channels[0].duty_cycle = pan_center  # Canal 0 pour le servo de pan
    pca.channels[1].duty_cycle = tilt_center  # Canal 1 pour le servo de tilt

    print("Servos positionnés en position médiane (0°).")
    time.sleep(2)  # Attendre pour assurer le positionnement correct

finally:
    # Arrêter le signal PWM et libérer les ressources
    pca.deinit()
    print("Script terminé et connexion I2C fermée.")

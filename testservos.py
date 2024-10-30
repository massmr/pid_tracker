
import board
import busio
from adafruit_pca9685 import PCA9685
import time

# Définir les valeurs minimales et maximales pour les servos
SERVO_MIN = 150
SERVO_MAX = 600

# Fonction pour convertir un angle en impulsion PWM
def angle_to_pwm(angle):
    return int(SERVO_MIN + (SERVO_MAX - SERVO_MIN) * (angle + 90) / 180)

# Initialiser la communication I2C et le contrôleur PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Contrôler les servos
try:
    print("Déplacement des servos en position centrale...")
    pan_center = angle_to_pwm(0)  # Centre
    tilt_center = angle_to_pwm(0)  # Centre
    pca.channels[0].duty_cycle = pan_center
    pca.channels[1].duty_cycle = tilt_center
    time.sleep(2)

    print("Déplacement des servos à -90°...")
    pan_left = angle_to_pwm(-90)  # -90°
    tilt_down = angle_to_pwm(-90)  # -90°
    pca.channels[0].duty_cycle = pan_left
    pca.channels[1].duty_cycle = tilt_down
    time.sleep(2)

    print("Déplacement des servos à +90°...")
    pan_right = angle_to_pwm(90)  # +90°
    tilt_up = angle_to_pwm(90)    # +90°
    pca.channels[0].duty_cycle = pan_right
    pca.channels[1].duty_cycle = tilt_up
    time.sleep(2)

    print("Retour en position centrale...")
    pca.channels[0].duty_cycle = pan_center
    pca.channels[1].duty_cycle = tilt_center
    time.sleep(2)

finally:
    # Arrêter le signal PWM et libérer les ressources
    pca.deinit()
    print("Test terminé et connexion I2C fermée.")

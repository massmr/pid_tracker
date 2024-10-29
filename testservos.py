# Code pour tester les servos sans le tracker
for angle in range(0, 180, 10):
    send_servo_command(angle, angle)  # Tourne les servos de 0° à 180° progressivement
    time.sleep(0.5)

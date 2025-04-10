from gpiozero import MotionSensor , LED
import pygame
import tkinter as tk

armed = False
pir = MotionSensor(4)
led = LED(18)

pygame.mixer.init()
pygame.mixer.music.load('alarm_noise.mp3')


window = tk.Tk()
window.title("Motion Detection System")
window.geometry("400x400")

status_label = tk.Label(window, text="Status: Idle", font=("Arial", 20), background="lightgreen")
status_label.pack(pady=20)


def arm_system():
    global armed
    armed = True
    status_label.config(text="Status: Armed", font=("Arial", 20), background="lightblue")



def disarm_system():
    global armed
    armed = False
    status_label.config(text="Status: Idle", font=("Arial", 20), background="lightgreen")
    led.off()
    pygame.mixer.music.stop()

def alert():
    status_label.config(text="MOTION DETECTED", font=("Arial", 20), background="red")
    led.on()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()


def check_status():
    global armed
    if armed:
        pir.wait_for_motion()
        alert()
        window.after(3000, disarm_system)
    window.after(500, check_status)

arm_button = tk.Button(window, text="Arm System", command=arm_system, font=("Arial", 20))
arm_button.pack(pady=10)
disarm_button = tk.Button(window, text="Disarm System", command=disarm_system, font=("Arial", 20))
disarm_button.pack(pady=10)

check_status()
window.mainloop()




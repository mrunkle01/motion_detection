from gpiozero import MotionSensor , LED
import pygame
import tkinter as tk

armed = False
pir = MotionSensor(4)
led = LED(18)
pygame.mixer.init()

window = tk.Tk()
window.title("Motion Detection System")
window.geometry("400x400")

status_label = tk.Label(window, text="Status: Idle", font=("Engravers MT", 20), background="lightgreen")
status_label.pack(pady=20)

def arm_system():
    print("ARMED")
    pygame.mixer.music.stop()
    pygame.mixer.music.load("armed.mp3")
    pygame.mixer.music.play()
    global armed
    armed = True
    status_label.config(text="Status: Armed", font=("Engravers MT", 20), background="lightblue")

def password_window():
    print("PASSWORD window")
    pw_window = tk.Toplevel(window)
    pw_window.title("Password Checker")
    pw_window.geometry("400x150")

    pwrd_label = tk.Label(pw_window, text="Enter Password: ", font=("Engravers MT", 15))
    pwrd_label.pack(pady=10)

    pwrd_entry = tk.Entry(pw_window, show="*", font=("Arial", 14))
    pwrd_entry.pack()

    def password_checker():
        password = "12345"
        entered_password = pwrd_entry.get()
        if entered_password == password:
            pw_window.destroy()
            disarm_system()
        else:
            pwrd_label.config(text="Incorrect Password", fg="red")

    pwrd_check = tk.Button(pw_window, text="Check", command=password_checker, font=("Arial", 14))
    pwrd_check.pack(pady=10)

def disarm_system():
    print("DISARMED")
    pygame.mixer.music.stop()
    pygame.mixer.music.load("disarmed.mp3")
    pygame.mixer.music.play()

    global armed
    armed = False
    status_label.config(text="Status: Idle", font=("Engravers MT", 20), background="lightgreen")
    led.off()

def alert():
    print("ALERTED")
    pygame.mixer.music.load("alarm_noise.mp3")
    status_label.config(text="MOTION DETECTED", font=("Engravers MT", 20), background="red")
    led.on()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1)

def check_status():
    global armed
    if armed:
        pir.wait_for_motion()
        alert()
        window.after(1500, disarm_system)
    window.after(500, check_status)

arm_button = tk.Button(window, text="Arm System", command=arm_system, font=("Engravers MT", 20))
arm_button.pack(pady=10)

disarm_button = tk.Button(window, text="Disarm System", command=password_window, font=("Engravers MT", 20))
disarm_button.pack(pady=10)

check_status()
window.mainloop()




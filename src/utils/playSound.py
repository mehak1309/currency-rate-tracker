from playsound import playsound

def play_sound():
    try:
        playsound("../currency-exchange-monitor/sounds/notification.mp3")
    except Exception as e:
        print(f"An error occurred: {e}")

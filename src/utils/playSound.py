from playsound import playsound

def play_sound():
    """
    This function plays a notification sound.
    It attempts to play a sound from the specified file path. If an error occurs during playback,
    it catches the exception and prints an error message.
    """
    try:
        playsound("../currency-exchange-monitor/sounds/notification.mp3")
    except Exception as e:
        print(f"An error occurred: {e}")

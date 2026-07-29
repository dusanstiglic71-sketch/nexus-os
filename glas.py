import pyttsx3

try:
    print("Palim zvučnike...")
    engine = pyttsx3.init()
    engine.say("Zdravo! Da li me sada čuješ?")
    engine.runAndWait()
    print("Test završen!")
except Exception as e:
    print(f"Prijavljena greška: {e}")
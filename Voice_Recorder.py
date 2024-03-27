import sounddevice
from scipy.io.wavfile import write

def record_audio(duration_seconds):
    fs = 44100  # Sample rate
    print(f"Recording for {duration_seconds} seconds...")
    record_voice = sounddevice.rec(int(duration_seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write("out.wav", fs, record_voice)
    print("Recording finished. File saved as 'out.wav'.")
    
if __name__ == "__main__":
    try:
        duration = int(input("Enter the duration of the recording in seconds: "))
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        record_audio(duration)

    except Exception as e:
        print(f"An error occurred: {e}")
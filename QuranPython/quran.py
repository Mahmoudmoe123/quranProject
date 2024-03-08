import speech_recognition as sr
from os.path import join, dirname, abspath

def generate_srt(audio_file_path, script_file_path, output_srt_path):
    recognizer = sr.Recognizer()
    
    # Process audio in chunks - here we use a fixed duration for simplicity
    chunk_duration = 20  # seconds
    with sr.AudioFile(audio_file_path) as source:
        audio_duration = source.DURATION
        chunks = int(audio_duration // chunk_duration) + (audio_duration % chunk_duration > 0)

        for i in range(chunks):
            # Adjust start time for each chunk
            start = i * chunk_duration
            end = start + chunk_duration
            with sr.AudioFile(audio_file_path) as source:
                # Adjust recognizer.record to capture specific chunk by offset and duration
                audio_data = recognizer.record(source, offset=start, duration=chunk_duration)
                try:
                    # Recognize speech using Google's speech recognition
                    text = recognizer.recognize_google(audio_data, language='ar-AR')  # Specify Arabic as the language
                    print(f"Chunk {i+1}/{chunks}: {text[:50]}...")  # Just to demonstrate progress
                    
                    # Simple timecode calculation (very basic for demonstration purposes)
                    start_timecode = f"{start//3600:02d}:{(start%3600)//60:02d}:{start%60:02d},000"
                    end_timecode = f"{end//3600:02d}:{(end%3600)//60:02d}:{end%60:02d},000"
                    
                    # Write to SRT file
                    with open(output_srt_path, 'a', encoding='utf-8') as output_file:
                        output_file.write(f"{i+1}\n")
                        output_file.write(f"{start_timecode} --> {end_timecode}\n")
                        output_file.write(f"{text}\n\n")
                except sr.UnknownValueError:
                    print(f"Speech Recognition could not understand audio in chunk {i+1}")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
# Example usage
audio_file_path = r'C:\Users\Fifam\OneDrive\Desktop\QuranPaths\QuranAudio\001 Surah Al-Fatiha With English Translation By Sheikh Noreen Muhammad Siddique.wav'
script_file_path = r'C:\Users\Fifam\OneDrive\Desktop\QuranPaths\QuranText\Alfatiha.txt'
output_srt_path = r'C:\Users\Fifam\OneDrive\Desktop\QuranPaths\QuranSrt\001-al-faatihah.srt'

generate_srt(audio_file_path, script_file_path, output_srt_path)

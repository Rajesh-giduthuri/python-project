from process import process_audio
from audio.transcriber import transcribe_all


input_file = r"uploads\short_meeting-2.webm"

print("Processing audio...")

chunks = process_audio(input_file)

print(f"\nCreated {len(chunks)} chunk(s).")

transcript = transcribe_all(
    chunks,
    language="english"
)

print("\n\n========== COMPLETE TRANSCRIPT ==========")
print(transcript)
print("==========================================")
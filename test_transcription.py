from audio.transcriber import transcribe_chunk_groq

chunk_path = r"uploads\short_meeting-3_converted.wav_chunk_0.wav"

print("Testing Groq Whisper...")
print(f"Chunk: {chunk_path}")

text = transcribe_chunk_groq(
    chunk_path,
    language="english"
)

print("\n========== TRANSCRIPT ==========")
print(text)
print("================================")
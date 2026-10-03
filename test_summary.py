from summarizer import generate_summary


transcript_file = r"outputs\short_meeting-2_transcript.txt"


with open(transcript_file, "r", encoding="utf-8") as f:
    transcript = f.read()


print("Transcript loaded.")
print(f"Characters: {len(transcript)}")

summary = generate_summary(transcript)


print("\n========== AI MEETING SUMMARY ==========\n")
print(summary)
print("\n========================================")
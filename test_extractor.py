import json
from extractor import extract_meeting_data


transcript_file = r"outputs\short_meeting-2_transcript.txt"


with open(transcript_file, "r", encoding="utf-8") as f:
    transcript = f.read()


print("Transcript loaded.")
print(f"Characters: {len(transcript)}")


meeting_data = extract_meeting_data(transcript)


print("\n========== STRUCTURED MEETING DATA ==========\n")

print(
    json.dumps(
        meeting_data,
        indent=4,
        ensure_ascii=False
    )
)

print("\n=============================================")
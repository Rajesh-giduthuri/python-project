
import json
from pathlib import Path

import streamlit as st

from config.settings import UPLOAD_DIR, OUTPUT_DIR
from process import process_audio
from audio.transcriber import transcribe_all

from ai.summarizer import analyze_meeting
from ai.extractor import extract_meeting_data

from rag.qa import answer_question


st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="🎙️",
    layout="wide"
)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


if "processed" not in st.session_state:
    st.session_state.processed = False

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if "meeting_data" not in st.session_state:
    st.session_state.meeting_data = {}


st.title("🎙️ AI Meeting Intelligence")

st.caption(
    "Open-source AI pipeline for transcription, meeting analysis, "
    "structured extraction and transcript-based Q&A."
)

st.divider()


if st.session_state.processed:

    if st.button("➕ Process Another Meeting"):

        st.session_state.processed = False
        st.session_state.transcript = ""
        st.session_state.analysis = ""
        st.session_state.meeting_data = {}

        st.rerun()


if not st.session_state.processed:

    st.subheader("📥 Upload Meeting")

    uploaded_file = st.file_uploader(
        "Choose an audio/video file",
        type=["mp3", "wav", "m4a", "mp4", "webm"]
    )

    if uploaded_file:

        st.info(f"Selected: {uploaded_file.name}")

        if st.button(
            "🚀 Process Meeting",
            type="primary",
            use_container_width=True
        ):

            try:

                input_path = UPLOAD_DIR / uploaded_file.name

                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())


                with st.status(
                    "Processing meeting...",
                    expanded=True
                ) as status:

                    st.write("🎵 Preparing audio...")

                    chunks = process_audio(
                        str(input_path)
                    )

                    st.write(
                        f"Created {len(chunks)} audio chunk(s)."
                    )


                    st.write(
                        "🎙️ Transcribing with Faster-Whisper..."
                    )

                    transcript = transcribe_all(
                        chunks
                    )

                    if not transcript.strip():
                        raise ValueError(
                            "Transcription returned empty text."
                        )

                    st.session_state.transcript = transcript

                    transcript_file = (
                        OUTPUT_DIR /
                        f"{input_path.stem}_transcript.txt"
                    )

                    transcript_file.write_text(
                        transcript,
                        encoding="utf-8"
                    )

                    Path("/content/transcript.txt").write_text(
                        transcript,
                        encoding="utf-8"
                    )


                    st.write(
                        "🤖 Generating meeting analysis..."
                    )

                    analysis = analyze_meeting(
                        transcript
                    )

                    st.session_state.analysis = analysis

                    analysis_file = (
                        OUTPUT_DIR /
                        f"{input_path.stem}_summary.txt"
                    )

                    analysis_file.write_text(
                        analysis,
                        encoding="utf-8"
                    )


                    st.write(
                        "📋 Extracting structured meeting data..."
                    )

                    meeting_data = extract_meeting_data(
                        transcript
                    )

                    st.session_state.meeting_data = meeting_data

                    json_file = (
                        OUTPUT_DIR /
                        f"{input_path.stem}_analysis.json"
                    )

                    json_file.write_text(
                        json.dumps(
                            meeting_data,
                            indent=2,
                            ensure_ascii=False
                        ),
                        encoding="utf-8"
                    )


                    status.update(
                        label="✅ Meeting processing complete",
                        state="complete"
                    )


                st.session_state.processed = True

                st.rerun()


            except Exception as error:

                st.error(
                    f"❌ Processing failed:\n\n{error}"
                )


if st.session_state.processed:

    transcript = st.session_state.transcript
    analysis = st.session_state.analysis
    meeting_data = st.session_state.meeting_data


    st.header("🎙️ Transcript")

    st.text_area(
        "Meeting Transcript",
        value=transcript,
        height=400,
        label_visibility="collapsed"
    )


    st.header("📝 Meeting Analysis")

    st.markdown(analysis)


    st.header("📋 Structured Meeting Data")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Overview")

        st.write(
            meeting_data.get(
                "meeting_overview",
                "No overview available."
            )
        )

        st.subheader("Discussion Points")

        points = meeting_data.get(
            "key_discussion_points",
            []
        )

        for point in points:
            st.markdown(f"- {point}")


    with col2:

        st.subheader("Decisions")

        decisions = meeting_data.get(
            "decisions",
            []
        )

        for decision in decisions:
            st.markdown(f"- {decision}")


        st.subheader("Action Items")

        actions = meeting_data.get(
            "action_items",
            []
        )

        for action in actions:
            st.markdown(f"- {action}")


        st.subheader("Next Steps")

        next_steps = meeting_data.get(
            "next_steps",
            []
        )

        for step in next_steps:
            st.markdown(f"- {step}")


    st.divider()

    st.header("🔎 Ask Questions About the Meeting")

    question = st.text_input(
        "Your question",
        placeholder="What decisions were made?"
    )

    if st.button(
        "🤖 Ask Question",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "🔍 Searching the meeting..."
                ):

                    answer = answer_question(
                        question,
                        top_k=5
                    )

                st.subheader("Answer")

                st.success(answer)

            except Exception as error:

                st.error(
                    f"❌ Q&A failed:\n\n{error}"
                )


    st.divider()

    st.header("📁 Download Results")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇️ Download Transcript",
            transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

    with col2:

        st.download_button(
            "⬇️ Download JSON",
            json.dumps(
                meeting_data,
                indent=2,
                ensure_ascii=False
            ),
            file_name="meeting_analysis.json",
            mime="application/json"
        )

import streamlit as st
from pathlib import Path

from config.settings import UPLOAD_DIR, OUTPUT_DIR

from audio.processor import process_audio
from audio.transcriber import (
    transcribe_audio,
    save_transcript
)

from audio.youtube import download_youtube_audio

from ai.summarizer import analyze_meeting
from ai.extractor import (
    extract_meeting_data,
    save_meeting_json
)

from database.service import save_meeting

from rag.vector_store import add_meeting_transcript
from rag.qa import ask_meeting_question


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="🎙️",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #777;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .step-title {
        font-size: 1.45rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .step-number {
        font-size: 0.85rem;
        font-weight: 600;
        color: #777;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .answer-box {
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-top: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SESSION STATE
# ==================================================

if "meeting_processed" not in st.session_state:
    st.session_state.meeting_processed = False

if "meeting_id" not in st.session_state:
    st.session_state.meeting_id = None

if "video_path" not in st.session_state:
    st.session_state.video_path = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "meeting_data" not in st.session_state:
    st.session_state.meeting_data = None

if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if "source_name" not in st.session_state:
    st.session_state.source_name = ""


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">'
    '🎙️ AI Meeting Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload a meeting or use a YouTube video to generate '
    'transcripts, summaries, insights and AI-powered Q&A.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# RESET BUTTON
# ==================================================

if st.session_state.meeting_processed:

    if st.button(
        "➕ Process Another Meeting"
    ):

        st.session_state.meeting_processed = False
        st.session_state.meeting_id = None
        st.session_state.video_path = None
        st.session_state.transcript = ""
        st.session_state.meeting_data = None
        st.session_state.analysis = ""
        st.session_state.source_name = ""

        st.rerun()


# ==================================================
# STEP 1 — INPUT
# ==================================================

if not st.session_state.meeting_processed:

    st.markdown(
        '<div class="step-number">Step 1</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="step-title">'
        '📥 Choose Meeting Source'
        '</div>',
        unsafe_allow_html=True
    )

    upload_tab, youtube_tab = st.tabs(
        [
            "📁 Upload Meeting",
            "📺 YouTube"
        ]
    )


    # ==================================================
    # FILE UPLOAD
    # ==================================================

    with upload_tab:

        uploaded_file = st.file_uploader(
            "Upload a meeting recording",
            type=[
                "mp3",
                "wav",
                "m4a",
                "mp4",
                "webm"
            ],
            help="Supported: MP3, WAV, M4A, MP4 and WEBM"
        )

        if uploaded_file:

            st.info(
                f"Selected file: {uploaded_file.name}"
            )

            if st.button(
                "🚀 Start Processing",
                type="primary",
                use_container_width=True
            ):

                try:

                    # ----------------------------------
                    # SAVE FILE
                    # ----------------------------------

                    input_path = (
                        UPLOAD_DIR
                        / uploaded_file.name
                    )

                    with open(
                        input_path,
                        "wb"
                    ) as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )


                    # ----------------------------------
                    # PROCESS AUDIO
                    # ----------------------------------

                    with st.status(
                        "Processing meeting...",
                        expanded=True
                    ) as status:

                        st.write(
                            "🎵 Preparing audio..."
                        )

                        processed_audio = (
                            process_audio(
                                input_path
                            )
                        )


                        # ----------------------------------
                        # TRANSCRIPTION
                        # ----------------------------------

                        st.write(
                            "☁️ Transcribing with OpenRouter Whisper..."
                        )

                        segments = (
                            transcribe_audio(
                                processed_audio
                            )
                        )
                        transcript = "\n".join(
                            segment["text"]
                            for segment in segments
                        )


                        # ----------------------------------
                        # SAVE TRANSCRIPT
                        # ----------------------------------

                        transcript_file = (
                            OUTPUT_DIR
                            / f"{input_path.stem}"
                            "_transcript.txt"
                        )

                        save_transcript(
                            segments,
                            transcript_file
                        )


                        # ----------------------------------
                        # AI ANALYSIS
                        # ----------------------------------

                        st.write(
                            "🤖 Generating meeting summary..."
                        )

                        analysis = (
                            analyze_meeting(
                                transcript
                            )
                        )


                        # ----------------------------------
                        # STRUCTURED DATA
                        # ----------------------------------

                        meeting_data = (
                            extract_meeting_data(
                                analysis
                            )
                        )


                        # ----------------------------------
                        # SAVE JSON
                        # ----------------------------------

                        json_file = (
                            OUTPUT_DIR
                            / f"{input_path.stem}"
                            "_analysis.json"
                        )

                        save_meeting_json(
                            meeting_data,
                            json_file
                        )


                        # ----------------------------------
                        # DATABASE
                        # ----------------------------------

                        st.write(
                            "🗄️ Saving meeting..."
                        )

                        meeting_id = save_meeting(
                            filename=uploaded_file.name,
                            transcript=transcript,
                            meeting_data=meeting_data
                        )


                        # ----------------------------------
                        # RAG
                        # ----------------------------------

                        st.write(
                            "🧠 Preparing question answering..."
                        )

                        add_meeting_transcript(
                            meeting_id=meeting_id,
                            transcript=transcript
                        )


                        status.update(
                            label="✅ Meeting processing complete",
                            state="complete"
                        )


                    # ----------------------------------
                    # STORE CURRENT MEETING
                    # ----------------------------------

                    st.session_state.meeting_processed = True

                    st.session_state.meeting_id = meeting_id

                    st.session_state.video_path = str(
                        input_path
                    )

                    st.session_state.transcript = transcript

                    st.session_state.meeting_data = meeting_data

                    st.session_state.analysis = analysis

                    st.session_state.source_name = (
                        uploaded_file.name
                    )

                    st.rerun()


                except Exception as error:

                    st.error(
                        f"❌ Processing failed:\n\n{error}"
                    )


    # ==================================================
    # YOUTUBE
    # ==================================================

    with youtube_tab:

        youtube_url = st.text_input(
            "Paste YouTube URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )

        if st.button(
            "🚀 Process YouTube Meeting",
            type="primary",
            use_container_width=True
        ):

            if not youtube_url.strip():

                st.warning(
                    "Please enter a YouTube URL."
                )

            else:

                try:

                    with st.status(
                        "Processing YouTube meeting...",
                        expanded=True
                    ) as status:

                        # ----------------------------------
                        # DOWNLOAD
                        # ----------------------------------

                        st.write(
                            "📥 Downloading YouTube video..."
                        )

                        youtube_file = (
                            download_youtube_audio(
                                youtube_url
                            )
                        )


                        # ----------------------------------
                        # AUDIO PROCESSING
                        # ----------------------------------

                        st.write(
                            "🎵 Preparing audio..."
                        )

                        processed_audio = (
                            process_audio(
                                youtube_file
                            )
                        )


                        # ----------------------------------
                        # TRANSCRIPTION
                        # ----------------------------------

                        st.write(
                            "☁️ Transcribing with OpenRouter Whisper..."
                        )

                        segments = (
                            transcribe_audio(
                                processed_audio
                            )
                        )

                        transcript = "\n".join(
                            segment["text"]
                            for segment in segments
                        )


                        # ----------------------------------
                        # AI ANALYSIS
                        # ----------------------------------

                        st.write(
                            "🤖 Generating meeting summary..."
                        )

                        analysis = (
                            analyze_meeting(
                                transcript
                            )
                        )


                        meeting_data = (
                            extract_meeting_data(
                                analysis
                            )
                        )


                        # ----------------------------------
                        # DATABASE
                        # ----------------------------------

                        st.write(
                            "🗄️ Saving meeting..."
                        )

                        meeting_id = save_meeting(
                            filename=youtube_file.name,
                            transcript=transcript,
                            meeting_data=meeting_data
                        )


                        # ----------------------------------
                        # RAG
                        # ----------------------------------

                        st.write(
                            "🧠 Preparing question answering..."
                        )

                        add_meeting_transcript(
                            meeting_id=meeting_id,
                            transcript=transcript
                        )


                        status.update(
                            label="✅ YouTube meeting processed",
                            state="complete"
                        )


                    # ----------------------------------
                    # STORE CURRENT MEETING
                    # ----------------------------------

                    st.session_state.meeting_processed = True

                    st.session_state.meeting_id = meeting_id

                    st.session_state.video_path = str(
                        youtube_file
                    )

                    st.session_state.transcript = transcript

                    st.session_state.meeting_data = meeting_data

                    st.session_state.analysis = analysis

                    st.session_state.source_name = (
                        youtube_file.name
                    )

                    st.rerun()


                except Exception as error:

                    st.error(
                        f"❌ YouTube processing failed:\n\n{error}"
                    )


# ==================================================
# CURRENT MEETING RESULTS
# ==================================================

if st.session_state.meeting_processed:

    meeting_data = (
        st.session_state.meeting_data
    )

    transcript = (
        st.session_state.transcript
    )

    video_path = (
        st.session_state.video_path
    )


    # ==================================================
    # STEP 2 — VIDEO + TRANSCRIPT
    # ==================================================

    st.divider()

    st.markdown(
        '<div class="step-number">Step 2</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="step-title">'
        '🎬 Meeting Video & Transcript'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        st.session_state.source_name
    )


    video_col, transcript_col = st.columns(
        [1, 1]
    )


    # ------------------------------------------
    # VIDEO
    # ------------------------------------------

    with video_col:

        st.subheader(
            "🎥 Recording"
        )

        video_file = Path(
            video_path
        )

        if video_file.exists():

            video_suffix = (
                video_file.suffix.lower()
            )

            if video_suffix in [
                ".mp4",
                ".webm",
                ".mov"
            ]:

                st.video(
                    str(video_file)
                )

            else:

                st.info(
                    "This meeting contains audio only."
                )

        else:

            st.warning(
                "Recording file is no longer available."
            )


    # ------------------------------------------
    # TRANSCRIPT
    # ------------------------------------------

    with transcript_col:

        st.subheader(
            "🎙️ Transcript"
        )

        st.text_area(
            "Meeting transcript",
            value=transcript,
            height=400,
            label_visibility="collapsed"
        )


    # ==================================================
    # STEP 3 — AI ANALYSIS
    # ==================================================

    st.divider()

    st.markdown(
        '<div class="step-number">Step 3</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="step-title">'
        '🤖 AI Meeting Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    # ------------------------------------------
    # SUMMARY
    # ------------------------------------------

    st.subheader(
        "📝 Summary"
    )

    st.write(
        meeting_data.get(
            "summary",
            "No summary available."
        )
    )


    # ------------------------------------------
    # KEY POINTS
    # ------------------------------------------

    st.subheader(
        "🔑 Key Points"
    )

    key_points = meeting_data.get(
        "key_points",
        []
    )

    if key_points:

        for point in key_points:

            st.markdown(
                f"- {point}"
            )

    else:

        st.info(
            "No key points identified."
        )


    # ------------------------------------------
    # DECISIONS
    # ------------------------------------------

    st.subheader(
        "🎯 Decisions"
    )

    decisions = meeting_data.get(
        "decisions",
        []
    )

    if decisions:

        for decision in decisions:

            st.markdown(
                f"- {decision}"
            )

    else:

        st.info(
            "No explicit decisions identified."
        )


    # ------------------------------------------
    # ACTION ITEMS
    # ------------------------------------------

    st.subheader(
        "✅ Action Items"
    )

    action_items = meeting_data.get(
        "action_items",
        []
    )

    if action_items:

        for item in action_items:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**Task:** {item.get('task', 'Not specified')}"
                )

                st.markdown(
                    f"**Owner:** {item.get('owner', 'Not specified')}"
                )

                st.markdown(
                    f"**Deadline:** {item.get('deadline', 'Not specified')}"
                )

    else:

        st.info(
            "No explicit action items identified."
        )


    # ==================================================
    # STEP 4 — RAG Q&A
    # ==================================================

    st.divider()

    st.markdown(
        '<div class="step-number">Step 4</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="step-title">'
        '🔎 Ask Questions About This Meeting'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Ask questions and get answers from the meeting transcript."
    )


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

                    answer = ask_meeting_question(
                        question,
                        top_k=5
                    )

                st.subheader(
                    "Answer"
                )

                st.success(
                    answer
                )

            except Exception as error:

                st.error(
                    f"❌ Q&A failed:\n\n{error}"
                )
import streamlit as st
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# =====================================
# GEMINI API SETUP
# =====================================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash-lite"
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="CORTEXA",
    page_icon="🎓",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title("🎓 CORTEXA")
st.subheader(
    "AI Lecture-to-Learning Assistant"
)

# =====================================
# YOUTUBE INPUT
# =====================================

video_url = st.text_input(
    "Paste YouTube Video URL"
)

# =====================================
# EXTRACT VIDEO ID
# =====================================

def extract_video_id(url):

    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in (
        "www.youtube.com",
        "youtube.com"
    ):
        return parse_qs(
            parsed_url.query
        )["v"][0]

    return None

# =====================================
# GET TRANSCRIPT
# =====================================

def get_transcript(video_url):

    video_id = extract_video_id(
        video_url
    )

    transcript_list = (
        YouTubeTranscriptApi()
        .fetch(video_id)
    )

    full_text = " ".join(
        [
            entry.text.strip()
            for entry in transcript_list
        ]
    )

    return full_text

# =====================================
# GENERATE AI NOTES
# =====================================

def generate_notes(transcript):

    prompt = f"""
    Convert this lecture transcript into:

    1. Structured Notes
    2. Important Concepts
    3. Easy Explanations
    4. Key Takeaways
    5. Bullet Points

    Make the notes clean and readable.

    Transcript:
    {transcript}
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =====================================
# MAIN BUTTON
# =====================================

if st.button("Generate Smart Notes"):

    if video_url:

        # -----------------------------
        # GET TRANSCRIPT
        # -----------------------------

        with st.spinner(
            "Extracting Transcript..."
        ):

            transcript = get_transcript(
                video_url
            )

        st.success(
            "Transcript Extracted!"
        )

        # -----------------------------
        # GENERATE NOTES
        # -----------------------------

        with st.spinner(
            "Generating AI Notes..."
        ):

            notes = generate_notes(
                transcript
            )

        st.success(
            "Smart Notes Generated!"
        )

        # -----------------------------
        # DISPLAY NOTES
        # -----------------------------

        st.header("📝 Smart Notes")

        st.write(notes)

    else:

        st.warning(
            "Please enter YouTube URL"
        )
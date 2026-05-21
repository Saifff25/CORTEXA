import streamlit as st
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# =====================================
# GEMINI API
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
# INPUT
# =====================================

video_url = st.text_input(
    "Paste YouTube Video URL"
)

# =====================================
# SESSION STATE
# =====================================

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "flashcards" not in st.session_state:
    st.session_state.flashcards = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = ""

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
# GENERATE NOTES
# =====================================

def generate_notes(transcript):

    prompt = f"""
    Convert this lecture transcript into:

    1. Structured Notes
    2. Important Concepts
    3. Easy Explanations
    4. Key Takeaways
    5. Bullet Points

    Transcript:
    {transcript}
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =====================================
# GENERATE FLASHCARDS
# =====================================

def generate_flashcards(transcript):

    prompt = f"""
    Create 10 study flashcards.

    Format EXACTLY like this:

    Q: Question here
    A: Answer here

    Transcript:
    {transcript}
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =====================================
# GENERATE QUIZ
# =====================================

def generate_quiz(transcript):

    prompt = f"""
    Create 5 multiple choice questions from this lecture.

    Format EXACTLY like this:

    QUESTION: What is AI?

    OPTION A: Artificial Intelligence
    OPTION B: Automatic Input
    OPTION C: Artificial Internet
    OPTION D: None

    ANSWER: A

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

if st.button("Generate Study Material"):

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
            "Generating Smart Notes..."
        ):

            notes = generate_notes(
                transcript
            )

        # -----------------------------
        # GENERATE FLASHCARDS
        # -----------------------------

        with st.spinner(
            "Generating Flashcards..."
        ):

            flashcards = generate_flashcards(
                transcript
            )

        # -----------------------------
        # GENERATE QUIZ
        # -----------------------------

        with st.spinner(
            "Generating Quiz..."
        ):

            quiz = generate_quiz(
                transcript
            )

        # -----------------------------
        # SAVE TO SESSION
        # -----------------------------

        st.session_state.notes = notes
        st.session_state.flashcards = flashcards
        st.session_state.quiz = quiz

    else:

        st.warning(
            "Please enter YouTube URL"
        )

# =====================================
# DISPLAY CONTENT
# =====================================

if st.session_state.notes:

    tab1, tab2, tab3 = st.tabs(
        [
            "📝 Smart Notes",
            "🧠 Flashcards",
            "🧪 Quiz"
        ]
    )

    # =====================================
    # NOTES TAB
    # =====================================

    with tab1:

        st.header(
            "📝 AI Smart Notes"
        )

        st.write(
            st.session_state.notes
        )

    # =====================================
    # FLASHCARDS TAB
    # =====================================

    with tab2:

        st.header(
            "🧠 AI Flashcards"
        )

        cards = (
            st.session_state.flashcards
            .split("Q:")
        )

        cols = st.columns(2)

        card_index = 0

        for card in cards:

            if "A:" in card:

                question, answer = card.split(
                    "A:",
                    1
                )

                question = question.strip()
                answer = answer.strip()

                with cols[card_index % 2]:

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#1e1e1e;
                            padding:20px;
                            border-radius:15px;
                            margin-bottom:20px;
                            border:1px solid #444;
                        ">
                            <h4 style='color:#00d4ff;'>
                                ❓ {question}
                            </h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Reveal Answer",
                        key=f"btn_{card_index}"
                    ):

                        st.success(answer)

                card_index += 1

    # =====================================
    # QUIZ TAB
    # =====================================

    with tab3:

        st.header(
            "🧪 AI Quiz"
        )

        quiz_text = (
            st.session_state.quiz
        )

        questions = quiz_text.split(
            "QUESTION:"
        )

        for i, q in enumerate(questions):

            if "ANSWER:" in q:

                question_part, answer_part = q.split(
                    "ANSWER:"
                )

                correct_answer = (
                    answer_part.strip()[0]
                )

                lines = (
                    question_part.strip()
                    .split("\n")
                )

                question = lines[0]

                options = []

                for line in lines[1:]:

                    if "OPTION" in line:

                        options.append(
                            line.strip()
                        )

                st.subheader(
                    f"Q{i}"
                )

                st.write(question)

                user_answer = st.radio(
                    "Choose an answer:",
                    options,
                    key=f"quiz_{i}"
                )

                if st.button(
                    f"Check Answer {i}",
                    key=f"check_{i}"
                ):

                    selected = (
                        user_answer[7]
                    )

                    if (
                        selected
                        == correct_answer
                    ):

                        st.success(
                            "Correct! ✅"
                        )

                    else:

                        st.error(
                            f"Wrong ❌ Correct answer: {correct_answer}"
                        )
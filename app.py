import streamlit as st
import google.generativeai as genai
import speech_recognition as sr

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="CORTEXA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# FUTURISTIC CSS
# =====================================

st.markdown(
    """
    <style>

    /* =====================================
       MAIN BACKGROUND
    ===================================== */

    .stApp {

        background:
        radial-gradient(circle at top left, #172554 0%, transparent 25%),
        radial-gradient(circle at bottom right, #0f172a 0%, transparent 25%),
        linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #111827
        );

        color: white !important;

        overflow-x: hidden;
    }

    /* =====================================
       REMOVE STREAMLIT HEADER
    ===================================== */

    header {

        background: transparent !important;
    }

    .block-container {

        padding-top: 2rem !important;
    }

    /* =====================================
       FORCE TEXT WHITE
    ===================================== */

    html, body, p, span, div, label {

        color: white !important;
    }

    h1, h2, h3, h4, h5, h6 {

        color: white !important;
    }

    /* =====================================
       ANIMATED BACKGROUND
    ===================================== */

    .animated-bg {

        position: fixed;

        width: 100%;
        height: 100%;

        top: 0;
        left: 0;

        background:
        radial-gradient(
            circle,
            rgba(56,189,248,0.12),
            transparent 60%
        );

        animation:
        pulse 6s infinite alternate;

        z-index: -1;
    }

    @keyframes pulse {

        from {

            transform: scale(1);
            opacity: 0.4;
        }

        to {

            transform: scale(1.3);
            opacity: 1;
        }
    }

    /* =====================================
       SIDEBAR
    ===================================== */

    section[data-testid="stSidebar"] {

        background:
        rgba(2,6,23,0.85);

        backdrop-filter: blur(18px);

        border-right:
        1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {

        color: white !important;
    }

    /* =====================================
       BRAIN ICON
    ===================================== */

    .brain-icon {

        font-size: 120px;

        text-align: center;

        margin-bottom: -10px;

        animation:
        brainFloat 3s ease-in-out infinite,
        brainGlow 2s infinite alternate;
    }

    @keyframes brainFloat {

        0% {

            transform: translateY(0px);
        }

        50% {

            transform: translateY(-10px);
        }

        100% {

            transform: translateY(0px);
        }
    }

    @keyframes brainGlow {

        from {

            filter:
            drop-shadow(
                0px 0px 12px rgba(56,189,248,0.3)
            );
        }

        to {

            filter:
            drop-shadow(
                0px 0px 40px rgba(56,189,248,0.9)
            );
        }
    }

    /* =====================================
       HERO TITLE
    ===================================== */

    .hero-title {

        position: relative;

        text-align: center;

        font-size: 95px;

        font-weight: 900;

        letter-spacing: 5px;

        background:
        linear-gradient(
            90deg,
            #38bdf8,
            #818cf8,
            #22d3ee
        );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        animation:
        cortexGlow 2s infinite alternate;
    }

    @keyframes cortexGlow {

        from {

            text-shadow:
            0px 0px 15px rgba(56,189,248,0.4),
            0px 0px 30px rgba(129,140,248,0.25);
        }

        to {

            text-shadow:
            0px 0px 40px rgba(56,189,248,0.95),
            0px 0px 70px rgba(129,140,248,0.8);
        }
    }

    /* =====================================
       ELECTRIC CURRENT EFFECT
    ===================================== */

    .hero-title::before {

        content: "";

        position: absolute;

        top: 50%;
        left: -5%;

        width: 110%;
        height: 8px;

        background:
        linear-gradient(
            90deg,
            transparent,
            rgba(56,189,248,0.9),
            rgba(129,140,248,1),
            rgba(34,211,238,0.9),
            transparent
        );

        filter: blur(8px);

        animation:
        electricFlow 2s linear infinite;

        z-index: -1;
    }

    @keyframes electricFlow {

        0% {

            transform:
            translateX(-120%);
            opacity: 0;
        }

        20% {

            opacity: 1;
        }

        80% {

            opacity: 1;
        }

        100% {

            transform:
            translateX(120%);
            opacity: 0;
        }
    }

    /* =====================================
       SUBTITLE
    ===================================== */

    .hero-subtitle {

        text-align: center;

        font-size: 30px;

        color: #f8fafc !important;

        margin-top: -15px;

        margin-bottom: 55px;

        animation:
        subtitleBounce 2.5s ease-in-out infinite;
    }

    @keyframes subtitleBounce {

        0% {

            transform: translateY(0px);
        }

        25% {

            transform: translateY(-5px);
        }

        50% {

            transform: translateY(0px);
        }

        75% {

            transform: translateY(-3px);
        }

        100% {

            transform: translateY(0px);
        }
    }

    /* =====================================
       INPUT LABEL
    ===================================== */

    .stTextInput label {

        color: #e2e8f0 !important;

        font-size: 18px !important;

        font-weight: 600 !important;
    }

    /* =====================================
       INPUT BOX
    ===================================== */

    .stTextInput input {

        background:
        rgba(15,23,42,0.75) !important;

        color: white !important;

        border:
        1px solid rgba(56,189,248,0.18) !important;

        border-radius: 20px !important;

        padding: 20px !important;

        font-size: 18px !important;

        box-shadow:
        0px 0px 18px rgba(56,189,248,0.08);
    }

    /* =====================================
       PLACEHOLDER
    ===================================== */

    .stTextInput input::placeholder {

        color: #94a3b8 !important;

        opacity: 1 !important;
    }

    /* =====================================
       BUTTONS
    ===================================== */

    .stButton button {

        width: 100%;

        background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );

        color: white !important;

        border: none;

        border-radius: 20px;

        padding: 18px;

        font-size: 18px;

        font-weight: 700;

        transition: 0.3s ease;

        box-shadow:
        0px 0px 28px rgba(99,102,241,0.35);
    }

    .stButton button:hover {

        transform: scale(1.02);

        box-shadow:
        0px 0px 40px rgba(56,189,248,0.45);
    }

    /* =====================================
       FLASHCARD
    ===================================== */

    .flashcard {

        background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );

        border:
        1px solid rgba(56,189,248,0.12);

        border-radius: 24px;

        padding: 24px;

        margin-bottom: 24px;

        transition: 0.3s ease;

        box-shadow:
        0px 0px 30px rgba(56,189,248,0.08);
    }

    .flashcard:hover {

        transform: translateY(-6px);

        box-shadow:
        0px 0px 45px rgba(56,189,248,0.18);
    }

    /* =====================================
       TABS
    ===================================== */

    .stTabs [data-baseweb="tab"] {

        background:
        rgba(255,255,255,0.04);

        color: white !important;

        border-radius: 14px;

        padding: 12px 24px;

        font-size: 18px;

        font-weight: 700;

        margin-right: 10px;
    }

    /* =====================================
       SCROLLBAR
    ===================================== */

    ::-webkit-scrollbar {

        width: 10px;
    }

    ::-webkit-scrollbar-thumb {

        background:
        linear-gradient(
            #38bdf8,
            #818cf8
        );

        border-radius: 10px;
    }

    </style>

    <div class="animated-bg"></div>
    """,
    unsafe_allow_html=True
)

# =====================================
# GEMINI API
# =====================================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown(
        """
        # 🚀 CORTEXA
        """
    )

    st.markdown("---")

    st.markdown(
        """
        ## 🧠 What is CORTEXA?

        CORTEXA is a futuristic
        AI-powered lecture intelligence
        system that transforms YouTube
        lectures into an interactive
        learning experience.
        """
    )

    st.markdown("---")

    st.markdown(
        """
        ## ⚡ What CORTEXA Can Do

        ✅ Generate Smart Notes  
        ✅ Create AI Flashcards  
        ✅ Build Interactive Quizzes  
        ✅ Voice-Based AI Tutor  
        ✅ Understand Lectures  
        ✅ Answer Doubts Instantly  
        ✅ Improve Learning Speed  
        """
    )

    st.markdown("---")

    st.info(
        "Built using Gemini AI + Streamlit"
    )

# =====================================
# HERO SECTION
# =====================================

st.markdown(
    """
    <div class="brain-icon">
        🧠
    </div>

    <div class="hero-title">
        CORTEXA
    </div>

    <div class="hero-subtitle">
        Futuristic AI Lecture Intelligence System
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# URL INPUT
# =====================================

video_url = st.text_input(
    "📺 Paste YouTube Video URL",
    placeholder="https://youtube.com/watch?v=..."
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

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# =====================================
# VIDEO ID
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
# NOTES
# =====================================

def generate_notes(transcript):

    prompt = f"""
    Convert this lecture into:
    - Smart Notes
    - Key Concepts
    - Bullet Points
    - Easy Explanations

    Transcript:
    {transcript}
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =====================================
# FLASHCARDS
# =====================================

def generate_flashcards(transcript):

    prompt = f"""
    Create flashcards.

    Format:

    Q: Question
    A: Answer

    Transcript:
    {transcript}
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =====================================
# QUIZ
# =====================================

def generate_quiz(transcript):

    prompt = f"""
    Create multiple choice questions.

    Transcript:
    {transcript}
    """

    response = model.generate_content(
        prompt
    )

    return response.text
# =====================================
# PDF EXPORT
# =====================================

def create_pdf(title, content):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.set_font(
        "Arial",
        "B",
        20
    )

    pdf.cell(
        200,
        12,
        title,
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        size=12
    )

    clean_text = (
        content
        .replace("•", "-")
        .replace("—", "-")
        .replace("→", "->")
    )

    pdf.multi_cell(
        0,
        8,
        clean_text
    )

    file_name = (
        title
        .replace(" ", "_")
        + ".pdf"
    )

    pdf.output(file_name)

    return file_name

# =====================================
# VOICE
# =====================================

def listen_to_voice():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        st.info(
            "🎤 Listening..."
        )

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=10
        )

    try:

        text = recognizer.recognize_google(
            audio
        )

        return text

    except:

        return "Could not understand audio"

# =====================================
# GENERATE BUTTON
# =====================================

if st.button(
    "✨ Generate AI Study Material"
):

    if video_url:

        with st.spinner(
            "🧠 Processing Lecture..."
        ):

            transcript = get_transcript(
                video_url
            )

            notes = generate_notes(
                transcript
            )

            flashcards = generate_flashcards(
                transcript
            )

            quiz = generate_quiz(
                transcript
            )

            st.session_state.notes = notes
            st.session_state.flashcards = flashcards
            st.session_state.quiz = quiz
            st.session_state.transcript = transcript

        st.success(
            "🚀 Study Material Generated!"
        )

    else:

        st.warning(
            "Please enter a YouTube URL"
        )

# =====================================
# MAIN CONTENT
# =====================================

if st.session_state.notes:

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📝 Smart Notes",
            "🧠 Flashcards",
            "🧪 Quiz",
            "🤖 AI Tutor"
        ]
    )

    # =====================================
    # NOTES TAB
    # =====================================

    with tab1:

        st.write(
            st.session_state.notes
        )


       # =====================================
    # FLASHCARDS TAB
    # =====================================

    with tab2:

        st.markdown(
            """
            <style>

            .flip-card {

                background: transparent;

                width: 100%;
                height: 260px;

                perspective: 1000px;

                margin-bottom: 30px;

                cursor: pointer;
            }

            .flip-card-inner {

                position: relative;

                width: 100%;
                height: 100%;

                text-align: center;

                transition: transform 0.8s;

                transform-style: preserve-3d;
            }

            .flip-card:hover .flip-card-inner {

                transform: rotateY(180deg);
            }

            .flip-card-front,
            .flip-card-back {

                position: absolute;

                width: 100%;
                height: 100%;

                backface-visibility: hidden;

                border-radius: 24px;

                display: flex;

                align-items: center;

                justify-content: center;

                padding: 25px;

                box-sizing: border-box;
            }

            .flip-card-front {

                background:
                linear-gradient(
                    145deg,
                    rgba(30,41,59,0.95),
                    rgba(15,23,42,0.95)
                );

                border:
                1px solid rgba(56,189,248,0.14);

                box-shadow:
                0px 0px 30px rgba(56,189,248,0.08);
            }

            .flip-card-back {

                background:
                linear-gradient(
                    145deg,
                    rgba(6,95,70,0.95),
                    rgba(4,120,87,0.95)
                );

                transform: rotateY(180deg);

                border:
                1px solid rgba(16,185,129,0.2);

                box-shadow:
                0px 0px 30px rgba(16,185,129,0.08);
            }

            .flash-question {

                font-size: 30px;

                font-weight: 800;

                color: white;

                line-height: 1.5;
            }

            .flash-answer {

                font-size: 22px;

                color: white;

                line-height: 1.7;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        cards = (
            st.session_state.flashcards
            .split("Q:")
        )

        cols = st.columns(2)

        index = 0

        for card in cards:

            if "A:" in card:

                question, answer = card.split(
                    "A:",
                    1
                )

                question = (
                    question
                    .replace("**", "")
                    .strip()
                )

                answer = (
                    answer
                    .replace("**", "")
                    .strip()
                )

                with cols[index % 2]:

                    st.components.v1.html(
    f"""
    <div class="flip-card" onclick="this.classList.toggle('flipped')">

        <div class="flip-card-inner">

            <div class="flip-card-front">

                <div class="flash-question">
                    ❓ {question}
                </div>

            </div>

            <div class="flip-card-back">

                <div class="flash-answer">
                    ✨ {answer}
                </div>

            </div>

        </div>

    </div>

    <style>

    .flip-card {{

        background: transparent;

        width: 100%;
        height: 260px;

        perspective: 1000px;

        cursor: pointer;
    }}

    .flip-card-inner {{

        position: relative;

        width: 100%;
        height: 100%;

        transition: transform 0.8s;

        transform-style: preserve-3d;
    }}

    .flip-card.flipped .flip-card-inner {{

        transform: rotateY(180deg);
    }}

    .flip-card-front,
    .flip-card-back {{

        position: absolute;

        width: 100%;
        height: 100%;

        backface-visibility: hidden;

        border-radius: 24px;

        display: flex;

        align-items: center;

        justify-content: center;

        padding: 25px;

        box-sizing: border-box;
    }}

    .flip-card-front {{

        background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );

        border:
        1px solid rgba(56,189,248,0.14);

        box-shadow:
        0px 0px 30px rgba(56,189,248,0.08);
    }}

    .flip-card-back {{

        background:
        linear-gradient(
            145deg,
            rgba(6,95,70,0.95),
            rgba(4,120,87,0.95)
        );

        transform: rotateY(180deg);

        border:
        1px solid rgba(16,185,129,0.2);
    }}

    .flash-question {{

        font-size: 28px;

        font-weight: 800;

        color: white;

        text-align: center;

        line-height: 1.5;
    }}

    .flash-answer {{

        font-size: 20px;

        color: white;

        text-align: center;

        line-height: 1.7;
    }}

    </style>
    """,
    height=280
)
                    

                index += 1
        # =====================================
    # QUIZ TAB
    # =====================================

    with tab3:

        quiz_prompt = f"""
        Create 5 MCQ quiz questions.

        STRICT FORMAT:

        Question: ...
        A) ...
        B) ...
        C) ...
        D) ...
        Correct: A

        Transcript:
        {st.session_state.transcript[:12000]}
        """

        if "formatted_quiz" not in st.session_state:

            response = model.generate_content(
                quiz_prompt
            )

            st.session_state.formatted_quiz = (
                response.text
            )

        quiz_blocks = (
            st.session_state.formatted_quiz
            .split("Question:")
        )

        question_number = 0

        for block in quiz_blocks:

            if "Correct:" in block:

                lines = [
                    line.strip()
                    for line in block.split("\n")
                    if line.strip()
                ]

                question = lines[0]

                options = []

                correct = ""

                for line in lines[1:]:

                    if line.startswith(
                        ("A)", "B)", "C)", "D)")
                    ):

                        options.append(line)

                    elif line.startswith(
                        "Correct:"
                    ):

                        correct = (
                            line.replace(
                                "Correct:",
                                ""
                            )
                            .strip()
                        )

                st.markdown(
                    f"""
                    <div class="flashcard">
                        <h2>
                        ❓ {question}
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                selected = st.radio(
                    "Choose your answer:",
                    options,
                    key=f"quiz_{question_number}"
                )

                if st.button(
                    "Submit",
                    key=f"submit_{question_number}"
                ):

                    if selected.startswith(correct):

                        st.success(
                            "✅ Correct Answer!"
                        )

                        st.balloons()

                    else:

                        st.error(
                            f"❌ Wrong Answer! Correct Answer: {correct}"
                        )

                question_number += 1
    # =====================================
    # AI TUTOR TAB
    # =====================================

    with tab4:

        if st.button(
            "🎤 Speak Question"
        ):

            voice_text = listen_to_voice()

            st.session_state.current_question = (
                voice_text
            )

            st.success(
                f"You said: {voice_text}"
            )

        user_question = st.text_input(
            "Ask your doubt here:",
            key="question_box"
        )

        final_question = user_question

        if (
            st.session_state.current_question
            != ""
        ):

            final_question = (
                st.session_state.current_question
            )

        st.info(
            f"🧠 Current Question: {final_question}"
        )

        if st.button(
            "🚀 Ask AI Tutor"
        ):

            with st.spinner(
                "🤖 Thinking..."
            ):

                tutor_prompt = f"""
                You are CORTEXA,
                a futuristic AI tutor.

                STRICT RULES:
                - Answer ONLY from lecture
                - Explain clearly
                - No hallucinations

                Lecture:
                {st.session_state.transcript[:12000]}

                Student Question:
                {final_question}
                """

                response = model.generate_content(
                    tutor_prompt
                )

                st.success(
                    "Answer Generated!"
                )

                st.write(
                    response.text
                )

                st.session_state.current_question = ""
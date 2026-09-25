import streamlit as st
import numpy as np
import joblib
import base64
from pathlib import Path
from tensorflow.keras.models import load_model


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PROJECT DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# FIND BACKGROUND IMAGE
# ============================================================

possible_backgrounds = [
    "student_background.png",
    "student_background.jpg",
    "student_background.jpeg",
    "student background.png",
    "student background.jpg",
    "student background.jpeg"
]

background_path = None

for filename in possible_backgrounds:

    file_path = BASE_DIR / filename

    if file_path.exists():

        background_path = file_path

        break


# ============================================================
# ENCODE BACKGROUND IMAGE
# ============================================================

encoded_background = ""

image_type = "image/png"

if background_path is not None:

    with open(background_path, "rb") as image_file:

        encoded_background = base64.b64encode(
            image_file.read()
        ).decode()

    extension = background_path.suffix.lower()

    if extension == ".jpg" or extension == ".jpeg":

        image_type = "image/jpeg"

    else:

        image_type = "image/png"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       BACKGROUND
       ====================================================== */

    .stApp {{

        background: transparent !important;
    }}


    .stApp::before {{

        content: "";

        position: fixed;

        top: 0;
        left: 0;

        width: 100%;
        height: 100%;

        background-image:

            linear-gradient(
                rgba(10, 35, 65, 0.18),
                rgba(10, 35, 65, 0.18)
            ),

            url(
                "data:{image_type};base64,{encoded_background}"
            );

        background-size: cover;

        background-position: center;

        background-repeat: no-repeat;

        filter: blur(2px);

        transform: scale(1.03);

        z-index: -2;
    }}


    /* ======================================================
       MAIN PAGE WIDTH
       ====================================================== */

    .block-container {{

        max-width: 1080px;

        padding-top: 30px;

        padding-bottom: 50px;
    }}


    /* ======================================================
       MAIN TITLE
       ====================================================== */

    h1 {{

        text-align: center !important;

        color: #ffffff !important;

        font-size: 42px !important;

        font-weight: 850 !important;

        letter-spacing: 0.2px;

        text-shadow:
            0 3px 12px
            rgba(0, 0, 0, 0.65);

        margin-bottom: 6px;
    }}


    /* ======================================================
       SUBTITLE
       ====================================================== */

    .subtitle {{

        text-align: center;

        color: #ffffff;

        font-size: 17px;

        font-weight: 650;

        text-shadow:
            0 2px 8px
            rgba(0, 0, 0, 0.60);

        margin-bottom: 28px;
    }}


    /* ======================================================
       GLASS CONTAINERS
       ====================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {{

        background:
            rgba(255, 255, 255, 0.94) !important;

        border:
            1px solid
            rgba(255, 255, 255, 0.98) !important;

        border-radius: 22px !important;

        box-shadow:
            0 15px 45px
            rgba(0, 0, 0, 0.20);

        backdrop-filter:
            blur(18px);

        -webkit-backdrop-filter:
            blur(18px);
    }}


    /* ======================================================
       SECTION HEADINGS
       ====================================================== */

    h2 {{

        color: #075dcc !important;

        font-size: 29px !important;

        font-weight: 850 !important;

        letter-spacing: 0.2px;

        text-shadow:
            0 1px 2px
            rgba(7, 93, 204, 0.15);

        margin-bottom: 20px;
    }}


    /* ======================================================
       SMALL HEADINGS
       ====================================================== */

    h3 {{

        color: #075dcc !important;

        font-size: 25px !important;

        font-weight: 850 !important;
    }}


    /* ======================================================
       INPUT LABELS
       ====================================================== */

    label {{

        color: #174b82 !important;

        font-size: 15px !important;

        font-weight: 750 !important;
    }}


    /* ======================================================
       INPUT AREA
       ====================================================== */

    div[data-baseweb="input"] {{

        background: #ffffff !important;

        border: 2px solid #c4daf4 !important;

        border-radius: 11px !important;

        box-shadow:
            0 3px 10px
            rgba(20, 80, 150, 0.08);
    }}


    /* ======================================================
       INPUT TEXT
       ====================================================== */

    input {{

        color: #173f70 !important;

        background: #ffffff !important;

        font-weight: 700 !important;

        font-size: 15px !important;
    }}


    /* ======================================================
       INPUT +/- BUTTONS
       ====================================================== */

    button[data-testid="stNumberInputStepUp"] span,
    button[data-testid="stNumberInputStepDown"] span {{

        color: #075dcc !important;
    }}


    /* ======================================================
       PREDICTION BUTTON
       ====================================================== */

    .stButton > button {{

        width: 100%;

        height: 60px;

        border: none !important;

        border-radius: 15px !important;

        background:
            linear-gradient(
                90deg,
                #0878f9 0%,
                #4c46f5 50%,
                #792df0 100%
            ) !important;

        color: #ffffff !important;

        font-size: 18px !important;

        font-weight: 800 !important;

        box-shadow:
            0 8px 25px
            rgba(55, 80, 220, 0.35);

        transition:
            all 0.2s ease;
    }}


    /* ======================================================
       BUTTON TEXT
       ====================================================== */

    .stButton > button p {{

        color: #ffffff !important;

        font-weight: 800 !important;
    }}


    /* ======================================================
       BUTTON HOVER
       ====================================================== */

    .stButton > button:hover {{

        background:
            linear-gradient(
                90deg,
                #006eea 0%,
                #443de8 50%,
                #7020e8 100%
            ) !important;

        color: #ffffff !important;

        transform:
            translateY(-2px);

        box-shadow:
            0 12px 32px
            rgba(55, 80, 220, 0.45);
    }}


    /* ======================================================
       SUCCESS PREDICTION BOX
       ====================================================== */

    div[data-testid="stAlert"] {{

        background:
            linear-gradient(
                135deg,
                #e9fff3,
                #d8f9e9
            ) !important;

        border:
            1px solid #9be4bb !important;

        border-radius: 15px !important;

        color: #087a43 !important;

        font-weight: 800 !important;

        font-size: 17px !important;
    }}


    div[data-testid="stAlert"] p {{

        color: #087a43 !important;

        font-weight: 800 !important;
    }}


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="stMetric"] {{

        background:
            rgba(255, 255, 255, 0.96) !important;

        border:
            1px solid #c9def5 !important;

        border-radius: 15px !important;

        padding: 14px !important;

        box-shadow:
            0 5px 16px
            rgba(20, 80, 150, 0.09);
    }}


    /* ======================================================
       METRIC LABEL
       ====================================================== */

    div[data-testid="stMetricLabel"] p {{

        color: #315d8c !important;

        font-size: 14px !important;

        font-weight: 700 !important;
    }}


    /* ======================================================
       METRIC VALUE
       ====================================================== */

    div[data-testid="stMetricValue"] {{

        color: #075dcc !important;

        font-size: 25px !important;

        font-weight: 850 !important;
    }}


    /* ======================================================
       CLASS PROBABILITY NAME
       ====================================================== */

    .stProgress ~ div {{

        color: #174b82 !important;
    }}


    /* ======================================================
       ALL NORMAL TEXT
       ====================================================== */

    p {{

        color: #234d78;
    }}


    /* ======================================================
       PROBABILITY PERCENTAGE
       ====================================================== */

    .stProgress + div p {{

        color: #174b82 !important;

        font-weight: 750 !important;
    }}


    /* ======================================================
       PROGRESS BAR
       ====================================================== */

    div[data-testid="stProgress"] {{

        margin-top: -5px;

        margin-bottom: 12px;
    }}


    /* ======================================================
       REMOVE EXTRA SPACE
       ====================================================== */

    .stMarkdown {{

        margin-bottom: 4px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL FILES
# ============================================================

MODEL_PATH = (
    BASE_DIR /
    "student_performance_ann.keras"
)

SCALER_PATH = (
    BASE_DIR /
    "student_scaler.pkl"
)

ENCODER_PATH = (
    BASE_DIR /
    "student_label_encoder.pkl"
)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

try:

    model = load_model(
        MODEL_PATH
    )

    scaler = joblib.load(
        SCALER_PATH
    )

    label_encoder = joblib.load(
        ENCODER_PATH
    )

except Exception as error:

    st.error(
        "Model files could not be loaded."
    )

    st.info(
        "Please run your Jupyter Notebook completely "
        "and keep the .keras and .pkl files "
        "in the same folder as app.py."
    )

    st.stop()


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "🎓 Student Performance Prediction"
)


# ============================================================
# SUBTITLE
# ============================================================

st.markdown(
    """
    <div class="subtitle">
        Artificial Neural Network based Student Performance Prediction
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STUDENT INPUT SECTION
# ============================================================

with st.container(border=True):


    # --------------------------------------------------------
    # HEADING
    # --------------------------------------------------------

    st.subheader(
        "👤 Enter Student Details"
    )


    st.write("")


    # --------------------------------------------------------
    # TWO COLUMNS
    # --------------------------------------------------------

    left_column, right_column = st.columns(
        2,
        gap="large"
    )


    # ========================================================
    # LEFT COLUMN
    # ========================================================

    with left_column:


        study_hours = st.number_input(
            "📚 Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=6.0,
            step=0.5
        )


        previous_gpa = st.number_input(
            "📊 Previous GPA",
            min_value=0.0,
            max_value=10.0,
            value=8.0,
            step=0.1
        )


    # ========================================================
    # RIGHT COLUMN
    # ========================================================

    with right_column:


        attendance = st.number_input(
            "📅 Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=1.0
        )


        exam_score = st.number_input(
            "📝 Exam Score",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=1.0
        )


    st.write("")


    # ========================================================
    # PREDICTION BUTTON
    # ========================================================

    predict_button = st.button(
        "✨ Predict Student Performance"
    )


# ============================================================
# PREDICTION
# ============================================================

if predict_button:


    # ========================================================
    # CREATE INPUT DATA
    # ========================================================

    input_data = np.array(
        [
            study_hours,
            attendance,
            previous_gpa,
            exam_score
        ]
    ).reshape(
        1,
        -1
    )


    # ========================================================
    # SCALE INPUT
    # ========================================================

    input_scaled = scaler.transform(
        input_data
    )


    # ========================================================
    # PREDICT
    # ========================================================

    prediction = model.predict(
        input_scaled,
        verbose=0
    )


    # ========================================================
    # FIND CLASS
    # ========================================================

    predicted_index = np.argmax(
        prediction,
        axis=1
    )


    predicted_result = (
        label_encoder.inverse_transform(
            predicted_index
        )[0]
    )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = (
        float(
            np.max(prediction)
        ) * 100
    )


    st.write("")


    # ========================================================
    # RESULT SECTION
    # ========================================================

    with st.container(border=True):


        # ----------------------------------------------------
        # RESULT HEADING
        # ----------------------------------------------------

        st.subheader(
            "🎯 Predicted Performance"
        )


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        st.success(
            f"Prediction: {predicted_result}"
        )


        st.write("")


        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        st.metric(
            "Model Confidence",
            f"{confidence:.2f}%"
        )


        st.write("")


        # ====================================================
        # STUDENT DETAILS
        # ====================================================

        st.subheader(
            "📊 Student Details"
        )


        detail1, detail2, detail3, detail4 = st.columns(
            4
        )


        with detail1:

            st.metric(
                "Study Hours",
                f"{study_hours:g}"
            )


        with detail2:

            st.metric(
                "Attendance",
                f"{attendance:g}%"
            )


        with detail3:

            st.metric(
                "Previous GPA",
                f"{previous_gpa:.1f}"
            )


        with detail4:

            st.metric(
                "Exam Score",
                f"{exam_score:g}"
            )


        st.write("")


        # ====================================================
        # CLASS PROBABILITIES
        # ====================================================

        st.subheader(
            "📈 Class Probabilities"
        )


        # ----------------------------------------------------
        # DISPLAY EACH CLASS
        # ----------------------------------------------------

        for class_name, probability in zip(
            label_encoder.classes_,
            prediction[0]
        ):


            probability = float(
                probability
            )


            percentage = (
                probability * 100
            )


            # ------------------------------------------------
            # PROBABILITY ROW
            # ------------------------------------------------

            probability_col1, probability_col2 = st.columns(
                [7, 1]
            )


            with probability_col1:

                st.markdown(
                    f"""
                    <div style="
                        color:#174b82;
                        font-size:15px;
                        font-weight:750;
                        margin-bottom:3px;
                    ">
                        {class_name}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.progress(
                    probability
                )


            with probability_col2:

                st.markdown(
                    f"""
                    <div style="
                        color:#075dcc;
                        font-size:15px;
                        font-weight:800;
                        text-align:right;
                        padding-top:3px;
                    ">
                        {percentage:.2f}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )
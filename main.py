import streamlit as st
import openai
import os
from parse_hh import get_candidate_info, get_job_description
from dotenv import load_dotenv
from settings import MODEL_NAME, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT, MESSAGES, INPUTS, ENV_VARS

# Load environment variables from .env file
load_dotenv()

# Set page config
st.set_page_config(page_title=MESSAGES["TITLE"])

st.title(MESSAGES["TITLE"])

# Hide Streamlit menu and footer
hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state
if 'last_analysis_response' not in st.session_state:
    st.session_state.last_analysis_response = None
if 'job_description_parsed' not in st.session_state:
    st.session_state.job_description_parsed = None
if 'cv_data_str' not in st.session_state: # Единая переменная для строки резюме
    st.session_state.cv_data_str = None

# Try to get API key from environment variables first
openai_api_key = os.getenv(ENV_VARS["OPENAI_API_KEY"])

if not openai_api_key:
    # If not found in environment, ask user to input
    openai_api_key = st.text_input(MESSAGES["API_KEY_INPUT"], type="password")
    if not openai_api_key:
        st.warning(MESSAGES["API_KEY_MISSING"])
        st.info(MESSAGES["ENV_SETUP_HELP"])
        st.stop()

# Initialize OpenAI client
try:
    client = openai.Client(api_key=openai_api_key)
except Exception as e:
    st.error(MESSAGES["INIT_ERROR"].format(error=str(e)))
    st.stop()

def request_gpt(sistem_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": sistem_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка при запросе к OpenAI: {str(e)}")
        return None

job_description_url = st.text_input(INPUTS["JOB_URL"])
cv_url = st.text_input(INPUTS["CV_URL"])

if st.button("Оценить резюме"):
    # Clear previous results
    st.session_state.last_analysis_response = None
    st.session_state.job_description_parsed = None
    st.session_state.cv_data_str = None # Очищаем строку резюме

    if not job_description_url or not cv_url:
        st.warning(MESSAGES["URL_MISSING"])
        st.stop()
        
    with st.spinner(MESSAGES["PROCESSING"]):
        try:
            job_description = get_job_description(job_description_url)
            # get_candidate_info теперь возвращает строку
            cv_data_string = get_candidate_info(cv_url) 
            
            st.session_state.job_description_parsed = job_description
            st.session_state.cv_data_str = cv_data_string # Сохраняем строку резюме

            user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{st.session_state.cv_data_str}"
            response = request_gpt(SYSTEM_PROMPT, user_prompt)
            
            st.session_state.last_analysis_response = response

        except Exception as e:
            st.error(MESSAGES["PROCESSING_ERROR"].format(error=str(e)))
            # Очищаем все в случае ошибки
            st.session_state.last_analysis_response = None
            st.session_state.job_description_parsed = None
            st.session_state.cv_data_str = None

# Display expanders and analysis result
if st.session_state.job_description_parsed:
    with st.expander(MESSAGES["JOB_DESCRIPTION_TITLE"], expanded=False):
        st.markdown(st.session_state.job_description_parsed, unsafe_allow_html=True)

if st.session_state.cv_data_str: # Отображаем, если есть строка резюме
    with st.expander(MESSAGES["CV_TITLE"], expanded=False):
        st.markdown(st.session_state.cv_data_str, unsafe_allow_html=True)

if st.session_state.last_analysis_response:
    st.subheader(MESSAGES["ANALYSIS_TITLE"])
    st.markdown(st.session_state.last_analysis_response, unsafe_allow_html=True)

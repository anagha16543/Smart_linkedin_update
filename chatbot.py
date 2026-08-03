import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from prompts import SALES_PROMPTS
from rag import retrieve_context


# --------------------------------------
# Initialize LLM
# --------------------------------------
def get_llm():

    api_key = st.secrets["GROQ_API_KEY"]

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

    return llm


# --------------------------------------
# Prompt Template
# --------------------------------------
PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "{system_prompt}"
        ),
        (
            "human",
            "{question}"
        )
    ]
)


# --------------------------------------
# Chat Function
# --------------------------------------
def ask_question(persona, question):

    context = retrieve_context(question)

    system_prompt = SALES_PROMPTS[persona].format(
        context=context
    )

    llm = get_llm()

    chain = (
        PROMPT
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(
        {
            "system_prompt": system_prompt,
            "question": question
        }
    )

    return answer


# --------------------------------------
# Chat History
# --------------------------------------
def initialize_chat():

    if "messages" not in st.session_state:

        st.session_state.messages = []


def add_user_message(message):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )


def add_assistant_message(message):

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message
        }
    )


def display_chat():

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

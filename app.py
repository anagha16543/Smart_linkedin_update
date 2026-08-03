import streamlit as st

from chatbot import (
    ask_question,
    initialize_chat,
    display_chat,
    add_user_message,
    add_assistant_message
)

from rag import update_knowledge_base


# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="PragyanAI AI Counsellor",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.title("🤖 PragyanAI AI Counsellor")

st.markdown(
"""
Ask anything about:

- 📘 AI Program
- 💰 Fees
- 🎯 Placements
- 📚 Curriculum
- 🏫 College Partnerships
- 💼 Enterprise Hiring
"""
)


# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("Settings")


persona = st.sidebar.selectbox(

    "Choose AI Persona",

    [

        "PragyanAI Student Counselor",

        "PragyanAI Institutional / CoE Advisor",

        "PragyanAI Enterprise AI & Placement Lead"

    ]

)


uploaded_files = st.sidebar.file_uploader(

    "Upload PDF / Excel",

    type=["pdf", "xlsx", "xls"],

    accept_multiple_files=True

)


if st.sidebar.button("Update Knowledge Base"):

    if uploaded_files:

        msg = update_knowledge_base(uploaded_files)

        st.sidebar.success(msg)

    else:

        st.sidebar.warning("Upload at least one file.")


# -------------------------------------------------------
# Chat
# -------------------------------------------------------

initialize_chat()

display_chat()


question = st.chat_input("Ask a question...")


if question:

    add_user_message(question)

    with st.chat_message("user"):

        st.markdown(question)


    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = ask_question(

                persona,

                question

            )

            st.markdown(answer)


    add_assistant_message(answer)


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()

st.caption(

    "Powered by LangChain • FAISS • HuggingFace • Groq • Streamlit"

)

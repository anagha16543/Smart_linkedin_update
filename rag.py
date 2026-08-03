import os
import pandas as pd

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# -----------------------------
# Embedding Model
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = None


# -----------------------------
# Load Documents
# -----------------------------
def load_documents(file_paths=None):
    docs = []

    # Uploaded files
    if file_paths:
        for file in file_paths:

            path = file

            # PDF
            if path.endswith(".pdf"):
                loader = PyPDFLoader(path)
                docs.extend(loader.load())

            # Excel
            elif path.endswith(".xlsx") or path.endswith(".xls"):

                df = pd.read_excel(path)

                for _, row in df.iterrows():

                    text = " | ".join(
                        [f"{col}: {row[col]}" for col in df.columns]
                    )

                    docs.append(
                        Document(
                            page_content=text,
                            metadata={"source": os.path.basename(path)}
                        )
                    )

    # Default FAQ
    if os.path.exists("pragyan_faq_prices.xlsx"):

        df = pd.read_excel("pragyan_faq_prices.xlsx")

        for _, row in df.iterrows():

            text = " | ".join(
                [f"{col}: {row[col]}" for col in df.columns]
            )

            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": "pragyan_faq_prices.xlsx"}
                )
            )

    # Fallback
    if len(docs) == 0:

        docs = [

            Document(
                page_content="""
PragyanAI offers a 6 Month Offline Training
followed by a 12 Month Internship &
Placement Program.
"""
            ),

            Document(
                page_content="""
Founding Batch Fee:
₹50,000 Initial Fee
₹50,000 Success Fee after Placement.
"""
            )

        ]

    return docs


# -----------------------------
# Build Vector Store
# -----------------------------
def build_vectorstore(file_paths=None):

    global vectorstore

    docs = load_documents(file_paths)

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    return vectorstore


# -----------------------------
# Retrieve Context
# -----------------------------
def retrieve_context(query, k=4):

    global vectorstore

    if vectorstore is None:
        build_vectorstore()

    docs = vectorstore.similarity_search(
        query,
        k=k
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context


# -----------------------------
# Update Knowledge Base
# -----------------------------
def update_knowledge_base(uploaded_files):

    paths = []

    for file in uploaded_files:

        temp_path = file.name

        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())

        paths.append(temp_path)

    build_vectorstore(paths)

    return f"Knowledge Base updated with {len(paths)} uploaded file(s)."

import streamlit as st
from app.pipeline.rag_pipeline import RAGPipeline
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -------------------------
# Session State
# -------------------------

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="InsightForge",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("📄 InsightForge")
st.sidebar.write("AI Research Assistant")

# Clear Chat Button
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# -------------------------
# Main UI
# -------------------------

st.title("📄 InsightForge")
st.subheader("AI Research Assistant")

st.caption(
    "Upload a PDF and ask questions using Retrieval-Augmented Generation (RAG)."
)

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

# -------------------------
# Upload & Index PDF
# -------------------------

if uploaded_file is not None:

    save_path = os.path.join(
        "data/uploads",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ {uploaded_file.name} uploaded successfully!")

    with st.spinner("Indexing PDF..."):

        pipeline = RAGPipeline()

        pipeline.index_pdf(save_path)

        st.session_state.pipeline = pipeline

    st.success(f"✅ {uploaded_file.name} indexed successfully!")
    if st.button("📝 Summarize Document"):

        if st.session_state.pipeline is None:

            st.warning("Please upload a PDF first.")

        else:

            with st.spinner("Generating summary..."):

                summary = st.session_state.pipeline.summarize()

        st.subheader("📖 Document Summary")

        st.info(summary)

    if st.button("🔑 Extract Keywords"):

        if st.session_state.pipeline is None:

            st.warning("Please upload a PDF first.")

        else:

            with st.spinner("Extracting keywords..."):

                keywords = st.session_state.pipeline.keywords()

        st.subheader("🔑 Keywords")

        st.success(keywords)

    if st.button("📘 Generate Study Notes"):

        if st.session_state.pipeline is None:

            st.warning("Please upload a PDF first.")

        else:

            with st.spinner("Generating study notes..."):

                notes = st.session_state.pipeline.study_notes()

        st.subheader("📘 Study Notes")

        st.markdown(notes)

    if st.button("📚 Generate Literature Review"):

        if st.session_state.pipeline is None:

            st.warning("Please upload a PDF first.")

        else:

            with st.spinner("Generating literature review..."):

                review = st.session_state.pipeline.literature_review()

        st.subheader("📚 Literature Review")

        st.markdown(review)

    if st.button("🔍 Find Research Gaps"):

        if st.session_state.pipeline is None:

            st.warning("Please upload a PDF first.")

        else:

            with st.spinner("Analyzing research gaps..."):

                gaps = st.session_state.pipeline.research_gap()

        st.subheader("🔍 Research Gap Analysis")

        st.markdown(gaps)

    # Sidebar Information

    st.sidebar.success("PDF Indexed")

    st.sidebar.write(f"**File:** {uploaded_file.name}")
    st.sidebar.write(f"**Pages:** {pipeline.pages}")
    st.sidebar.write(f"**Chunks:** {len(pipeline.chunks)}")

    # Metrics

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pages", pipeline.pages)

    with col2:
        st.metric("Chunks", len(pipeline.chunks))

    with col3:
        st.metric("Words", len(pipeline.text.split()))

    # Document Information

    with st.expander("📄 Document Information"):

        st.write(f"**Filename:** {pipeline.filename}")
        st.write(f"**Pages:** {pipeline.pages}")
        st.write(f"**Words:** {len(pipeline.text.split())}")
        st.write(f"**Characters:** {len(pipeline.text)}")
        st.write(f"**Chunks:** {len(pipeline.chunks)}")

# -------------------------
# Ask Questions
# -------------------------

question = st.text_input(
    "Ask a question"
)

if question.strip() == "":
    st.info(
        """
Try asking:

• Summarize this document

• What are the key skills?

• What internship experience is mentioned?

• Give me the main points
"""
    )

if st.button("🚀 Ask InsightForge"):

    if st.session_state.pipeline is None:

        st.warning("Please upload a PDF first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating answer..."):

            answer, sources = st.session_state.pipeline.ask(question)

        st.markdown("## 🤖 Answer")

        st.success(answer)

        # Source Chunks

        st.subheader("📑 Source Chunks")

        for i, source in enumerate(sources):

            with st.expander(f"Chunk {i+1}"):

                st.write(source)

        st.session_state.history.append(
            (question, answer)
        )

# -------------------------
# Chat History
# -------------------------

if st.session_state.history:

    st.subheader("💬 Chat History")

    for q, a in st.session_state.history:

        with st.container():

            st.markdown(f"### ❓ {q}")

            st.success(a)

            st.divider()

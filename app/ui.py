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

if "summary" not in st.session_state:
    st.session_state.summary = None

if "keywords" not in st.session_state:
    st.session_state.keywords = None

if "study_notes" not in st.session_state:
    st.session_state.study_notes = None

if "literature_review" not in st.session_state:
    st.session_state.literature_review = None

if "research_gap" not in st.session_state:
    st.session_state.research_gap = None

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

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

    save_path = os.path.join("data/uploads", uploaded_file.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ {uploaded_file.name} uploaded successfully!")

    with st.spinner("Indexing PDF..."):

        pipeline = RAGPipeline()
        pipeline.index_pdf(save_path)

        st.session_state.pipeline = pipeline

        # Reset workspace
        st.session_state.summary = None
        st.session_state.keywords = None
        st.session_state.study_notes = None
        st.session_state.literature_review = None
        st.session_state.research_gap = None
        st.session_state.last_answer = None
        st.session_state.last_sources = []

    st.success(f"✅ {uploaded_file.name} indexed successfully!")


# -------------------------
# Everything below uses the indexed pipeline
# -------------------------

if st.session_state.pipeline is not None:

    pipeline = st.session_state.pipeline

    # -------------------------
    # Summary
    # -------------------------

    if st.button("📝 Summarize Document"):

        with st.spinner("Generating summary..."):
            st.session_state.summary = pipeline.summarize()

    if st.session_state.summary:

        st.subheader("📖 Document Summary")
        st.info(st.session_state.summary)

    # -------------------------
    # Keywords
    # -------------------------

    if st.button("🔑 Extract Keywords"):

        with st.spinner("Extracting keywords..."):
            st.session_state.keywords = pipeline.keywords()

    if st.session_state.keywords:

        st.subheader("🔑 Keywords")
        st.success(st.session_state.keywords)

    # -------------------------
    # Study Notes
    # -------------------------

    if st.button("📘 Generate Study Notes"):

        with st.spinner("Generating study notes..."):
            st.session_state.study_notes = pipeline.study_notes()

    if st.session_state.study_notes:

        st.subheader("📘 Study Notes")
        st.markdown(st.session_state.study_notes)

    # -------------------------
    # Literature Review
    # -------------------------

    if st.button("📚 Generate Literature Review"):

        with st.spinner("Generating literature review..."):
            st.session_state.literature_review = pipeline.literature_review()

    if st.session_state.literature_review:

        st.subheader("📚 Literature Review")
        st.markdown(st.session_state.literature_review)

    # -------------------------
    # Research Gap
    # -------------------------

    if st.button("🔍 Find Research Gaps"):

        with st.spinner("Analyzing research gaps..."):
            st.session_state.research_gap = pipeline.research_gap()

    if st.session_state.research_gap:

        st.subheader("🔍 Research Gap Analysis")
        st.markdown(st.session_state.research_gap)

    # -------------------------
    # Sidebar Information
    # -------------------------

    st.sidebar.success("✅ PDF Indexed")

    if hasattr(pipeline, "filename"):
        st.sidebar.write(f"**File:** {pipeline.filename}")

    st.sidebar.write(f"**Pages:** {pipeline.pages}")
    st.sidebar.write(f"**Chunks:** {len(pipeline.chunks)}")

    st.sidebar.divider()
    st.sidebar.subheader("📊 Workspace Status")

    st.sidebar.write(
        "📖 Summary: " + ("✅" if st.session_state.summary else "❌")
    )

    st.sidebar.write(
        "🔑 Keywords: " + ("✅" if st.session_state.keywords else "❌")
    )

    st.sidebar.write(
        "📘 Study Notes: " + ("✅" if st.session_state.study_notes else "❌")
    )

    st.sidebar.write(
        "📚 Literature Review: "
        + ("✅" if st.session_state.literature_review else "❌")
    )

    st.sidebar.write(
        "🔍 Research Gap: "
        + ("✅" if st.session_state.research_gap else "❌")
    )

    # -------------------------
    # Metrics
    # -------------------------

    st.subheader("📊 Document Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 Pages", pipeline.pages)

    with col2:
        st.metric("🧩 Chunks", len(pipeline.chunks))

    with col3:
        st.metric("📝 Words", len(pipeline.text.split()))

    with col4:
        st.metric("🔤 Characters", len(pipeline.text))
# -------------------------
# Ask Questions
# -------------------------

st.subheader("❓ Ask InsightForge")

question = st.text_input("Ask a question")

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

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating answer..."):

            answer, sources = pipeline.ask(question)

        st.session_state.last_answer = answer
        st.session_state.last_sources = sources

        st.session_state.history.append((question, answer))

# -------------------------
# Latest Answer
# -------------------------

if st.session_state.last_answer:

    st.markdown("## 🤖 Latest Answer")

    st.success(st.session_state.last_answer)

    st.subheader("📑 Source Chunks")

    for i, source in enumerate(st.session_state.last_sources):

        with st.expander(f"Chunk {i + 1}"):

            st.write(source)

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

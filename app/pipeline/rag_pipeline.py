from app.pdf.parser import extract_text
from app.rag.chunker import chunk_text
from app.embeddings.embedder import create_embeddings
from app.database.vector_store import (
    store_embeddings,
    search,
    clear_collection,
)
from app.llm.generator import generate_answer
from app.llm.summarizer import summarize_document
from app.llm.keyword_extractor import extract_keywords
from app.llm.study_notes import generate_study_notes
from app.llm.literature_review import generate_literature_review
from app.llm.research_gap import generate_research_gap
import os


class RAGPipeline:

    def __init__(self):
        self.filename = None
        self.text = None
        self.pages = None
        self.chunks = None
        self.embeddings = None

    def index_pdf(self, pdf_path):

        self.filename = os.path.basename(pdf_path)

        self.text, self.pages = extract_text(pdf_path)

        self.chunks = chunk_text(self.text)

        self.embeddings = create_embeddings(self.chunks)

        clear_collection()

        store_embeddings(self.chunks, self.embeddings)

    def ask(self, question):

        question_embedding = create_embeddings([question])[0]

        results = search(question_embedding)

        context = "\n\n".join(results["documents"][0])

        answer = generate_answer(question, context)

        print(type(answer))
        print(type(results["documents"][0]))
        print(results["documents"][0])

        return answer, results["documents"][0]

    def summarize(self):

        return summarize_document(self.text)

    def keywords(self):

        return extract_keywords(self.text)

    def study_notes(self):

        return generate_study_notes(self.text)

    def literature_review(self):

        return generate_literature_review(self.text)

    def research_gap(self):

        return generate_research_gap(self.text)

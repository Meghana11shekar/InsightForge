from app.pdf.parser import extract_text
from app.rag.chunker import chunk_text
from app.embeddings.embedder import create_embeddings
from app.database.vector_store import store_embeddings
from app.database.vector_store import search
from app.llm.generator import generate_answer

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

        store_embeddings(self.chunks, self.embeddings)

    def ask(self, question):

        question_embedding = create_embeddings([question])[0]

        results = search(question_embedding)

        context = "\n\n".join(results["documents"][0])

        answer = generate_answer(question, context)

        return answer

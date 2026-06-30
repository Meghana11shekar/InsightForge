from app.pdf.parser import extract_text
from app.rag.chunker import chunk_text
import os
from app.embeddings.embedder import create_embeddings
from app.database.vector_store import store_embeddings
from app.database.vector_store import search
from app.llm.generator import generate_answer
from app.agents.planner import PlannerAgent

pdf_path = "data/uploads/sample.pdf"

text, pages = extract_text(pdf_path)

chunks = chunk_text(text)

filename = os.path.basename(pdf_path)

embeddings = create_embeddings(chunks)

store_embeddings(chunks, embeddings)

question = "Who are the major cyber attackers?"

question_embedding = create_embeddings([question])[0]

results = search(question_embedding)

context = "\n\n".join(results["documents"][0])

answer = generate_answer(question, context)

planner = PlannerAgent()

task = input("What do you want to do?\n")

plan = planner.plan(task)

print("=" * 50)
print("📄 InsightForge")
print("=" * 50)

print(f"File: {filename}")
print(f"Pages: {pages}")
print(f"Words: {len(text.split())}")
print(f"Characters: {len(text)}")
print(f"Chunks Created: {len(chunks)}")

print("\nFirst Chunk\n")

print(chunks[0])
print(f"Embeddings Generated: {len(embeddings)}")

print()

print(len(embeddings[0]))

print("\nFirst 10 values of the first embedding:")
print(embeddings[0][:10])

print("Stored successfully in ChromaDB!")

print("\nTop Retrieved Chunks:\n")

for i, doc in enumerate(results["documents"][0]):
    print(f"Result {i+1}")
    print(doc)
    print("-" * 60)

print("\nQuestion:")
print(question)

print("\nAnswer:\n")

print(answer)


print()

print(plan)

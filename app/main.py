from app.pipeline.rag_pipeline import RAGPipeline
from app.agents.planner import PlannerAgent

# Create the pipeline
pipeline = RAGPipeline()

# Index the PDF
pipeline.index_pdf("data/uploads/sample.pdf")

# Ask a question to the RAG system
question = "Who are the major cyber attackers?"

answer = pipeline.ask(question)

# Planner Agent
planner = PlannerAgent()

task = input("What do you want to do?\n")

plan = planner.plan(task)

# Display information
print("=" * 50)
print("📄 InsightForge")
print("=" * 50)

print(f"File: {pipeline.filename}")
print(f"Pages: {pipeline.pages}")
print(f"Words: {len(pipeline.text.split())}")
print(f"Characters: {len(pipeline.text)}")
print(f"Chunks Created: {len(pipeline.chunks)}")

print("\nFirst Chunk:\n")
print(pipeline.chunks[0])

print(f"\nEmbeddings Generated: {len(pipeline.embeddings)}")
print(f"Embedding Size: {len(pipeline.embeddings[0])}")

print("\nFirst 10 values of the first embedding:")
print(pipeline.embeddings[0][:10])

print("\nStored successfully in ChromaDB!")

print("\nQuestion:")
print(question)

print("\nAnswer:\n")
print(answer)

print("\nPlanner Output:\n")
print(plan)

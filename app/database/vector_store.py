import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(
    name="research_papers"
)


def clear_collection():

    global collection

    try:
        client.delete_collection("research_papers")
    except:
        pass

    collection = client.get_or_create_collection(
        name="research_papers"
    )


def store_embeddings(chunks, embeddings):

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        collection.add(

            ids=[f"chunk_{i}"],

            documents=[chunk],

            embeddings=[embedding]

        )


def search(query_embedding, n_results=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results

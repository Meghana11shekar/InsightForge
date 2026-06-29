import ollama


def create_embeddings(chunks):

    embeddings = []

    for chunk in chunks:

        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )

        embeddings.append(response["embedding"])

    return embeddings

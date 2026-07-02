import chromadb
from chromadb.utils import embedding_functions

# This means chroma writes everything on the disk in this folder
# even if you stop server later on your uploaded document are still there
client = chromadb.PersistentClient(path ="./data/chroma_db")

# creating an embedding fn sth chroma can call automatically everytime 
# we add or search to turn text to vector
#embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name ="all-MiniLM-L6-v2")

# Collection in chroma db is like a table in database
# get_or_create_collection - if a collection named documents already exists reuse it else create a new one
collection = client.get_or_create_collection(name ="documents")

# add_chunks() - saving chunks to a vector store
def add_chunks(doc_id:str , chunks: list[str]):
    # Create a unique id for every chunk
    # Chromadb require every stored item to have a unique id
    ids = [f"{doc_id}{i}" for i in range(len(chunks))]
    metadatas = [{"source":doc_id, "chunk_index":i} for i in range(len(chunks))]
    # Actually inserts data into chroma db
    # document = chunks - the raw thext gets embedded automatically using embedding_fn
    collection.add(documents =chunks, metadatas = metadatas, ids =ids)
    #Return the count of chunks that were added
    return len(chunks)

# search_chunks()- finding the closes chunk to a question
# query is the question text top k - how many of the closes chunks to return
def search_chunks(query:str, top_k:int = 4):
    return collection.query(query_texts =[query], n_results = top_k)



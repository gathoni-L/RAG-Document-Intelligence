import os
from dotenv import load_dotenv #Making it able to read
from groq import Groq
# from openai import openai

# Import functions from python-dotenv library. This function reads a file called .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Looks up the environment variable named grok api key

def build_prompt(question:str, chunks:list[str], metadatas:list[dict]):
    blocks =[] # To hold each chunk
    #(zip(chunk,metadatas))- pairs each chunk with its metadata dict
    for i, (chunk, meta) in enumerate(zip(chunks,metadatas), start=1): # enumerate adds a counter to our iterable
        # meta["source"]- the file name eg company.txt
        # meta["chunk_index" - which chunk number within that file
        blocks.append(f"[Source{i}:{meta["source"]}, chunk{meta["chunk_index"]}]\n{chunk}")
        context = "\n\n".join(blocks)  # It joins all the blocks into 1 big string with a blank line between each block
        # For the above context becomes knowledge base you hand to the llm

        # This builds and returns a complete prompt
        return (
            "Answer the questions using the context below."
            "Cite sources using [Source N]. If the answer is not in the"
            "context say you dont have enough information -do not gues. \n\n"
            f"Context:\n{context}\n\nQuestion::{question}\n\nAnswer:"
        )
    
    # search_results we are getting dictionaries from chroma
def generate_answer(question:str, search_results:dict):
        chunks = search_results["documents"][0]
        metadatas = search_results["metadatas"][0]
        # Safety guard if no file has been uploaded
        if not chunks:
            return {"answer":"No documents have been uploaded yet", "sources":[]}
        prompt =build_prompt(question, chunks, metadatas)
        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            max_tokens = 500,
            messages = [{"role":"user","content":prompt}]
        )

        answer_text = response.choices[0].message.content
        sources = [{"sources":m["source"],"chunk_index":m["chunk_index"]}for m in metadatas]
        # answer - The llms generated response
        # sources the list of source reference used to generate the answer
        return {"answer":answer_text,"sources":sources}

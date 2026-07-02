# io lets us treat raw bytes in memory as if they were a file. We need because the uploaded file arrives as bytes
#  and our pdf reader excepts sth behaving like a file 
import io
from pypdf import PdfReader


# def extract takes the original filename and raw bytes of uploaded file
def extract_text(filename:str, file_bytes:bytes) -> str:
    if filename.lower().endswith(".pdf"):
        reader= PdfReader(io.BytesIO(file_bytes))
        return "/n".join(page.extract_text() or "" for page in reader.pages)
    return file_bytes.decode("utf-8", errors="ignore")


def chunk_text(text:str,chunk_size:int =300, overlap:int =50) -> list[str]:
    words=text.split()
    chunks =[]
    start = 0 # start chunk
    while start < len(words):
        end = start + chunk_size # End of chunk
        chunk = " ".join(words[start:end]) # Making the chunk
        if chunk.strip(): # removed white spaces from chunks
            chunks.append(chunk) # added chunks to the list
        start += chunk_size - overlap
    return chunks
        
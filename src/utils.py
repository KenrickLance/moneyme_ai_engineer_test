import pymupdf
import pymupdf4llm

from langchain_text_splitters import MarkdownTextSplitter
from urllib.request import urlopen
    
def chunk_pdf(url, chunk_size=1000, chunk_overlap=100):
    with urlopen(url) as response:
        pdf_data = response.read()

     # Convert PDF to Markdown format
    doc = pymupdf.Document(stream=pdf_data)
    md_text = pymupdf4llm.to_markdown(doc)

    # Split the Markdown text into chunks
    splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    md_splits = splitter.split_text(md_text)

    return md_splits
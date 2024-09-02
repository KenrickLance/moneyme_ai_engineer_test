import os

import chromadb

from openai import OpenAI

import prompts

from utils import chunk_pdf
from db import sqlite_con, sqlite_cur, add_conversation_message, get_conversation_history

from dotenv import load_dotenv
load_dotenv(override=True)

class Dialog:
    def __init__(self):
        # Initialize OpenAI and ChromaDB clients
        self.openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.chat_model = os.environ.get('OPENAI_CHAT_MODEL')
        self.embedding_model = os.environ.get('OPENAI_EMBEDDING_MODEL')
        self.chroma_client = chromadb.PersistentClient(path='vectordb')
        self.collection = self.chroma_client.get_or_create_collection(name=f'{os.environ.get("VECTORDB_COLLECTION_NAME")}_collection')

        # Check if the PDF data has been loaded into the vector database; if not, load it
        res = sqlite_cur.execute(f'''SELECT finished FROM vectordb_collections WHERE collection_name='{os.environ.get("VECTORDB_COLLECTION_NAME")}_collection' ''')
        if res.fetchone() is None:
            self.load_vector_db()
        sqlite_cur.execute(f'''INSERT INTO vectordb_collections (collection_name, finished) VALUES (?, ?) ''', (f'{os.environ.get("VECTORDB_COLLECTION_NAME")}_collection', True))
        sqlite_con.commit()

    def query(self, content, conversation_id):
        # Generate embeddings with the content and query vectordb for relevent documents
        response = self.openai_client.embeddings.create(input=[content], model='text-embedding-3-large')
        embedding = response.data[0].embedding
        documents = self.collection.query(query_embeddings=embedding, n_results=20)['documents'][0]
        context = 'Here are some snippets that are relevant to the user query:\n=====\n'.join(documents)

        # Retrieve the conversation history if a conversation_id is provided
        if conversation_id is not None:
            history_messages = get_conversation_history(conversation_id)
        else:
            history_messages = []

        # Call openai chatcompletion
        response = self.openai_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': prompts.system_prompt},
                *prompts.post_system_instructions,
                {'role': 'assistant', 'content': context},
                *history_messages,
                {'role': 'user', 'content': content}
            ]
        )
        
        # If a conversation_id is provided, save the user query and the chatbot's response
        if conversation_id is not None:
            add_conversation_message(conversation_id, {'role': 'user', 'content': content})
            add_conversation_message(conversation_id, {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        return response.choices[0].message.content

    def load_vector_db(self):
        # Chunk PDF, create embeddings for each chunk, and load onto vectordb
        print('CHUNKING PDF...')
        chunks = chunk_pdf(os.environ.get('PDF_KNOWLEDGE_BASE_URL'))
        print('CREATING EMBEDDINGS...')
        response = self.openai_client.embeddings.create(input=chunks, model='text-embedding-3-large')
        embeddings = [x.embedding for x in response.data]
        print('LOADING ONTO VECTORDB...')
        self.collection.upsert(documents=chunks, embeddings=embeddings, ids=[f'{os.environ.get("VECTORDB_COLLECTION_NAME")}_{i}' for i in range(len(chunks))])

        
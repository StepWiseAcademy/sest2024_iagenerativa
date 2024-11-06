# Processamento de arquvios
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

# Modeles de Embedding
from langchain_ollama import OllamaEmbeddings

# Chroma DB
from langchain_chroma import Chroma

# Variáveis de Ambiente
import os
import dotenv

# Outros
import shutil
import argparse

dotenv.load_dotenv('backend/.env.paths')

CHROMA_FILES = os.environ.get('CHROMA_FILES')
DOCUMENTS = os.environ.get('DOCUMENTS')

# Carrega os documentos presentes no diretório
def load_documents():
    document_loader = PyPDFDirectoryLoader(DOCUMENTS)
    return document_loader.load()

# Divide o documento em chunks de 800 com sobreposição de 80 caractéres
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

# Prepara o modelo de embeding
def get_embedding_function():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return embeddings

# Limpa a base
def clear_database():
    if os.path.exists(CHROMA_FILES):
        shutil.rmtree(CHROMA_FILES)

# Calcula o Chunk Id para cada um dos segmentos de texto
def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

# Adiciona os chuncks ao Chroma DB
def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_FILES, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            chunk.page_content = "search_document: "+chunk.page_content
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")

def get_top5(query_text):

    db = Chroma(
        persist_directory=CHROMA_FILES, 
        embedding_function=get_embedding_function()
    )

    similarity_results = db.similarity_search_with_score("search_query: "+query_text, k=3)
    context_text = [doc.page_content for doc, _score in similarity_results]

    return context_text

def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    

if __name__ == "__main__":
    
    main()

    print(get_top5('What is self attention?'))
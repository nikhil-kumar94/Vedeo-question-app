from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
import pytube
from pytube.exceptions import PytubeError
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma,FAISS
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain_openai import OpenAIEmbeddings

# from langchain import FAISS
from decouple import config
from langchain_openai import OpenAI,ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def get_response(docs,question,SECRET_KEY):
    embeddings = OpenAIEmbeddings(openai_api_key=SECRET_KEY)
    docs_texts = [doc.page_content for doc in docs]
    faiss = FAISS.from_texts(docs_texts, embeddings)
    docs_db = faiss.similarity_search(question)
    relevant_info = "\n".join([doc.page_content for doc in docs_db])
    llm = ChatOpenAI(openai_api_key=SECRET_KEY)
    messages = [
        SystemMessage(
            content="You are Jarvis, a helpful AI assistant. Answer the user's question based on the information provided."
        ),
        HumanMessage(
            content=f"Question: {question}\n\nUse this data to respond: {relevant_info}"
        )
    ]
    ai_msg = llm.invoke(messages)
    print(ai_msg.content)
    return ai_msg.content



def get_video_info(url,question,key):
    try:
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=True,
            transcript_format=TranscriptFormat.CHUNKS,
    chunk_size_seconds=30,
        )
        doc = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=4)
        docs = text_splitter.split_documents(doc)
     
    except PytubeError as e:
        print(f"Error fetching video info: {str(e)}")
        print("Try updating pytube or check the video URL.")


    res = get_response(docs,question,key)
    return res


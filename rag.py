from dotenv import load_dotenv
from langchain_classic.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_chroma import Chroma
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

Chunk_size = 400
Embedding_model = "sentence-transformers/all-mpnet-base-v2"
VectorStore_DIR  =Path(__file__).parent/"resources/vectorstore"
Collection_name = "real_estate"

llm = None
vector_store = None

def initialize_components() :
    global llm , vector_store
    if llm is None:
        llm = ChatGroq(model= "llama-3.3-70b-versatile" , temperature = 0.9 , max_tokens = 500)
    if vector_store is None:
        ef =  HuggingFaceEmbeddings(
            model_name = Embedding_model,
            model_kwargs = {}
        )
        vector_store = Chroma(
            collection_name =  Collection_name,
            embedding_function = ef ,
            persist_directory = str(VectorStore_DIR)
        )

def process_urls(urls):
   """
   :param urls: input urls
   :return:
   """
   yield "Initialize components"
   initialize_components()

   vector_store.reset_collection()
   yield "Load Data"

   loader = UnstructuredURLLoader(urls = urls)
   data=loader.load()
   yield "Split Data"

   text_splitter = RecursiveCharacterTextSplitter(
       separators = ["/n/n","/n",",","."],
       chunk_size =Chunk_size,
       chunk_overlap=50

   )
   docs = text_splitter.split_documents(data)
   docs = [doc for doc in docs if doc.page_content.strip()]
   yield "Add Text to Vector DB"

   vector_store.add_documents(docs)
   yield "Done adding documents to Vector DB"

def generate_answer(query):
    if not vector_store :
        raise RuntimeError("Vector Database not initialized")
    chain = RetrievalQAWithSourcesChain.from_llm(llm = llm , retriever = vector_store.as_retriever())
    result = chain.invoke({"question": query} , return_only_outputs = True)
    sources = result.get("sources"," ")
    return result ['answer'] , sources



if __name__=="__main__" :
    urls = [
        "https://www.realestatenews.com/2026/03/20/hope-for-sub-6-mortgages-evaporates-as-rates-jump-again"

    ]

    process_urls(urls)
    answer , sources = generate_answer("Tell me what was the 30 year fixed mortgage rate along with the date ")
    print (f" Answer {answer}")
    print (f"Source {sources}")


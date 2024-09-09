from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()


class Question_and_Answer:
    '''
    # Initialize the llm , loader, 
    # Initialize the text-spliter embedding
    
    '''

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model ="gemini-1.5-pro", temperature=.3, max_tokens= 500)
        self.loader = PyPDFLoader("sports.pdf")
        self.text_spliter = RecursiveCharacterTextSplitter(chunk_size = 500)
        self.embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")


    def question(self, ques):
        data = self.loader.load()
        docs = self.text_spliter.split_documents(data)
        vectorstore = Chroma.from_documents(documents=docs, embedding=self.embedding)

        retriever = vectorstore.as_retriever(search_type ="similarity", search_kwargs = {"k":5})


        system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ('system', system_prompt),
                ('human','{input}')
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        response = rag_chain.invoke({"input": ques})
        return response["answer"]

        print(response)
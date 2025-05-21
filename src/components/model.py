
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings;
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from src.exception.exception_base import ProjectException
from langchain_community.vectorstores import FAISS
import sys
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def __path__():
    return os.path.join(os.getcwd(),'faiss-lib')


def get_conversational_chain(model_name):
    try:
        prompt_template = """  
            Hello! 😊 Let's get straight to your question.  
            - Explore greetings.
            - I will answer **clearly and concisely** using only the provided context.  
            - If the answer is in the context, **I'll respond directly** in a **point format**.  
            - If the answer is **not available**, I'll say:  
            "Answer is not available in the context."  
            - I will **highlight** important details (e.g., 🔗 Links, 📞 Contact numbers, etc.).  
            - No extra information beyond the given context.  
            - do plot some details manualy if he asked some data from the context.
            - Explore the context to find the answer example (what is your name ? , My name is ..).

            **Context:**  
            {context}  

            **Question:**  
            {question}  

            **Answer:**  
        """


        model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain
    except Exception as e:
        ProjectException(e,sys)


def user_input(user_question ,model_name = "gemini-1.5-pro"):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        #print(embeddings)
        new_db = FAISS.load_local(__path__(), embeddings, allow_dangerous_deserialization=True)
        #print(new_db)
        docs = new_db.similarity_search(user_question)
        
        chain = get_conversational_chain(model_name)
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        return response
    except Exception as e:
        print("Error ",e)
        ProjectException(e,sys)

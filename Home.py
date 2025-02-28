import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from datasets import load_dataset
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain.tools import Tool

with st.sidebar:
    st.title("Voice Appointment Chatbot")
    st.selectbox("selct the voice type:" ,['Voice1' ,'Voice2' ,'Voice3'] , index=0)
    st.selectbox("select the language : ",['English','Hindi'] , index=0)

    st.markdown("""
       <style>
       div[data-baseweb="select"] > :hover {
       cursor: pointer ;
       }
       </style>
        """ , unsafe_allow_html=True)

    appntbutton = st.button("Book apointment")
    healthp = st.button("Check your health status")
    st.markdown("""
    <style>
    div.stButton > button:hover {
        color: green;
        border-color: green;
    }
    </style>
    """, unsafe_allow_html=True)
    st.selectbox("Send notifucation after :" ,['Every hour'  ,'1 day' ,'2 days' ,'3 days' ,'4 days'  , 'A week' ,'A month'] ,index=0)
if appntbutton:
    st.switch_page("pages/appointment.py")
if healthp:
    st.switch_page("pages\health.py")

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(groq_api_key=groq_api_key, model_name='Llama3-70b-8192')
embedding = HuggingFaceEmbeddings(
    model_name='BAAI/bge-small-en-v1.5',
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
def load_and_process_document(file_path):
    loader = TextLoader(file_path)
    document = loader.load()
    return text_splitter.split_documents(document)

def create_tool(documents, embedding, tool_name, description):
    vector = FAISS.from_documents(documents, embedding)
    retriever = vector.as_retriever()
    return create_retriever_tool(retriever, tool_name, description)

doc1_path = 'C:/Users/gupta/OneDrive/Desktop/My Projects/Automatic_opintment/doctors_timing1.txt'
doc2_path = 'C:/Users/gupta/OneDrive/Desktop/My Projects/Automatic_opintment/hospital_doctors2.txt'

final_document1 = load_and_process_document(doc1_path)
final_document2 = load_and_process_document(doc2_path)

tool1 = create_tool(final_document1, embedding, "timing", "Provide information about the doctor's timing")
tool2 = create_tool(final_document2, embedding, "hospital", "Provide information about the hospital")

qna_dataset = load_dataset('ruslanmv/ai-medical-chatbot', split='train[:20]')
documents = [
    Document(page_content=item['Description'], metadata={'doctor_response': item['Doctor']})
    for item in qna_dataset
]
split_documents = text_splitter.split_documents(documents)
vector3 = FAISS.from_documents(split_documents, embedding)
retriever3 = vector3.as_retriever(search_kwargs={"k": 1})

def tool3_retriever(query: str) -> str:
    results = retriever3.invoke(query)
    if results:
        result = results[0]
        matched_description = result.page_content
        doctor_response = result.metadata.get('doctor_response', 'No doctor response available.')
        return f"Matched Description: {matched_description}\n\nDoctor's Response: {doctor_response}"
    else:
        return "Sorry, I couldn't find a relevant answer."

tool3 = Tool(
    name="general q&a",
    func=tool3_retriever,
    description="Answer general medical questions using the chatbot data."
)

tools = [tool2, tool3]
prompt = hub.pull("brianxiadong/openai-functions-agent")
prompt.messages
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

st.markdown("<h1 style='text-align: center; width : 795px; height:100px'>Welcome to Voice Appointment Chatbot</h1>", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"], unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask about doctor's timing, hospital information, or general medical questions:"):
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    input_data = {
        "input": prompt,
        "chat_history": st.session_state.messages,
        "system": (
            "You are a knowledgeable and helpful medical assistant. "
            "Your goal is to provide accurate and concise information based on the provided medical context. "
            "Always refer to the context documents before formulating a response. "
            "If the context does not provide sufficient information, it's okay to admit it. "
            "Maintain a polite and very simple english language, do not use hard words, behave like a human."
        )
    }
    response = agent_executor.invoke(input_data)

    with st.chat_message("assistant"):
        st.markdown(response["output"], unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response["output"]})




import streamlit as st
import json
from dotenv import load_dotenv
load_dotenv()

with st.sidebar:
    st.title("your current health status")
    st.checkbox("import your health parameters")
st.markdown("""
<style>
    .stApp {
        # background-color: #2D2D2D;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #4A4A4A;
        color: white;
            border: 2px solid white;
            border-radius: 3px;
    }
    .stHeader {
        background-color: transparent;
    }
    .main > div {
        padding: 2rem;
    }
    h1 {
        text-align: center;
        padding-bottom: 2em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
            input[type=number]:hover {
            color: green;
            border: 2px solid green;
            border-radius: 1.5px;
           
    }
         </style> """ , unsafe_allow_html=True)

st.title("Current Body Health Parameters" )

col1, col2 = st.columns(2)

with col1:
    heart_rate = st.number_input("Heart Rate :" , step = 1)
    respiratory_rate = st.number_input("Respiratory Rate :", step = 1)
    systolic_bp = st.number_input("Systomin B.P. :", step = 1)
    diastolic_bp = st.number_input("Diagstotic B.P. :", step = 1)

with col2:
    oxygen_level = st.number_input("Oxygen Level :", step = 1)
    derived_pulse = st.number_input("Derived Pulse Pressure :", step = 1)
    body_temp = st.number_input("Body Temp :", step = 1)

predict = st.button("Predict Health Risk")


health_risk = st.slider("Health Risk Percentage :", 
                           min_value=0, 
                           max_value=100, 
                           value= 0 , key="health_risk")              
st.markdown("""
<style>
    .stSelectbox >div{
            border: 1px solid white;
            border-radius: 9px;
            cursor: pointer;
            }

    [data-baseweb="textarea"] {
        border: 1px solid white;
            color: green;
    }
            </style>
            """, unsafe_allow_html=True)

# risk_category = st.text_area("Risk Category :", 
#                                value = "" , key="risk_category" ,height=70 )
# st.text_area("Nessecary Precautions :", value="", height=100, key="precautions")

import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
import pandas as pd
import json

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(groq_api_key=groq_api_key, model_name='mistral-saba-24b')
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

doc1_path = "precaution.txt"
final_document1 = load_and_process_document(doc1_path)

tool1 = create_tool(final_document1, embedding, "timing", "Provide information about the doctor's timing")

tools = [tool1]
user_query =  {
    "Heart Rate" : 60,
    "Respiratory Rate" : 20,
    "Systolic Blood Pressure" : 120,
    "Diastolic Blood Pressure" : 80,
    "Body Temperature" : 37,
    "Oxygen Saturation" :98 ,
    "Derived_Pulse_Pressure" : 40
}
# user_query =  {
#     "Heart Rate" : heart_rate,
#     "Respiratory Rate" : respiratory_rate,
#     "Systolic Blood Pressure" :systolic_bp ,
#     "Diastolic Blood Pressure" : diastolic_bp,
#     "Body Temperature" : body_temp,
#     "Oxygen Saturation" :oxygen_level ,
#     "Derived_Pulse_Pressure" : derived_pulse
# }
input_data = {
    "input": user_query,
    "system": (
        "You are a senior doctor analyzing the patient's health parameters. "
        "Based on the given values, predict:\n"
        "- Risk category (Low, Medium, High)\n"
        "- Health risk percentage (0-100)\n"
        "- Necessary precautions (brief text)\n\n"
        "Respond in **JSON format**:\n"
        "```json\n"
        '  "risk_category": "Low/Medium/High",\n'
        '  "health_risk_percentage": 25,\n'
        '  "precautions": ""\n'
        "```"
    ),
    "chat_history": []  
}

prompt = hub.pull("brianxiadong/openai-functions-agent")
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

if predict:
    response = agent_executor.invoke(input_data)
    st.markdown(response["output"], unsafe_allow_html=True)

# hospital_name = "King George's Medical hospital(KGMU) Lucknow, UP"
# def get_hospital_details(hospital_name):   
#     web_agent = Agent(
#         tools=[DuckDuckGoTools()],
#         model = Gemini(id = "gemini-1.5-flash"),
#         instructions=[
#             "You are a web agent tasked with retrieving comprehensive details about hospitals in India. "
#             "For each hospital, provide the following information in a concise, point-wise format:\n"
#             "- **Exact Location**: "
#             "- **Contact Number**:"
#             "- **Services Provided**: "
#             "- **Rating**: "
#             "- **Website**:"
#             "- **Email Address**: "
#             "If any details are unavailable, omit that point. Ensure the response is formatted in Markdown, utilizing HTML tags for green-colored text as shown above."
#         ],
#         show_tool_calls = False ,
#         markdown = True
#     )
#     response2 = web_agent.run(f"give me the details of {hospital_name} hospital")
#     st.markdown(response2.content, unsafe_allow_html=True)   
# get_hospital_details(hospital_name)          
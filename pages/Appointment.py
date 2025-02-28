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
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
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

doc1_path = "appointment.csv"
final_document1 = load_and_process_document(doc1_path)

tool1 = create_tool(final_document1, embedding, "timing", "Provide information about the doctor's timing")

tools = [tool1]

prompt = hub.pull("brianxiadong/openai-functions-agent")
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

st.markdown("<h1 style='text-align: center; width: 795px; height:100px'>Appointment Booking</h1>", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"], unsafe_allow_html=True)

user_prompt = st.chat_input("Ask about doctor's timing, hospital information, or general medical questions:")
from datetime import datetime
today = datetime.today().strftime('%d-%m-%Y')
if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    input_data = {
        "input": user_prompt,
        "chat_history": st.session_state.messages,
     "system": (
    "You are a helpful medical assistant that provides real-time doctor availability. "
    "Follow these steps precisely:\n\n"
    f"if user has not mentioned the date , then by default assume today's date that is {today}"
    "mostly focus now on doctor's timing and empty slotes\n"
    f"{today} column values represents the number of empty slotes for that doctor\n"
    f"1. Always check the {today} column (format DD-MM-YYYY) in the CSV first\n" 
    f"2. For availability checks: If {today}'s count or sheet of that doctor > 0 → 'Available', else → 'Unavailable'\n and {today}'s value represent number of available slots\n"
    f"3. When time is specified: Match both timing slot AND {today}'s availability\n"
    "4. Always show results in markdown tables with columns: Doctor Name, Department, Timing and number of empty slots \n"
    "5. Before booking and confirming : Re-check availability and get explicit user confirmation\n if not available say 'No available doctors matching your request'\n"
    "6. Confirmations must include folowing thinf in table form with succesful message inside st.success :\n"
    "   - Doctor's Name\n"
    "   - Department\n"
    "   - Time Slot\n"
    "   - Appointment Date to which you fix the appointment \n\n"
    "Rules:\n"
    "- Use simple English (grade 6 level)\n"
    f"- Never assume availability without checking {today} column\n"
    "- If no doctors match criteria, say 'No available doctors matching your request'\n"
    "- Today's date is always the column header in DD-MM-YYYY format\n"
    "Don't say 'Success! Your appointment has been booked successfully' like these sentences before booking confirmed by user"
    "if booking is confirmed by user say -'Your Appointmnet is successfully booked"
    )
    }
    response = agent_executor.invoke(input_data)
    with st.chat_message("assistant"):
        st.markdown(response["output"], unsafe_allow_html=True)
        if "Your Appointment is successfully booked" in response["output"] or "successfully booked" in response["output"]:
            with st.sidebar:
                st.button("Download Reciept" , key= "reciept" )

        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
st.markdown(
    """ 
    <style>
    .stSelectbox option {
        font-size: 14px !important;
        padding: 8px !important;
    }
    .stSelectbox option small {
        font-size: 12px !important;
        color: #666 !important;
        display: block !important;
        margin-top: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with open("hospitals_list.json", "r") as file:
    hospitals = json.load(file)

def format_hospital(hospital):
    return f"{hospital['name']} - {hospital['location']}"

default_hospital = {"name": "King George's Medical University (KGMU)", "location": "Lucknow, UP"}
default_index = next((i for i, h in enumerate(hospitals) if h["name"] == default_hospital["name"]), 0)

def get_hospital_details(hospital_name):   
    web_agent = Agent(
        tools=[DuckDuckGoTools()],
        model = Gemini(id = "gemini-1.5-flash"),
        instructions=[
            "You are a web agent tasked with retrieving comprehensive details about hospitals in India. "
            "For each hospital, provide the following information in a concise, point-wise format:\n"
            "- **Exact Location**: "
            "- **Contact Number**:"
            "- **Services Provided**: "
            "- **Rating**: "
            "- **Website**:"
            "- **Email Address**: "
            "If any details are unavailable, omit that point. Ensure the response is formatted in Markdown, utilizing HTML tags for green-colored text as shown above."
        ],
        show_tool_calls = False ,
        markdown = True
    )
    response2 = web_agent.run(f"give me the details of {hospital_name} hospital")
    st.markdown(response2.content, unsafe_allow_html=True)

with st.sidebar:
    selected_hospital = st.selectbox(
        "Select the hospital",
        hospitals,
        format_func=format_hospital,
        index=default_index,  
        key="hospital_selectbox",
    )

    st.markdown(
        f"**You selected:** <br>"
        f"<span style='font-size: 17px;'>{selected_hospital['name']}</span><br>"
        f"<small>{selected_hospital['location']}</small>",
        unsafe_allow_html=True
    )
    with st.expander("Hospital Details"):
        get_hospital_details(selected_hospital)

with st.sidebar:
    st.header("Current Availability")
    try:
        df = pd.read_csv(r"appointment.csv")
        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")
        today_index = df.columns.get_loc(today)
        s = df.iloc[:,1:4]
        q = pd.DataFrame(df.iloc[:,today_index])
        show1 = pd.concat([s,q], axis=1)
        show = show1[show1.iloc[:,-1]!=0]
        st.dataframe(show)
    except Exception as e:
        st.error(f"Error loading database: {str(e)}")

with st.sidebar:
    st.markdown("""
    <style>
    div.stButton {
                margin-top: 10px;
                margin-left: 80px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    div.stButton > button:hover {
        color: green;
        border-color: green;
              
    }
    </style>
    """, unsafe_allow_html=True)


    st.image("apoointment_image.webp")
    
    st.markdown("""
    <style>
     img {
            margin-top: 30px;
             margin-left: 30px;
           width: 80%;
            height: 80%;
            padding: 4px;
            box-shadow: 
                0 0 2px #330000,
                0 0 5px #660000,
                0 0 10px #990000,
                0 0 15px #CC0000,
                0 0 20px #FF0000,
                0 0 25px #FF3333,
                0 0 30px #FF6666;
            position: relative;
            z-index: -1;
            border-radius: 45px;
        }
   </style>
    """, unsafe_allow_html=True)
    
    manual = st.button("Book Manually")

# st.markdown('<img src="https://cdn3.iconfinder.com/data/icons/flat-set-1/64/flat_set_1-13-1024.png" class="audio-recorder-icon">', unsafe_allow_html=True)
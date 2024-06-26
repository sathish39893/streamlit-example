import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

st.title("Blog Outline Generator App \n with 🦜🔗 Langchain - Streamlit")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    model_name = st.selectbox("Select a model",
        ("gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-3.5-turbo-1106", "text-davinci-003"),
        index=None,
        placeholder="please select a model")
    temperature_input = st.slider("Select temperature", min_value=0.1,step=0.1,value=0.2,max_value=1.0)

def blog_outline(topic):
    # Instantiate LLM model
    llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, temperature=temperature_input)
    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an experienced data scientist and technical writer, generate an outline for a blog about a topic from user input"
            ),
            MessagesPlaceholder(variable_name="topics")
        ]
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    demo_ephemeral_chat_history = ChatMessageHistory()
    demo_ephemeral_chat_history.add_user_message(topic)

    response = chain.invoke({"topics": demo_ephemeral_chat_history.messages})
    # Print results
    return st.info(response)


with st.form("myform"):
    topic_text = st.text_input("Enter a topic to generate blog outline:", "")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif not model_name:
        st.info("Please select a model to continue.")
    elif submitted:
        blog_outline(topic_text)
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

st.title("🦜🔗 Langchain - Blog Outline Generator App")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
model_name = st.sidebar.selectbox("Select a model",
    ("gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-3.5-turbo-1106", "text-davinci-003"),
    index=None,
    placeholder="please select a model")

def blog_outline(topic):
    # Instantiate LLM model
    llm = OpenAI(model_name=model_name, openai_api_key=openai_api_key)
    # Prompt
    template = "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)
    # Run LLM model
    response = llm(prompt_query)
    # Print results
    return st.info(response)


with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key and model_name:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        blog_outline(topic_text)
import streamlit as st
from transformers import pipeline

# Initialize the model and tokenizer
@st.cache(allow_output_mutation=True)
def load_model():
    model_path = "distilgpt2"  # You can replace this with your preferred model
    generator = pipeline('text-generation', model=model_path)
    return generator

generator = load_model()

st.title("💬 Chatbot")
st.caption("🚀 A chatbot powered by Hugging Face and Streamlit")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type your message here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response from the model
    response = generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
    
    # The model may include the prompt in its response; let's try to clean it up.
    response_text = response.replace(prompt, "").strip()
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})
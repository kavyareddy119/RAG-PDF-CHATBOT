import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import base64
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from datetime import datetime

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def get_conversational_chain(api_key):
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, api_key, pdf_docs, conversation_history):
    if api_key is None or pdf_docs is None:
        st.warning("Please upload PDF files before processing.")
        return
    
    with st.spinner("Processing your question..."):
        text_chunks = get_text_chunks(get_pdf_text(pdf_docs))
        vector_store = get_vector_store(text_chunks, api_key)
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain(api_key)
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        
        user_question_output = user_question
        response_output = response['output_text']
        pdf_names = [pdf.name for pdf in pdf_docs] if pdf_docs else []
        conversation_history.append((user_question_output, response_output, 
                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ", ".join(pdf_names)))

    # Display chat messages
    st.markdown(
        f"""
        <style>
            .chat-container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            .chat-message {{
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                display: flex;
                max-width: 80%;
            }}
            .chat-message.user {{
                background-color: #2b313e;
                margin-left: auto;
                border-bottom-right-radius: 0.2rem;
            }}
            .chat-message.bot {{
                background-color: #475063;
                margin-right: auto;
                border-bottom-left-radius: 0.2rem;
            }}
            .chat-message .avatar {{
                width: 40px;
                margin-right: 1rem;
            }}
            .chat-message .avatar img {{
                width: 100%;
                border-radius: 50%;
                object-fit: cover;
            }}
            .chat-message .message {{
                flex: 1;
                color: #fff;
            }}
        </style>
        <div class="chat-container">
            <div class="chat-message user">
                <div class="avatar">
                    <img src="https://i.ibb.co/CKpTnWr/user-icon-2048x2048-ihoxz4vq.png">
                </div>    
                <div class="message">{user_question_output}</div>
            </div>
            <div class="chat-message bot">
                <div class="avatar">
                    <img src="https://cdn-icons-png.flaticon.com/512/8649/8649605.png">
                </div>
                <div class="message">{response_output}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display previous conversation history
    for question, answer, _, _ in reversed(conversation_history[:-1]):
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="chat-message user">
                    <div class="avatar">
                        <img src="https://i.ibb.co/CKpTnWr/user-icon-2048x2048-ihoxz4vq.png">
                    </div>    
                    <div class="message">{question}</div>
                </div>
                <div class="chat-message bot">
                    <div class="avatar">
                        <img src="https://i.ibb.co/wNmYHsx/langchain-logo.webp">
                    </div>
                    <div class="message">{answer}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Create download link for conversation history
    if len(conversation_history) > 0:
        df = pd.DataFrame(conversation_history, 
                         columns=["Question", "Answer", "Timestamp", "PDF Name"])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="conversation_history.csv">Download conversation history</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="PDF Chat Assistant", page_icon=":books:", layout="wide")
    
    # Main header
    st.title("📄 PDF Chat Assistant")
    st.markdown("Ask questions about your uploaded PDF documents")
    
    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Hardcoded API key (since we removed the configuration)
    api_key = "AIzaSyCZ8tI9S_VvA-hNTFsIOLaeL9xoGYrYXEU"
    
    # Sidebar configuration
    with st.sidebar:
        # PDF upload section
        st.subheader("Upload PDFs")
        pdf_docs = st.file_uploader(
            "Upload your PDF files (multiple allowed)",
            accept_multiple_files=True,
            type="pdf"
        )
        
        # Process button
        if st.button("Process PDFs"):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    get_vector_store(get_text_chunks(get_pdf_text(pdf_docs)), api_key)
                st.success("PDFs processed successfully!")
            else:
                st.warning("Please upload at least one PDF file")
        
        # Reset button
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()
        
        # Social links
        st.markdown("---")
        st.markdown("### Connect with me")
        linkedin = "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kavya-reddy-thummilla-0395682b9)"
        github = "[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kavyareddy119/)"
        st.markdown(f"{linkedin} {github}", unsafe_allow_html=True)
    
    # Main chat interface
    user_question = st.chat_input("Ask a question about your PDFs...")
    
    if user_question and pdf_docs:
        user_input(user_question, api_key, pdf_docs, st.session_state.conversation_history)

if __name__ == "__main__":
    main()
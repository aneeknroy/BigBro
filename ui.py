import streamlit as st
import os
from langchain_community.llms import Ollama
from document_loader import load_documents_into_database
from models import get_list_of_models
from llm import getStreamingChain

EMBEDDING_MODEL = "nomic-embed-text"

# Function to display files in a folder structure in the sidebar
def display_files_in_folder(upload_dir):
    st.sidebar.subheader("Uploaded Files")
    
    # Mimic folder structure
    if os.path.exists(upload_dir):
        folder_name = os.path.basename(upload_dir)
        st.sidebar.write(f"📁 **{folder_name}**")  # Display folder icon
        
        files = os.listdir(upload_dir)
        if files:
            for file in files:
                file_path = os.path.join(upload_dir, file)
                st.sidebar.write(f"   - {file}")  # Indent the file names
        else:
            st.sidebar.write("   - No files uploaded yet.")
    else:
        st.sidebar.write("No upload directory found.")

# Function for handling chat page and multiple file uploads
def chat_page():
    # Display the course name at the top
    course_name = st.session_state['selected_course']
    st.title(f"Chat for {course_name} - Big Bro")

    # Create a folder for the course if it doesn't exist
    upload_dir = f"uploads/{course_name.replace(' ', '_')}"  # Folder specific to the course
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # File upload section
    st.subheader("Upload Multiple Files for Document Indexing")
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True, key=f"{course_name}_file_uploader")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save each uploaded file to the course's folder
            file_path = os.path.join(upload_dir, uploaded_file.name)
            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File {uploaded_file.name} uploaded to {upload_dir}")
            except Exception as e:
                st.error(f"Error uploading file: {e}")

    # Model selection
    if "list_of_models" not in st.session_state:
        st.session_state["list_of_models"] = get_list_of_models()

    selected_model = st.sidebar.selectbox(
        "Select a model:", st.session_state["list_of_models"]
    )

    if st.session_state.get("ollama_model") != selected_model:
        st.session_state["ollama_model"] = selected_model
        st.session_state["llm"] = Ollama(model=selected_model)

    # Use the uploaded folder path for document indexing
    st.sidebar.subheader("Document Indexing")
    if st.sidebar.button("Index Uploaded Documents"):
        if "db" not in st.session_state:
            with st.spinner(
                "Creating embeddings and loading documents into Chroma..."
            ):
                st.session_state["db"] = load_documents_into_database(
                    EMBEDDING_MODEL, upload_dir  # Indexing the uploaded folder
                )
            st.info("All set to answer questions with indexed documents!")

    # Display the uploaded files for the course in the sidebar
    st.sidebar.subheader("Uploaded Files")
    files = os.listdir(upload_dir)
    if files:
        for file in files:
            file_path = os.path.join(upload_dir, file)
            st.sidebar.write(f"- {file}", unsafe_allow_html=True)
    else:
        st.sidebar.write("No files uploaded yet.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input handling
    if prompt := st.chat_input("Ask a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = getStreamingChain(
                prompt,
                st.session_state.messages,
                st.session_state["llm"],
                st.session_state["db"],
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Back button to return to course selection
    if st.button("Back to Courses"):
        st.session_state['page'] = 'home'
        st.rerun()



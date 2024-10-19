import streamlit as st
import os
from langchain_community.llms import Ollama
from document_loader import load_documents_into_database
from models import get_list_of_models
from llm import getStreamingChain
import time

EMBEDDING_MODEL = "nomic-embed-text"

# Function to display files in a folder structure in the sidebar
def display_files_in_folder(upload_dir):
    st.sidebar.subheader("Uploaded Files")
    
    # Mimic folder structure
    if os.path.exists(upload_dir):
        folder_name = os.path.basename(upload_dir)
        files = os.listdir(upload_dir)
        if files:
            # Create a list of options for the selectbox
            selectbox_options = [file for file in files]
        else:
            selectbox_options = ["No files uploaded yet."]
        
        # Display the folder name and the files in a selectbox
        st.sidebar.selectbox(
            f"📁 **{folder_name}**",
            selectbox_options,
        )
    else:
        st.sidebar.write("No upload directory found.")


# Function for handling chat page and multiple file uploads
def chat_page():
    course_name = st.session_state['selected_course']
    course_key = f"messages_{course_name.replace(' ', '_')}"  # Unique key for each course

    # Initialize chat history for the selected course
    if course_key not in st.session_state:
        st.session_state[course_key] = []  # Initialize an empty message history for this course

    # Display the course name at the top
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
            file_path = os.path.join(upload_dir, uploaded_file.name)
            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                success_message = st.empty()
                success_message.success(f"File {uploaded_file.name} uploaded to {upload_dir}")
                success_message.empty()  # Clear the message after 3 seconds
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
    db_session_name = f"db_{course_name}"
    if st.sidebar.button("Index Uploaded Documents"):
        if db_session_name not in st.session_state:
            with st.spinner("Creating embeddings and loading documents into Chroma..."):
                st.session_state[db_session_name] = load_documents_into_database(
                    EMBEDDING_MODEL, upload_dir  # Indexing the uploaded folder
                )
            st.info("All set to answer questions with indexed documents!")

    # Display the folder and files in the sidebar
    display_files_in_folder(upload_dir)

    # Display chat messages from history specific to the current course
    for message in st.session_state[course_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input handling
    if prompt := st.chat_input("Ask a question"):
        # Append the user message to the chat history
        st.session_state[course_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                stream = getStreamingChain(
                    prompt,
                    st.session_state[course_key],
                    st.session_state["llm"],
                    st.session_state[db_session_name],
                )
                response = st.write_stream(stream)
                st.session_state[course_key].append({"role": "assistant", "content": response})
        except:
            st.error('You must index your uploaded docs before asking questions', icon="🚨")

    # Back button to return to course selection
    if st.button("Back to Courses"):
        st.session_state['page'] = 'home'
        st.rerun()

import streamlit as st
import ui
from datetime import datetime

# Main Title
st.title('👨‍🏫 Welcome to Big Bro')

# Introduction Section
st.markdown("""
## Meet **Big Bro** – Your Personal Academic Assistant

**Big Bro** is here to help you master your classes, like that older sibling who always knows the answers! Unlike general chatbots, **Big Bro** focuses on your class-specific materials—assignments, notes, and exams. Whether you need help with homework or clarifying lecture notes, Big Bro has already "taken the class" and is ready to guide you to success.

Let **Big Bro** handle the hard work, so you can focus on learning and acing your exams!
""")

# Initialize session states
if 'courses' not in st.session_state:
    st.session_state['courses'] = []
if 'text' not in st.session_state:
    st.session_state['text'] = ''
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # Default page is 'home'
if 'selected_course' not in st.session_state:
    st.session_state['selected_course'] = ''  # Store the selected course for the chat page

# Reset the text field
def clear_text():
    st.session_state['text'] = "" 

# Get the current year to generate year options
current_year = datetime.now().year
years = [str(year) for year in range(current_year + 10, current_year - 11, -1)]  # Next 10 years
terms = [
    "Fall", "Winter", "Spring", "Summer"
]

# Main Page - Course Input and Display
if st.session_state['page'] == 'home':
    # Input section for course details with columns
    st.write("---")
    st.markdown("### Add Your Course Details")
    col1, col2 = st.columns(2)

    with col1:
        course_name = st.text_input("📚 Course Name", st.session_state['text'])
        selected_month = st.selectbox("📅 Select Month", terms)
        selected_year = st.selectbox("📅 Select Year", years, index=10)
    with col2:
        course_details = st.text_area("📝 Course Details", st.session_state['text'], height=206)
        
    # Combine selected month and year into a single string
    course_semester = f"{selected_month} {selected_year}"

    # Button to add the course
    if st.button("Add Course"):
        if course_name and course_details and course_semester:
            st.session_state['courses'].append({
                "name": course_name,
                "details": course_details,
                "semester": course_semester
            })
            st.success(f"Added {course_name}")
            clear_text()
            st.rerun()
        else:
            st.error("Please fill in all fields.")

    # Show the list of courses in tabs
    if st.session_state['courses']:
        st.write("---")
        st.title("📚 Your Courses")
        course_tabs = st.tabs([f"**{course['name']}**" for course in st.session_state['courses']])

        # Predefined class images
        class_images = {
            "ECEN": "https://w7.pngwing.com/pngs/290/911/png-transparent-google-classroom-icon-hd-logo.png",  # Placeholder URL for ECEN
            "PHYS": "https://via.placeholder.com/150?text=PHYS",  # Placeholder URL for PHYS
            "POLS": "https://via.placeholder.com/150?text=POLS",  # Placeholder URL for POLS
            "default": "https://w7.pngwing.com/pngs/290/911/png-transparent-google-classroom-icon-hd-logo.png"  # Default placeholder image
        }

        # Display course details in each tab
        for index, tab in enumerate(course_tabs):
            with tab:
                course = st.session_state['courses'][index]
                course_code = course['name'].split()[0].upper()  # Extract course code for image selection
                image_url = class_images.get(course_code, class_images["default"])

                st.image(image_url, width=150)  # Display image
                st.subheader(course['name'])
                st.write(f"**Details**: {course['details']}")
                st.write(f"**Semester**: {course['semester']}")

                # Add a "Chat" button for each course tab
                if st.button(f"Chat for {course['name']}"):
                    st.session_state['selected_course'] = course['name']
                    st.session_state['page'] = 'chat'  # Navigate to the chat page
                    st.rerun()  # Refresh to go to the new page

# Chat Page (ui.py)
if st.session_state['page'] == 'chat':
    ui.chat_page()

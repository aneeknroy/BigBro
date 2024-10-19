import streamlit as st
import ui


# Initialize an empty list to store courses
if 'courses' not in st.session_state:
    st.session_state['courses'] = []

if 'text' not in st.session_state:
    st.session_state['text'] = ''

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # Set the default page to 'home'

if 'selected_course' not in st.session_state:
    st.session_state['selected_course'] = ''  # Store the selected course for the chat page

# Reset the text field
def clear_text():
    st.session_state['text'] = '' 

# Main Page - Course Input and Display
if st.session_state['page'] == 'home':
    # Input section for course details
    st.title("Input Course Details")
    course_name = st.text_input("Course Name", st.session_state['text'])
    course_details = st.text_input("Course Details", st.session_state['text'])
    course_semester = st.text_input("Course Semester", st.session_state['text'])

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
        else:
            st.error("Please fill in all fields.")

    # Create tabs for each course
    if st.session_state['courses']:
        st.title("Courses")
        course_tabs = st.tabs([course['name'] for course in st.session_state['courses']])

        # Display the course details in each tab
        for index, tab in enumerate(course_tabs):
            with tab:
                st.subheader(st.session_state['courses'][index]['name'])
                st.write(f"Details: {st.session_state['courses'][index]['details']}")
                st.write(f"Semester: {st.session_state['courses'][index]['semester']}")

                # Add a "Chat" button for each course tab
                if st.button(f"Chat for {st.session_state['courses'][index]['name']}"):
                    st.session_state['selected_course'] = st.session_state['courses'][index]['name']
                    st.session_state['page'] = 'chat'  # Navigate to the chat page
                    st.rerun()  # Refresh to go to the new page

# Chat Page (ui.py)
if st.session_state['page'] == 'chat':
    ui.chat_page()



# import streamlit as st

# # Initialize an empty list to store courses
# if 'courses' not in st.session_state:
#     st.session_state['courses'] = []
# if 'text' not in st.session_state:
#     st.session_state['text'] = ''

# # Reset the text field
# def clear_text():
#     st.session_state['text'] = '' 

# # Input section for course details
# st.title("Input Course Details")
# course_name = st.text_input("Course Name", st.session_state['text'])
# course_details = st.text_input("Course Details", st.session_state['text'])
# course_semester = st.text_input("Course Semester", st.session_state['text'])

# # Button to add the course
# if st.button("Add Course"):
#     if course_name and course_details and course_semester:
#         st.session_state['courses'].append({
#             "name": course_name,
#             "details": course_details,
#             "semester": course_semester
#         })
#         st.success(f"Added {course_name}")
#         clear_text()
#     else:
#         st.error("Please fill in all fields.")

# # Create tabs for each course
# if st.session_state['courses']:
#     st.title("Courses")
#     course_tabs = st.tabs([course['name'] for course in st.session_state['courses']])

#     # Display the course details in each tab
#     for index, tab in enumerate(course_tabs):
#         with tab:
#             st.subheader(st.session_state['courses'][index]['name'])
#             st.write(f"Details: {st.session_state['courses'][index]['details']}")
#             st.write(f"Semester: {st.session_state['courses'][index]['semester']}")

#             # Add a "Chat" button for each course tab
#             if st.button(f"Chat for {st.session_state['courses'][index]['name']}"):
#                 st.write(f"Chat started for {st.session_state['courses'][index]['name']}")


    
# # Based on that display course in individual tabs(TODO)


# # If they click on that course it goes to a chat(ui.py) for that course name


# # {"name": "ECEN 303", "details": "ECEN-303:200,501", "semester": "Fall 2024"},
# #     {"name": "ECEN 370", "details": "ECEN 370 502", "semester": "Fall 2024"},
# #     {"name": "ECEN 426", "details": "ECEN-426:501,700", "semester": "Fall 2024"},
# #     {"name": "PHYS 217 Lec", "details": "ENGR-217:201,202", "semester": "Fall 2024"},
# #     {"name": "PHYS 217 Multi", "details": "ENGR-217:201,202", "semester": "Fall 2024"},
# #     {"name": "POLS 206", "details": "POLS-206:598,M99", "semester": "Fall 2024"},
# #     {"name": "ECEN Undergraduate Advising", "details": "COMU-045-CAAG", "semester": "Fall 2024"}
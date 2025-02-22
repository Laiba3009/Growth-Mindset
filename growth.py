from io import BytesIO
import os
import pandas as pd
import streamlit as st
import random

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Mindset Growth", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .block-container {
            height: auto !important;
            width: 100% !important;
            background-color: #E0E7FF !important;
            color: #333 !important;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            padding: 3rem 2rem;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #333;
        }
        .stButton>button {
            background-color: #0078D7 !important;
            color: white !important;
            padding: 10px 20px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #005a9e !important;
        }
        .stRadio div {
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
option = st.sidebar.radio("Choose an Option", ("Mindset Booster", "To-Do List", "Motivational Quotes", "File Converter"))

# ======================== Mindset Booster (Python Quiz) ========================
if option == "Mindset Booster":
    st.title("🚀 Growth Mindset 🎓 Coding Challenge! 💻")
    st.write(
        "An Agentic Mindset is the belief that you can be the driver of your own learning and growth, much like an AI agent that takes actions based on decisions it makes to achieve a goal."
        " Just like an AI agent becomes smarter with every decision and adjustment, you, too, become more capable as you learn, adapt, and optimize your learning journey."
    )

    st.subheader("The Future of Growth")
    st.write(
        "The future is bright for those who believe in their potential to grow and evolve. As you continue your journey in AI, Machine Learning, or any other field, always remember that learning is a lifelong process. "
        "Embrace each challenge, mistake, and success along the way, knowing that you are growing stronger, smarter, and more capable with every experience. "
        "Your growth mindset will be the key that unlocks new opportunities, new solutions, and new heights of success."
    )

    # Python Quiz Section
    st.subheader("Python Quiz: Test Your Knowledge!")

    questions = [
        {"question": "What does the 'def' keyword do in Python?", "options": ["Defines a function", "Declares a variable", "Imports a module", "None of the above"], "answer": "Defines a function"},
        {"question": "Which of the following is used for single-line comments in Python?", "options": ["//", "#", "/* */", "/*"], "answer": "#"},
        {"question": "Which data type is immutable in Python?", "options": ["List", "Set", "Dictionary", "Tuple"], "answer": "Tuple"},
        {"question": "What does the 'len()' function do?", "options": ["Returns the length of an object", "Converts a string to lowercase", "Finds the maximum number in a list", "None of the above"], "answer": "Returns the length of an object"}
    ]

    user_answers = {}

    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['question']}")
        user_answer = st.radio("Choose an option:", q['options'], key=f"q{i}")
        user_answers[i] = {"question": q['question'], "answer": user_answer, "correct_answer": q['answer']}

    if st.button("Submit Quiz"):
        score = sum([1 for ans in user_answers.values() if ans["answer"] == ans["correct_answer"]])
        st.write(f"Your score: {score}/{len(questions)}")
        if score == len(questions):
            st.success("🎉 Perfect score! You're a Python pro!")
        elif score > len(questions) // 2:
            st.success("Good job! Keep learning and you'll get better!")
        else:
            st.warning("Don't worry, practice makes perfect! Keep at it!")

# ======================== Motivational Quotes ========================
elif option == "Motivational Quotes":
    st.title("Motivational Quotes")
    quote = random.choice([
        "The only way to achieve the impossible is to believe it is possible.",
        "Success is the sum of small efforts, repeated day in and day out."
    ])
    st.write(f"💬 {quote}")

# ======================== To-Do List ========================
elif option == "To-Do List":
    st.title("📝 To-Do List")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # Input for adding a new task
    task = st.text_input("Add a New Task")
    if st.button("Add Task"):
        if task:
            st.session_state.tasks.append(task)
            st.success(f"✅ Task '{task}' added successfully!")

    # Display existing tasks with update & delete options
    if st.session_state.tasks:
        st.write("Your Current Tasks:")

        for i, task in enumerate(st.session_state.tasks):
            cols = st.columns([4, 1, 1])  # Columns for Task, Update, Delete

            # Display the task in an input field (for editing)
            updated_task = cols[0].text_input(f"Task {i+1}", task, key=f"task_{i}")

            # Update button
            if cols[1].button("✏️", key=f"update_{i}"):
                if updated_task.strip():  # Ensure task isn't empty
                    st.session_state.tasks[i] = updated_task
                    st.success(f"✅ Task updated successfully!")

            # Delete button
            if cols[2].button("❌", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.warning(f"🗑️ Task deleted!")
                st.experimental_rerun()

    else:
        st.write("No tasks added yet. Start by adding a new task!")

# ======================== File Converter ========================
elif option == "File Converter":
    st.title("📂 Advanced Data Sweeper")

    uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[-1].lower()

            if file_extension == ".csv":
                df = pd.read_csv(file)
            elif file_extension == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file type: {file_extension}")
                continue

            st.write(f"📄 File Name: {file.name}")
            st.write("🔍 Preview of the Uploaded File:")
            st.dataframe(df.head())

            if st.button(f"Convert {file.name}", key=f"convert_{file.name}"):
                buffer = BytesIO()
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                st.download_button(
                    label=f"⬇ Download {file.name} as CSV",
                    data=buffer,
                    file_name=file.name.replace(file_extension, ".csv"),
                    mime="text/csv"
                )
                st.success(f"✅ File '{file.name}' converted successfully!")

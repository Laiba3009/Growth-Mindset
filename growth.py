import streamlit as st
import pandas as pd
import os
import random
from io import BytesIO

# Configure Streamlit app
st.set_page_config(page_title="Mindset Growth & Data Sweeper", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main { background-color: #121212; }
        .block-container {
            padding: 3rem 2rem;
            background-color: #E0E7FF ;
            border-radius: 12px;
            color: #333 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3, h4, h5, h6 { color: #66c2ff; }
        .stButton>button {
            border-radius: 8px;
            background-color: #0078D7;
            color: white;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
        .stButton>button:hover { background-color: #005a9e; }
        .stDataFrame, .stTable { border-radius: 10px; overflow: hidden; }
        .stRadio label { color: #004080 !important; font-weight: bold; } /* Dark Blue Quiz Text */
        .stDownloadButton>button { background-color: #28a745; color: white; }
        .stDownloadButton>button:hover { background-color: #218838; }
        .correct { color: green; font-weight: bold; }
        .wrong { color: red; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
option = st.sidebar.radio("Choose an Option", ("Mindset Booster", "To-Do List", "Motivational Quotes", "File Converter"))

# =================== MINDSET BOOSTER (Python Quiz) ===================
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
        {"question": "Which of the following is used for single-line comments in Python?", "options": ["//", "\\#", "/* */", "/*"], "answer": "\\#"},
        {"question": "Which data type is immutable in Python?", "options": ["List", "Set", "Dictionary", "Tuple"], "answer": "Tuple"},
        {"question": "What does the 'len()' function do?", "options": ["Returns the length of an object", "Converts a string to lowercase", "Finds the maximum number in a list", "None of the above"], "answer": "Returns the length of an object"}
    ]

    user_answers = {}
    
    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['question']}")
        user_answer = st.radio("Choose an option:", q['options'], key=f"q{i}")
        user_answers[i] = {"answer": user_answer, "correct_answer": q['answer']}

    if st.button("Submit Quiz"):
        score = 0
        for i, ans in user_answers.items():
            if ans["answer"] == ans["correct_answer"]:
                st.markdown(f"✅ **Q{i+1}: {ans['answer']}** - <span class='correct'>Correct</span>", unsafe_allow_html=True)
                score += 1
            else:
                st.markdown(f"❌ **Q{i+1}: {ans['answer']}** - <span class='wrong'>Wrong</span>, Correct answer: {ans['correct_answer']}", unsafe_allow_html=True)

        st.write(f"Your score: {score}/{len(questions)}")
        if score == len(questions):
            st.success("🎉 Perfect score! You're a Python pro!")
        elif score > len(questions) // 2:
            st.success("Good job! Keep learning!")
        else:
            st.warning("Don't worry, practice makes perfect!")

# =================== TO-DO LIST ===================
elif option == "To-Do List":
    st.title("📝 To-Do List")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    task = st.text_input("Add a New Task")
    if st.button("Add Task"):
        if task:
            st.session_state.tasks.append(task)
            st.success(f"✅ Task '{task}' added successfully!")

    if st.session_state.tasks:
        st.write("Your Current Tasks:")
        for i, task in enumerate(st.session_state.tasks):
            cols = st.columns([4, 1, 1])
            updated_task = cols[0].text_input(f"Task {i+1}", task, key=f"task_{i}")
            if cols[1].button("✏️", key=f"update_{i}"):
                if updated_task.strip():
                    st.session_state.tasks[i] = updated_task
                    st.success("✅ Task updated!")
            if cols[2].button("❌", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.warning("🗑️ Task deleted!")
                st.experimental_rerun()

# =================== MOTIVATIONAL QUOTES ===================
elif option == "Motivational Quotes":
    st.title("Motivational Quotes")
    quote = random.choice([
        "The only way to achieve the impossible is to believe it is possible.",
        "Success is the sum of small efforts, repeated day in and day out."
    ])
    st.write(f"💬 {quote}")

# =================== FILE CONVERTER (CSV/Excel) ===================
elif option == "File Converter":
    st.title("📂 Advanced Data Sweeper")
    uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

    files_processed = False

    if uploaded_files:
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[-1].lower()

            try:
                if file_extension == ".csv":
                    df = pd.read_csv(file, encoding="ISO-8859-1", errors="replace")
                elif file_extension == ".xlsx":
                    df = pd.read_excel(file, engine="openpyxl")
                else:
                    st.error(f"Unsupported file type: {file_extension}")
                    continue
            except Exception as e:
                st.error(f"⚠️ Error processing {file.name}: {e}")
                continue

            st.write(f"📄 **File Name:** {file.name}")
            st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")
            st.write("🔍 **Preview of the Uploaded File:**")
            st.dataframe(df.head())

            # File Conversion
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_extension, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine='openpyxl')
                    file_name = file.name.replace(file_extension, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                st.download_button(label=f"⬇️ Download {file_name}", data=buffer, file_name=file_name, mime=mime_type)
                files_processed = True

    if files_processed:
        st.success("🎉 All files processed successfully!")

import streamlit as st
import pandas as pd
import time
import datetime

# ----- Page Setup -----
st.set_page_config(page_title="Smart To-Do", layout="centered")

# ----- Session State -----
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "mood" not in st.session_state:
    st.session_state.mood = "😐"
if "timer_active" not in st.session_state:
    st.session_state.timer_active = None
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# ----- Sidebar -----
st.sidebar.title("⚙️ Settings")
if st.sidebar.button("Toggle Dark/Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

st.session_state.mood = st.sidebar.selectbox("🧠 How are you feeling today?", ["😴", "😐", "🙂", "😄", "🔥"], index=1)

# ----- Task Input -----
st.title("✅ Smart To-Do List")
task_input = st.text_input("Add a new task:")
if st.button("➕ Add Task") and task_input:
    st.session_state.tasks.append({"task": task_input, "done": False, "created": datetime.date.today()})

# ----- Display Tasks -----
done_count = 0
for i, task in enumerate(st.session_state.tasks):
    col1, col2, col3, col4 = st.columns([0.1, 0.6, 0.2, 0.1])

    checked = col1.checkbox("", value=task["done"], key=f"check_{i}")
    st.session_state.tasks[i]["done"] = checked

    if checked:
        done_count += 1

    col2.write(f"**{task['task']}**")
    if col3.button("⏱️ Pomodoro", key=f"pomodoro_{i}"):
        st.session_state.timer_active = i
        st.session_state.timer_start = time.time()

    if col4.button("❌", key=f"delete_{i}"):
        st.session_state.tasks.pop(i)
        st.experimental_rerun()

# ----- Daily Goal -----
st.markdown("---")
if done_count >= 3:
    st.success("🎯 You’ve hit your goal of 3+ tasks today!")
else:
    st.info(f"Tasks done: {done_count}. Complete {3 - done_count} more to hit your daily goal!")

# ----- Pomodoro Timer -----
if st.session_state.timer_active is not None:
    i = st.session_state.timer_active
    elapsed = int(time.time() - st.session_state.timer_start)
    remaining = 1500 - elapsed  # 25 mins

    if remaining > 0:
        mins, secs = divmod(remaining, 60)
        st.warning(f"⏳ Pomodoro for: {st.session_state.tasks[i]['task']} — {mins:02d}:{secs:02d}")
        time.sleep(1)
        st.experimental_rerun()
    else:
        st.success("🎉 Pomodoro complete!")
        st.balloons()
        st.session_state.timer_active = None
        st.session_state.timer_start = None
# ----- About Section -----
with st.expander("About This App"):
    st.markdown("""
        ### Smart To-Do List
        Smart To-Do List is a lightweight, productivity-focused web application developed using Streamlit and Python. It is designed to help users efficiently manage tasks while also tracking their emotional state and daily consistency.

        #### Key Features:
        - Add, delete, and mark tasks as complete
        - Toggle between light and dark mode
        - Track daily mood using a predefined scale
        - Daily goal tracker to encourage consistent task completion
        - Built-in Pomodoro timer to support focused work sessions

        #### Purpose:
        This tool was built for students, developers, and professionals who value a minimal, intuitive productivity dashboard. It integrates behavioral cues (like mood) and simple gamification (like daily goals) to promote consistent habits.

        #### Built With:
        - Python 3
        - Streamlit
        - Pandas
        - Visual Studio Code

        This application is modular and extensible. Future enhancements may include CSV export, cloud storage, user authentication, or integration with tools like Notion or Google Calendar.
    """)

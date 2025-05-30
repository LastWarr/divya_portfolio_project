import streamlit as st
from utils import ask_gpt, get_daily_topic


st.set_page_config(page_title="DS Interview Prep Assistant", layout="centered")
st.title("🧠 Daily DS Interview Prep Assistant")

st.subheader("📅 Today's Topic")
daily_topic = get_daily_topic()
st.success(daily_topic)

task = st.selectbox("Choose a task", [
    "Quiz Me", "Explain a topic", "Mock Interview",
    "Evaluate My Answer", "Study Plan", "Summarize Notes"
])
topic = st.text_input("Topic (e.g., 'Random Forest', 'PCA')", key="topic",placeholder="Leave empty to use today's topic")
user_answer = st.text_area("Your Answer (for 'Evaluate My Answer')", key="answer") if task == "Evaluate My Answer" else None
goal = st.text_input("Your Goal (for 'Study Plan')", key="goal") if task == "Study Plan" else None
content = st.text_area("Paste content (for 'Summarize Notes')", key="content") if task == "Summarize Notes" else None



if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Ask"):
    chosen_topic = topic if topic else daily_topic
    if not chosen_topic:
        st.warning("No topic selected.")
    else:
        with st.spinner("Thinking..."):
            response = ask_gpt(
            task=task,
            topic=topic,
            user_answer=user_answer,
            goal=goal,
            content=content
        )
            # st.session_state.messages.append(("You", f"{task} - {chosen_topic}"))
            # st.session_state.messages.append(("AI", response))
            st.markdown("### 💬 Response")
            st.markdown(response)

st.divider()


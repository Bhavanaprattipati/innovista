import streamlit as st

def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []

def save_to_history(original, rewritten, audio):
    st.session_state.history.append({
        "original": original,
        "rewritten": rewritten,
        "audio": audio
    })

def display_history():
    st.sidebar.title("📜 Past Narrations")
    for i, item in enumerate(st.session_state.history[::-1]):
        st.sidebar.markdown(f"*Narration {len(st.session_state.history)-i}*")
        st.sidebar.write("🔤 Original:")
        st.sidebar.caption(item["original"][:100] + "...")
        st.sidebar.write("🎧 Audio:")
        st.sidebar.audio(item["audio"], format="audio/wav")
        st.sidebar.download_button("⬇ Download", item["audio"], file_name=f"narration_{len(st.session_state.history)-i}.wav")
        st.sidebar.markdown("---")

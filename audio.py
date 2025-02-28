from audio_recorder_streamlit import audio_recorder
import streamlit as st

st.markdown('<img src="https://cdn3.iconfinder.com/data/icons/flat-set-1/64/flat_set_1-13-1024.png" class="audio-recorder-icon" style = "margin-top:28em; padding:3em;">', unsafe_allow_html=True)

custom_css = """
.st-emotion-cache-1cvow4s img {
    max-width: 20%;
    vertical-align: middle;
}
"""
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()




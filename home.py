import streamlit as st
from opeai import get_video_info
from streamlit_TTS import auto_play, text_to_speech, text_to_audio

from gtts.lang import tts_langs
langs=tts_langs().keys()

# Set up the page layout and title
st.set_page_config(page_title="Video Info", layout="centered")
st.title("Video Info")

# Add some description or instructions
st.write("Enter a video URL to retrieve its information.")

# Input box for the video URL
video_url = st.text_input("Video URL", max_chars=100, placeholder="Enter the video link here")
question = st.text_input("Question", max_chars=100, placeholder="Enter the Question here")
api_key = st.text_input("Key", max_chars=1000, placeholder="Enter the Key here",type = 'password')
# Submit button to trigger the action
if st.button("Get Info"):
    if video_url:
        try:
            res = get_video_info(video_url, question,api_key)
            st.write(f"Here is the info :- \n{res}")
            text_to_speech(text=res, language='en')
            # Here, you would add the code to get the video info using an API or other method
        except Exception as e:
            # print(e)
            st.write(f"Some error occured :- {e}")
    else:
        st.warning("Please enter a valid video URL.")

# Optionally, add a footer or other elements to beautify the page
st.markdown("---")
st.write("Powered by Streamlit")

import streamlit as st
from google import genai
import requests
from bs4 import BeautifulSoup

# 1. Setup the Look of the Website
st.set_page_config(page_title="GAM Key-Value Creator", page_icon="🏷️")
st.title("🏷️ GAM Contextual Key-Value Creator")
st.write("Enter a URL to generate Google Ad Manager Key-Values automatically.")

# 2. Get the API Key from you (User Input)
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 3. The URL Input Box
url_input = st.text_input("Paste Website URL here:", placeholder="https://example.com/article")

if st.button("Generate My Keys"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar!")
    elif not url_input:
        st.warning("Please enter a URL first.")
    else:
        try:
            with st.spinner("Scanning website and thinking..."):
                # STEP A: Scrape the website text
                response = requests.get(url_input, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                # Grab the title and some text
                page_text = f"Title: {soup.title.string if soup.title else ''} \nContent: {soup.get_text()[:2000]}"

                # STEP B: Ask Gemini to create the keys
                client = genai.Client(api_key=api_key)
                prompt = f"""
                You are a GAM Ad Ops expert. Analyze this webpage content:
                {page_text}
                
                Generate 5 Key-Value pairs for Google Ad Manager. 
                Focus on: IAB Category, Content Sentiment, and Main Topic.
                Format the output as a clean Table with: Key | Value | Why it's valuable.
                Then, provide the 'googletag.pubads().setTargeting' code for the user.
                """
                
                result = client.models.generate_content(
                    model="gemini-3-flash-preview", 
                    contents=prompt
                )

                # STEP C: Show the result
                st.success("Done! Here is your GAM Setup:")
                st.markdown(result.text)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

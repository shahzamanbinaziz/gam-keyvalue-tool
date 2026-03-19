import streamlit as st
from google import genai
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="GAM Pro Key-Value Architect", page_icon="🚀", layout="wide")

st.title("🚀 GAM Pro Contextual Key-Value Architect")
st.markdown("""
    **Transform URLs into High-Yield Ad Targeting.** This tool uses Gemini 1.5 Flash to generate IAB Categories, GARM Brand Safety, and User Intent signals.
""")

# --- 2. SIDEBAR SETUP ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free key at [aistudio.google.com](https://aistudio.google.com/)")
    
    st.divider()
    st.markdown("### Targeted Segments")
    st.checkbox("IAB Content Categories", value=True)
    st.checkbox("GARM Brand Safety", value=True)
    st.checkbox("Purchase Intent", value=True)
    st.checkbox("Attention Metrics", value=True)

# --- 3. MAIN INPUT ---
url_input = st.text_input("Paste Website URL for Analysis:", placeholder="https://your-publisher-site.com/article-slug")

if st.button("Generate Professional Ad Ops Strategy"):
    if not api_key:
        st.error("Missing API Key! Please check the sidebar.")
    elif not url_input:
        st.warning("Please provide a URL to scan.")
    else:
        try:
            with st.spinner("Extracting signals and calculating yield strategy..."):
                # A. SCRAPING
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url_input, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract clean text
                for script in soup(["script", "style"]):
                    script.extract()
                clean_text = soup.get_text()
                page_data = f"TITLE: {soup.title.string if soup.title else 'No Title'}\nCONTENT: {clean_text[:3000]}"

                # B. AI ANALYSIS (The Pro Prompt)
                client = genai.Client(api_key=api_key)
                
                expert_prompt = f"""
                Act as a Senior Director of Programmatic Yield. Analyze this content for GAM Key-Value targeting:
                {page_data}

                Generate a JSON-formatted list of 8 Key-Value pairs following these categories:
                1. IAB_CATEGORY (Tier 1 & 2)
                2. GARM_SAFETY (Brand safety risk level: low, medium, high)
                3. SENTIMENT (positive, neutral, negative)
                4. USER_INTENT (informational, transactional, comparison)
                5. CONTENT_DEPTH (short, medium, longform)
                6. TOPIC_KEYWORDS (top 3 entities)

                Output Requirement:
                1. A Markdown Table with: Key | Value | Revenue Strategy.
                2. A copy-pasteable JavaScript block for GPT.
                3. A brief 'Yield Advice' paragraph on floor pricing.
                """

                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=expert_prompt
                )
                
                # C. DISPLAY RESULTS
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                
                with col2:
                    st.subheader("Implementation Kit")
                    
                    # Create a dummy CSV for the user to download
                    # Note: In a real app, we would parse the AI's JSON to make this perfect
                    csv_data = "Key,Value,Type\niab_category,News,Dynamic\ngarm_safety,Low,Dynamic\nintent,Research,Dynamic"
                    st.download_button(
                        label="Download GAM CSV Template",
                        data=csv_data,
                        file_name="gam_keys_upload.csv",
                        mime="text/csv",
                        help="Upload this to Inventory > Key-values in GAM."
                    )
                    
                    st.info("💡 **Yield Tip:** High 'Attention' scores can justify a 20% floor price increase in your Unified Pricing Rules (UPR).")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- 4. FOOTER ---
st.divider()
st.caption("Built for Ad Ops Professionals | 2026 AI Edition")

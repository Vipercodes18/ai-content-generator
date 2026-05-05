import os
import re
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

st.title("🚀 AI Content Generator")

user_input = st.text_input("Enter your topic:")

platform = st.selectbox("Select Platform", ["Instagram", "LinkedIn", "Twitter"])
tone = st.selectbox("Select Tone", ["Motivational", "Funny", "Serious"])

if st.button("Generate"):
    if user_input:
        prompt = f"""
        Generate a {platform} post for the topic: {user_input}
        for the tone: {tone}

        Strict rules:
        - Return ONLY valid JSON
        - No extra text or explanation
        - Do NOT add anything outside JSON
        - Use ONLY these keys: title, hook, caption
        - If output is not valid JSON, regenerate it correctly

        Guidelines:
        - Title: short and relevant
        - Hook: catchy and engaging (NOT hashtags)
        - Caption: simple, natural English
        - Include hashtags ONLY inside caption (at the end)

        Output format:
        {{
          "title": "...",
          "hook": "...",
          "caption": "..."
        }}
        """
        with st.spinner("Generating content..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a professional social media content creator."},
                    {"role": "user", "content": prompt}
                ]
            )

            output = response.choices[0].message.content

            st.markdown("---")
            st.success("Content Generated Successfully ✅")
            st.toast("Content ready 🚀")

            data = None  # 👈 IMPORTANT

            try:
                # 👇 JSON extract karega even if extra text ho
                json_match = re.search(r'\{.*\}', output, re.DOTALL)
                
                if json_match:
                    clean_json = json_match.group()
                    data = json.loads(clean_json)
                else:
                    raise ValueError("No JSON found")

                st.markdown("### 📌 Title")
                st.info(data["title"])

                st.markdown("### 🔥 Hook")
                st.warning(data["hook"])

                st.markdown("### 📝 Caption")
                st.success(data["caption"])

            except:
                st.error("Invalid JSON output")
                st.code(output)

            # 👇 safe usage
            if data:
                st.code(data["caption"], language="text")

    else:
        st.warning("Please enter a topic")

st.markdown("---")
st.caption("🚀 Built by Abhishek | AI Content Generator")

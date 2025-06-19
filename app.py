from dotenv import load_dotenv
load_dotenv()

import os
import base64
import io
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

# ✅ Load API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# ✅ Safety check: Stop app if API key is missing
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in your .env file.")
    st.stop()

# ✅ Configure Gemini with API key
genai.configure(api_key=api_key)

# ✅ Gemini response function
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# ✅ Convert uploaded PDF to image and Base64 format
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# ✅ Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Evaluate the resume against the provided job description. Give a percentage match, list missing keywords, and provide final thoughts.
"""

# ✅ Submit button 1: Evaluation
if submit1:
    if uploaded_file:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please upload a resume.")

# ✅ Submit button 3: Percentage match
elif submit3:
    if uploaded_file:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please upload a resume.")

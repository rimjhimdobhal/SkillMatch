import streamlit as st
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Let's configure the model
gemini_api_key = os.getenv('GOOGLE_API_KEY2')
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature = 0.9
)

# Let's create the sidebar to upload the resume
st.sidebar.title('UPLOAD YOUR RESUME (PDF)')
file = st.sidebar.file_uploader('Resume', type = ['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('File Uploaded Successfully')


# Create the main page of the application
st.markdown(
    """
    <h1 style="
        font-size:52px;
        font-weight:700;
        display:inline-block;
    ">
        <span style="color:#C2185B;">SKILLMATCH:</span>
        <span style="color:#4793AF;"> AI-Powered Skill Matching</span>
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown('#### This application will match and analyze your resume and the job description provided.')
tips = '''
Follow these steps:
1. Upload your resume (PDF Only) in the sidebar.
2. Copy and paste the job description below.
3. Click on submit to run the application.'''
st.write(tips)

job_desc = st.text_area('Copy and paste your job description over here.',
             max_chars= 50000)
if st.button('SUBMIT'):
    with st.spinner('Processing...'):
        prompt = f'''
        <Role> You are an expert in analyzing resume and matching job description.
        <Goal> Match the resume and the job description provided by the applicant and create a report.
        <Context> The following content has been provided by the applicant: 
        * Resume: {file_text}
        * Job Description: {job_desc}
        <Format> The report should follow these steps:
        * Give a bried description of the applicant in 3-5 lines.
        * Describe in percentage what are the chances of this resume getting selected.
        * Need not be the exact percentage, you can give interval of percentage.
        * Give the expected ATS Score along with matching and non-matching keywords.
        * Perform SWOT Analysis and explain each parameter i.e., Strength, Weakness, Opportunity and Threat.
        * Give what all sections in the current resume that are required to be changed in order to improve the ATS Score
        and selection percentage. 
        * Show both the current version and the improved version of the section in resume.
        * Create two sample resume which can maximize the ATS Score and selection percentage.

        <Instruction> 
        * Use bullet points for explanation wherever possible. 
        * Create tables for description wherever required. 
        * Strictly do not add any new skill in sample resume.
        * The format of sample resume should be in such a way that they can be copied and pasted in Word. 
        '''


        response = model.invoke(prompt)
        clean_output = (
              response.content
                        .replace("<br>", "\n")
                        .replace("<br/>", "\n")
                        .replace("<br />", "\n"))

        st.markdown(clean_output)





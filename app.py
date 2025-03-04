#GRADIO APP
import gradio as gr
import os
import base64
import io
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text

def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        file_path = uploaded_file.name  
        pdf_text = extract_text(file_path)  # Extract text from the PDF
        return pdf_text
    else:
        raise FileNotFoundError("File not uploaded")

input_prompt1 = """
You are an experienced HR with Tech experience in the field of any one job role from Data Science, Full stack Web Development, Big Data Engineering, DEVOPS, Data Analyst, Machine Learning, LLM engineering.
Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to specified job requirements.
"""

input_prompt2 = """   
You are an experienced HR with Tech experience in the field of any one job role from Data Science, Full stack Web Development, Big Data Engineering, DEVOPS, Data Analyst, Machine Learning, LLM engineering.
Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether there are any missing keywords in the resume that are mentioned in the job description.
Just provide the exact missing keywords in bullet points.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Full stack Web Development, Big Data Engineering, DEVOPS, Data Analyst, Machine Learning, LLM engineering and deep ATS functionality.
Your task is to evaluate the resume against the provided job description.
Give me the percentage of match if the resume matches the job description. First, the output should come as percentage and then keywords missing and last final thoughts.
"""

def process_resume(job_description, uploaded_file, option):
    if not job_description.strip():
        return "Please provide the job description."

    if uploaded_file is not None:
        pdf_text = extract_pdf_text(uploaded_file)
        if option == "Resume Evaluation":
            response = get_gemini_response(job_description, pdf_text, input_prompt1)
        elif option == "Missing Keywords":
            response = get_gemini_response(job_description, pdf_text, input_prompt2)
        elif option == "Percentage Match":
            response = get_gemini_response(job_description, pdf_text, input_prompt3)
        else:
            response = "Invalid option selected."
        return response
    else:
        return "Please upload a resume."

with gr.Blocks(css="""  
    .gradio-container {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        background-color: #ffffff;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    #submit {
        background-color: #E3963E;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }

    #submit:hover {
        background-color: #ff8c00;
    }

    #head {
        text-align: center;
    }
    #head2 {
        text-align: center;
    }
""") as demo:
    gr.Markdown("# ATS Resume Expert", elem_id="head")
    gr.Markdown("Upload your resume and job description to analyze how well it matches the job requirements.", elem_id="head2")
    
    job_description = gr.TextArea(label="Job Description")
    uploaded_file = gr.File(label="Upload your resume (PDF)")
    option = gr.Radio(["Resume Evaluation", "Missing Keywords", "Percentage Match"], label="Select Analysis Type")
    
    submit_button = gr.Button("Analyze Resume", elem_id="submit")
    output = gr.Markdown(label="Response")

    submit_button.click(process_resume, inputs=[job_description, uploaded_file, option], outputs=output)

demo.launch(debug=True, server_port=7860)





































#Streamlit app
# from dotenv import load_dotenv

# load_dotenv()

# import streamlit as st
# import os
# from PIL import Image
# import pdf2image
# import google.generativeai as genai
# import base64
# import io

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,pdf_content,prompt):
#     model=genai.GenerativeModel("gemini-1.5-flash")
#     response=model.generate_content(
#         [input,pdf_content[0],prompt]
#     )
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         ##convert the pdf to image
#         images = pdf2image.convert_from_bytes(uploaded_file.read()) #Reading the uploaded file and converting from bytes to image
#         first_page=images[0] #Taking the first page
        
#         #Convert to bytes
#         img_byte_arr=io.BytesIO() #Saving first image to byte format in virtual memory. It is like saving memory rather than file or disk. Analogy if you want to write something temporarily you will write in your memory not on paper.
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr=img_byte_arr.getvalue()# Retrve the byte data from virtual memory
        
#         pdf_parts=[
#             {
#                 "mime_type":"image/jpeg", #to represent what type of data mime_type is used
#                 "data":base64.b64encode(img_byte_arr).decode()   #converting byte data to base64 encoding and decoding it to string back again. This is done for easy transport or storage.
#             }
#         ]
#         return pdf_parts
#     else:
#          raise FileNotFoundError("File not uploaded")

# #This is the format which google gemini expects

# ##Streamlit app
# st.set_page_config(page_title="ATS Resume Expert")
# st.header("ATS Tracking System")
# input_text=st.text_area("Job Decription: ", key="input")
# uploaded_file=st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# if uploaded_file is not None:
#     st.write("PDF Uploaded successfully")
    
# submit1=st.button("Tell me about the Resume")

# # submit2=st.button("How can I improvise my skills")

# submit2=st.button("What are the keywords that are missing")

# submit3=st.button("Percentage Match")

# input_prompt1="""

# You are an experienced HR with Tech experience in the field of any one job role from Data Science, Full stack Web Development, Big Data Engineering,DEVOPS, Data Analyst, Machine Learning, LLM engineering.
# Your task is to review the provided resume against the job description for these profiles.
# Please share your professional evaluation on whether the candidate's profile aligns with the role.
# Highlight the strengths and weakness of the applicant in relation to specified job requirements.
# """

# input_prompt2="""   
# You are an experienced HR with Tech experience in the field of any one job role from Data Science, Full stack Web Development, Big Data Engineering,DEVOPS, Data Analyst, Machine Learning, LLM engineering.
# Your task is to review the provided resume against the job description for these profiles.
# Please share your professional evaluation on whether are there any missing keywords in the resume that are mentioned in the job description.
# Just provide the exact missing keywords in bullet points.
# """

# input_prompt3="""
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Full stack Web Development, Big Data Engineering, DEVOPS
# Data Analyst, Machine Learning, LLM engineering and deep ATS functionality.
# Your task is to evaluate the resume against the provided job description.
# Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_text,pdf_content,input_prompt1) #input_text means job description
#         st.subheader("The response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")

# elif submit2:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_text,pdf_content,input_prompt2) #input_text means job description
#         st.subheader("The response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")
        

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_text,pdf_content,input_prompt3) #input_text means job description
#         st.subheader("The response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")
        
       
        
    

    



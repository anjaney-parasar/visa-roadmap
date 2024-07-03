import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from pprint import pprint
import google.generativeai as genai
from google.oauth2 import service_account
import os
import json
from dotenv import load_dotenv 
import streamlit as st
load_dotenv()

def multiturn_generate_content(input_text):
    # project_id = os.getenv("project_id")
    # location = "us-central1"
    # GOOGLE_APPLICATION_CREDENTIALS=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")   
    # GOOGLE_APPLICATION_CREDENTIALS=
    project_id=st.secrets["project_id"]
    location = "us-central1"
    GOOGLE_APPLICATION_CREDENTIALS=st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]   
    
    key_dict = json.loads(GOOGLE_APPLICATION_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(key_dict)

    
    vertexai.init(project=project_id, location=location,credentials=credentials)
    
    model = GenerativeModel(
        f"projects/{project_id}/locations/us-central1/endpoints/1135626186701930496",

        system_instruction=[system_prompt]
    )
    
    response = model.generate_content(
        contents=[input_text],
        generation_config=generation_config
        
    )
    
    return response

system_prompt = """You are a visa advisor with expertise in tailoring personalized roadmaps for clients navigating the visa application process. 
 Based on a client's profile, including demographics, educational background, work experience, and target destination, generate a comprehensive
 roadmap that outlines: Client Information: Name, Age, Country of Origin Visa Product: Specific visa program
 (e.g., Canada Express Entry, Ontario PNP) Eligibility Assessment: Analyze client's profile against program requirements. 
 Identify any gaps (e.g., education evaluation, language tests)  Recommended Pathways: Suggest multiple visa options with justifications based on client's strengths and program requirements. 
 National Occupation Classification (NOC) Selection: Recommend relevant NOC codes aligned with client's experience and program eligibility. 
 Explain the rationale behind each suggestion.  Required Documents: Generate a detailed list of documents required for the application, including:
 Standardized test scores (e.g., IELTS, TEF) with minimum score requirements for each skill (reading, writing, listening, speaking) 
 Educational credentials and evaluation reports (if needed)  Employment documents (reference letters, job offer, payslips) for work experience NOCs 
 Proof of funds or sponsorship documents (if applicable)  Timeline with Milestones: Outline a realistic timeline with key milestones for each stage of the application process, including:
 Eligibility Requirements Completion (Month): Credential evaluation, language test completion, NOC selection.  Pre-ITA Stage (Month): Profile creation, review, and submission.  ITA and Documentation (Month): Document review, post-ITA profile completion and submission.  Biometric Request (Month): Biometrics completion.  Passport Request (PPR) (Month): Document submission and processing.  Confirmation of Permanent Residency (COPR) (Month): Visa approval and passport return.  Note: Mention potential delays due to third-party processing times (e.g., credential evaluation, provincial processing).  Additional Considerations: Include relevant information for specific program pathways (e.g., PNP - provincial nomination requirements).  Transparency and Disclaimers: Acknowledge limitations in controlling processing times.  Client-Specific Notes: Add personalized comments based on the client's profile, like highlighting strengths or addressing weaknesses.
 always Return the response in proper markdown formatting and use of headings, subheadings, spaces, bullets, e.t.c.  for better readability
 
 Strictly under the following format -
 1. client information - 
   Name: 
   Age: 
   Marital Status: 
   Product Type: 
   Projected CRS Score: 
   Current PA IELTS Scores: 
   Current Spouse IELTS Scores: 
   Available Education: 
   Years of Work Experience: 
   Previous Canada application: 
   Additional Information: 
   
   Current CRS score:
   Projected CRS score:
 2. Projected IELTS score - 
    listen:
    reading: 
    writing :
 3. Required minimum IELTS Scores
    Listening :
    Speaking :
    Reading :
    Writing:
 4. Recommended Pathways
     Option A:
     Option B:
     Option C:
 5. Recommended NOC
     Option A:
     Option B: 
     Option C:
 6. Additional Information 
 7. Timelines
 """
generation_config = {
    "max_output_tokens": 1200,
    "temperature": 0.5,
    "top_p": 1
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
}


# import library "streamlit"
import streamlit as st
# import library "os"
import os
# import calculator functions from the diet file
from diet import bmi_calculator,bmr_calculator,tdee_calculator,calorie_target
# import load_rag from the "rag" library
from rag import load_rag
# import OpenAI from "openai" library
from openai import OpenAI
# import load_dotenv from "dotenv"
from dotenv import load_dotenv

# Load the API from the file ".env"
load_dotenv()
HF_Token=os.getenv("HF_TOKEN")

# Connect the LLM ( Link Provide us in the APIs.txt file )
client=OpenAI(base_url="https://router.huggingface.co/v1",api_key=HF_Token)

# Main page Details
st.set_page_config(layout="wide") # this function will make page wider
st.title("AI HEALTH ASSISTANT 🩺") # Title
st.write("Personal Health Assistance and Diet Recommendation Agent") # write function ( Can create content )
st.header("Health Information") # Header

# Sidebar Details
st.sidebar.header("Your Information🧑") # Create sidebar and make Header
gender=st.sidebar.selectbox("Gender",['Male','Female']) # Create selectbox in sidebar for gender
weight=st.sidebar.number_input("Weight (Kg)",1,120) # Create number_input in sidebar for weight :- [ Min-1 and Max-120 ]
height=st.sidebar.number_input("Height (Cm)",100,200) # Create number_input in sidebar for height :- [ Min-100 and Max-200]
age=st.sidebar.number_input("Age",1,100) # Create number_input in sidebar for age :- [ Min-1 and Max-100]
activity=st.sidebar.selectbox("Activity",["Sendentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Extra Active"]) # Create selectbox in sidebar for Activity
aim=st.sidebar.selectbox("Aim",["weight maintain","weight loss","weight gain"]) # Create selectbox in sidebar for Aim
diet_type=st.sidebar.selectbox("Diet Type",["Vegeterian","Non Vegetarian"]) # Create selectbox in sidebar for Diet_type
allergies=st.sidebar.selectbox("Allergies",["Allergies","None"]) # Create selectbox in sidebar for Allergies


# Calling all calculators
bmi=bmi_calculator(weight,height)
bmr=bmr_calculator(gender,age,weight,height)
tdee=tdee_calculator(bmr,activity)
calorie=calorie_target(tdee,aim)

# Creating columns on the Main page
col1,col2,col3,col4=st.columns(4)
col1.metric("BMI",bmi) # BMI Column with value
col2.metric("BMR",f"{bmr} kcal") # BMR Column with value
col3.metric("TDEE",f"{tdee} Kcal") # TDEE Column with value
col4.metric("Calorie Target",f"{calorie} Kcal") # Calorie Column with value

# creating tabs
tab1,tab2=st.tabs(['Diet Recommandation',"Health Assistant"])
with tab1:
    # creating button "Build My Diet Plan"
    if st.button("Build My Diet Plan"):
        if client:
            with st.spinner("Analyzing your details and creating a personalized diet plan for your body..."):
                # start of exception handling , try section
                try:
                    db=load_rag()
                    search_query=f"""diet_type {diet_type}
                                         Healthy food
                                         Protein
                                         Allergies {allergies}"""
                    docs=db.similarity_search(search_query,3)
                    context="\n\n".join([ doc.page_content for doc in docs])
                    prompt=f"""You are a helpful AI nutrition assistant.
                    Use the following nutrition knowledge to create a simple one-day diet plan.

                    NUTRITION KNOWLEDGE:{context}
                    USER INFORMATION:
                    Age: {age}
                    Gender: {gender}
                    Height: {height} cm
                    Weight: {weight} kg
                    Activity Level: {activity}
                    aim: {aim}
                    Diet Type: {diet_type}
                    Food Allergy: {allergies}
                    Estimated BMI: {bmi}
                    Estimated BMR: {bmr} kcal/day
                    Estimated TDEE: {tdee} kcal/day
                    Estimated Daily Calorie Target:
                    {calorie} kcal/day

                    Create the following:
                    1\. Breakfast
                    2\. Morning Snack
                    3\. Lunch
                    4\. Evening Snack
                    5\. Dinner

                    For every meal provide:
                    \- Food
                    \- Portion
                    \- Approximate calories
                    \- Approximate protein

                    IMPORTANT RULES:
                    \- Respect the user's diet type.
                    \- Do not recommend foods containing &#x20; the stated allergy.
                    \- Use the provided nutrition knowledge &#x20; when possible.
                    \- Keep the plan simple and practical.
                    \- Do not diagnose diseases.
                    \- Do not prescribe medicines.
                    \- Do not claim to cure diseases.
                    \- This is general wellness information, &#x20; not medical advice."""

                    # creating response from the AI
                    response=client.chat.completions.create(model="openai/gpt-oss-120b",
                            messages=[{
                                 "role":"user",
                                 "content":prompt
                            }])    
                    answer=response.choices[0].message.content  
                    st.markdown(answer)
                # except section      
                except:
                    st.error("RAG is not connected")

with tab2:
    # place where question will ask !
    question=st.text_area("Health Assistant",placeholder="Ask anything about nutrition, fitness, diet, or general health.")
    # After pressing button "Submit Question"
    if st.button("Submit Question"):
        with st.spinner("Wait......."):
            db=load_rag()
            docs=db.similarity_search(question,3)
            context="\n\n".join([doc.page_content for doc in docs])
            prompt=f"""You are an AI health and nutrition assistant.
                    Use the following knowledge to answer the user's question.

                    NUTRITION KNOWLEDGE:{context}
                    USER QUESTION:{question}
                    INSTRUCTIONS:
                    \- Answer clearly.
                    \- Keep the explanation beginner-friendly.
                    \- Use the provided knowledge when possible.
                    \- Do not invent medical facts.
                    \- Do not diagnose diseases.
                    \- Do not prescribe medicines.
                    \- Do not claim to cure diseases.
                    \- If the question concerns a serious &#x20; medical problem, recommend consulting &#x20; a qualified healthcare professional.
                    This application provides general health and nutrition information for educational and wellness purposes."""
            # Response from the "Ask AI"
            response=client.chat.completions.create(model="openai/gpt-oss-120b",
                                messages=[{
                                    "role":"user",
                                    "content":prompt
                                }])
            # Provide us answer
            answer=response.choices[0].message.content
            st.markdown(answer)
# Gives warning 
st.warning("Knowledge-based health information tools serve as guides, but they cannot replace a physical examination or professional medical diagnosis")


# folder ka naam data then put pdf nutrition
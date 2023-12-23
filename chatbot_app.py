import streamlit as st
import random
import pyttsx3
import speech_recognition as tp
from datetime import datetime
import pandas as pd

# Load data from CSV
data = pd.read_csv('Classes.csv')

def display_schedule_text(schedule):
    if not schedule:
        st.write("No classes scheduled.")
    else:
        st.write("Here is the class schedule:")
        # Convert schedule to a DataFrame for better table display
        schedule_df = pd.DataFrame(schedule, columns=["Day", "Time", "Subject"])

        # Display the DataFrame as a table
        st.table(schedule_df)

def display_schedule_audio(schedule, eng):
    if not schedule:
        st.write("No classes scheduled.")
        eng.say("No classes scheduled.")
        eng.runAndWait()
    else:
        st.write("Here is the class schedule:")
        eng.say("Here is the class schedule.")
        eng.runAndWait()
        schedule_df = pd.DataFrame(schedule, columns=["Day", "Time", "Subject"])
        st.table(schedule_df)
        for row in schedule:
            eng.say(str(row))
            eng.runAndWait()

def get_class_schedule(role, user_id, input_method):
    if role and user_id:
        user_id = int(user_id)
        schedule = data[(data[f"{role}_id"] == user_id)][["day", "time", "subject"]].values.tolist()
        if input_method == 'text':
            display_schedule_text(schedule)
        elif input_method == 'audio':
            eng = pyttsx3.init('sapi5')
            voices = eng.getProperty('voices')
            eng.setProperty('voice', voices[1].id)
            display_schedule_audio(schedule, eng)

def manage_classes(role, user_id, input_method):
    if input_method == 'text':
        day = st.text_input("Enter the day of the week (e.g., Monday): ")
        time = st.text_input("Enter the class time: ")
        subject = st.text_input("Enter the subject: ")
    elif input_method == 'audio':
        eng = pyttsx3.init('sapi5')
        voices = eng.getProperty('voices')
        eng.setProperty('voice', voices[1].id)

        st.write("Which day of the week?")
        eng.say("Which day of the week?")
        eng.runAndWait()
        rec3 = tp.Recognizer()
        with tp.Microphone() as source:
            st.write("user->", end='')
            rec3.adjust_for_ambient_noise(source, duration=.2)
            aa = rec3.listen(source)
            try:
                day = rec3.recognize_google(aa, language='en-in')
                day = role.lower()
                st.write(day)
            except:
                st.write("try again")

        st.write("What is the class timing?")
        eng.say("What is the class timing?")
        eng.runAndWait()
        rec4 = tp.Recognizer()
        with tp.Microphone() as source:
            st.write("user->", end='')
            rec4.adjust_for_ambient_noise(source, duration=.2)
            aa = rec4.listen(source)
            try:
                time = rec4.recognize_google(aa, language='en-in')
                time = role.lower()
                st.write(time)
            except:
                st.write("try again")

        st.write("What is the subject?")
        eng.say("What is the subject?")
        eng.runAndWait()
        rec5 = tp.Recognizer()
        with tp.Microphone() as source:
            st.write("user->", end='')
            rec5.adjust_for_ambient_noise(source, duration=.2)
            aa = rec5.listen(source)
            try:
                subject = rec5.recognize_google(aa, language='en-in')
                subject = role.lower()
                st.write(subject)
            except:
                st.write("try again")

    existing_class = data[(data[f"{role}_id"] == user_id) & (data["day"] == day) & (data["time"] == time)].iloc[0]

    if existing_class:
        st.write(f"bot->Class canceled: {subject} on {day} at {time}.")
        eng.say(f"Class canceled: {subject} on {day} at {time}.")
        eng.runAndWait()
    else:
        new_class = pd.DataFrame({"role_id": [user_id], "day": [day], "time": [time], "subject": [subject]})
        data = pd.concat([data, new_class], ignore_index=True)
        st.write(f"bot->Class requested: {subject} on {day} at {time}.")
        eng.say(f"Class requested: {subject} on {day} at {time}.")
        eng.runAndWait()

# Main Streamlit app
def main():
    st.title("WizzIQ Chatbot")

    # Global variable for key generation
    choice_input_key = 0

    user_id = None
    ui = None
    role = None

    def get_unique_key():
        nonlocal choice_input_key
        key = f"choice_input_{choice_input_key}"
        choice_input_key += 1
        return key

    def take_input():
        # Unique key for each selectbox
        choice_key = get_unique_key()

        choices = ["Text", "Audio"]
        choice = st.selectbox("Choose input method:", choices, key=choice_key)

        if choice == "Text":
            return 'text'
        elif choice == "Audio":
            return 'audio'

    ct = datetime.now()

    input_method = take_input()

    if input_method == 'text':
        ui = st.text_input("Enter your query:")

    elif input_method == 'audio':
        eng = pyttsx3.init('sapi5')
        voices = eng.getProperty('voices')
        eng.setProperty('voice', voices[1].id)
        st.warning("What is your query?")
        eng.say("What is your query?")
        eng.runAndWait()
        r = tp.Recognizer()
        with tp.Microphone() as source:
            #st.write("user->", end='')
            r.adjust_for_ambient_noise(source, duration=.2)
            aa = r.listen(source)
            try:
                ui = r.recognize_google(aa, language='en-in')
                ui = ui.lower()
                st.success(ui)
            except:
                st.write("try again")
                return  # Stop execution if there is an error in audio input

    if ui and any(keyword in ui for keyword in ['class schedule', 'when', 'schedule', 'what']):
        if input_method == 'text':
            role = st.text_input("Are you a 'student' or 'tutor'? ").lower()
            user_id = st.text_input("Enter your ID: ")
        elif input_method == 'audio':
            st.warning("Are you a student or tutor?")
            eng.say("Are you a student or tutor?")
            eng.runAndWait()
            rec1 = tp.Recognizer()
            with tp.Microphone() as source:
                #st.write("user->", end='')
                rec1.adjust_for_ambient_noise(source, duration=.2)
                aa = rec1.listen(source)
                try:
                    role = rec1.recognize_google(aa, language='en-in')
                    role = role.lower()
                    st.success(role)
                except:
                    st.write("try again")
                    eng.say("try again")
                    return
            
            st.warning("What is your ID?")
            eng.say("What is your ID?")
            eng.runAndWait()
            rec2 = tp.Recognizer()
            with tp.Microphone() as source:
                #st.write("user->", end='')
                
                aa = rec2.listen(source)
                try:
                    user_id = rec2.recognize_google(aa, language='en-in')
                    user_id = user_id.lower()
                    st.success(user_id)
                except:
                    st.write("try again")
                    eng.say("Try again")
                    return
            
        get_class_schedule(role, user_id, input_method)
    
    elif ui and any(keyword in ui for keyword in ['manage classes', 'cancel', 'add', 'insert', 'remove']):
        if input_method == 'text':
            role = st.text_input("Are you a 'student' or 'tutor'? ").lower()
            user_id = st.text_input("Enter your ID: ")
        
        elif input_method == 'audio':
            st.write("Are you a student or tutor?")
            rec1 = tp.Recognizer()
            with tp.Microphone() as source:
                st.write("user->", end='')
                rec1.adjust_for_ambient_noise(source, duration=.2)
                aa = rec1.listen(source)
                try:
                    role = rec1.recognize_google(aa, language='en-in')
                    role = role.lower()
                    st.write(role)
                except:
                    st.write("try again")
                    return
                    
            st.write("What is your ID?")
            rec2 = tp.Recognizer()
            with tp.Microphone() as source:
                st.write("user->", end='')
                
                aa = rec2.listen(source)
                try:
                    user_id = rec2.recognize_google(aa, language='en-in')
                    user_id = user_id.lower()
                    st.write(user_id)
                except:
                    st.write("try again")
                    return

        manage_classes(role, user_id, input_method)

    elif ui is None and input_method == 'audio':
        st.write("No speech detected. Please try again.")

if __name__ == "__main__":
    main()

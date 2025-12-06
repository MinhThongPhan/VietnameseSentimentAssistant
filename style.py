import streamlit as st
#Style
def loadStyle():
    return """
        <style>
        .stApp {
            background: linear-gradient(0deg, #13C6D6, #A35257);
        }
        div.stButton > button {
            background-color: #A35257;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            border: 2px solid black;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0px 4px 8px black;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #E0960B;
            border-color: black;
            
        }
        
        .title {
            font-size: 45px !important;
            color: white;
            text-shadow: 1px 1px 10px black;
            font-family: Arial, sans-serif !important;
        }

        .sub-title {
            font-size: 28px !important;
            font-weight: 600;
            color: white;
            text-shadow: 1px 1px 10px black;
            font-family: Arial, sans-serif !important;
            justify-items: center;
        }

        .bordered-text {
            font-size: 16px !important;
            font-weight: 600;
            color: white;
            text-shadow: 1px 1px 10px black;
            font-family: Arial, sans-serif !important;
        }
        
        </style>
        """
    
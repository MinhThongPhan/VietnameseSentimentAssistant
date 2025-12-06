import streamlit as st
import sqlite3
import datetime
import pandas as pd
from transformers import pipeline
from underthesea import word_tokenize
from style import loadStyle

#Pipeline
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="mr4/phobert-base-vi-sentiment-analysis",
        tokenizer="mr4/phobert-base-vi-sentiment-analysis"
    )

pipe = load_model()


#Database
conn = sqlite3.connect("history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        label TEXT,
        score REAL,
        time TEXT
    )
""")
conn.commit()


def save_to_db(text, label, score):
    cursor.execute(
        "INSERT INTO history(text, label, score, time) VALUES (?,?,?,?)",
        (text, label, score, datetime.datetime.now().isoformat())
    )
    conn.commit()


def get_history():
    cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 50")
    return cursor.fetchall()


#Preprocess
def preprocess(text):
    text = text.strip().lower()
    text = word_tokenize(text, format="text")
    return text


#Giao diện
st.markdown(loadStyle(), unsafe_allow_html=True)
st.markdown("<h1 class='title'>Vietnamese Sentiment Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='bordered-text'>By: Trần Phan Minh Thông - 3121410015.</p>", unsafe_allow_html=True)

user_input = st.text_input("Nhập câu", value="")

#Nút
if st.button("Phân tích cảm xúc"):
    if len(user_input.strip()) < 5:
        st.toast("Câu quá ngắn, phải nhiều hơn 5 ký tự.")
    elif len(user_input.strip()) >50:
        st.toast("Câu quá dài, phải ít hơn 50 ký tự.")
    else:
        clean_text = preprocess(user_input)
        result = pipe(clean_text)[0]

        label = result["label"]
        score = round(result["score"], 4)

        st.markdown("<h class='sub-title'>Kết quả</h>", unsafe_allow_html=True)
        st.write(f"**Cảm xúc:** {label}")
        st.write(f"**Độ tin cậy:** {score}")

        save_to_db(user_input, label, score)
        st.toast("Đã lưu vào lịch sử!")
        
        
#Lịch sử        
st.markdown("<h style='text-align: center;' class='sub-title'>Lịch sử</h>", unsafe_allow_html=True)

history = get_history()
if len(history) == 0:
    st.write("Chưa có dữ liệu.")
else:
    df = pd.DataFrame(history, columns=["id", "text", "label", "score", "time"])

    df["time"] = df["time"].apply(
        lambda t: datetime.datetime.fromisoformat(t).strftime("%d/%m/%Y - %H:%M:%S")
    )

    #hiện cột
    df = df[["id", "text", "label", "score", "time"]]
    #đổi tên cột
    df.columns = ["ID", "Câu đã nhập", "Phân loại", "Điểm", "Thời gian"]

    st.dataframe(df, width="stretch",hide_index=True)




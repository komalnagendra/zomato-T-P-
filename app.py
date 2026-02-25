import streamlit as st
import pandas as pd
import time
import plotly.express as px
import re

#step 1: Page_setup with css
st.set_page_config(
    page_title="MyFeeds@ZOMATO.com",
    page_icon=":dango:",
    layout="wide",
    initial_sidebar_state="expanded")

st.title(":red[Zomato|]Feeds:dumpling:",text_alignment="center")

st.markdown(''' 
            <style> 
                    .stApp { 
                        font-style: italic;              
                        }   
            </style>''', unsafe_allow_html=True)

#step 2: Data intialization and LLM

if 'db' not in st.session_state:
    st.session_state.db = []

if 'p' not in st.session_state:
    st.session_state.p = {
        "Pizza" : {
            "ts" : 5.0,
            "c" : 1,
            "icon" : "https://th.bing.com/th/id/OIP.OZny5F6g0QAQPLsU_4HnEAHaE8?w=275&h=183&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
            "data" : "cheese, mushroom, chicken",
            "variaty" : "veg, non-veg",
            "type" : "breads",
            "price" : 449.54
        },
        "Burger" : {
            "ts" : 4,
            "c"  : 1,
            "icon" : "https://th.bing.com/th/id/OIP.NyTWHuB1hxeFLThmmg1XjQHaE8?w=229&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
            "data" : "Cheese, Mushroom, Chicken",
            "variaty" : "veg, non-veg",
            "type": "breads",
            "price": 349.54
        },
        "French Fries" : {
            "ts" : 5.0,
            "c" : 1,
            "icon" : "https://th.bing.com/th/id/OIP.9MM9v7VZhiUSGon_EapRuwHaFj?w=206&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
            "data" : "cheese, mushroom, chicken",
            "variaty" : "veg",
            "type" : "snacks",
            "price" : 199.54
        },
        "Pasta" : {
            "ts" : 5.0,
            "c"  : 1,
            "icon" : "https://th.bing.com/th/id/OIP.7Z_920eymh8JocugnBWFYwHaHa?w=208&h=208&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
            "data" : "Mushroom, Chicken",
            "variaty" : "veg, non-veg",
            "type": "snacks",
            "price": 149.54
        },
        "Biryanis" : {
            "ts" : 3.8,
            "c" : 1,
            "icon" : "https://th.bing.com/th/id/OIP.wBu0Xsb774mtzvjhq1C3DgHaE8?w=297&h=198&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
            "data" : "veg, mutton, chicken",
            "variaty" : "veg, non-veg",
            "type" : "main menu",
            "price" : 599.54
        }
    }
def analyse(t):
    t = t.lower()
    p = sum(t.count(w) for w in ["good", "excellent", "amazing", "delicious", "tasty"])
    n = sum(t.count(w) for w in ["bad", "terrible", "awful", "disgusting", "horrible"])
    if p > n:
        return "Positive", "#008000"
    elif n > p:
        return "Negative", "#F30E0A"
    else:
        return "Neutral", "#B1F6FA"

#step 3: UI page with CSS

options = st.sidebar.radio(":red[Menu]",["Feedback","Analytics"])

if options == "Feedback":
    st.badge("Explore our menu", color = "green")
    cols = st.columns(5)

    for i, (name, info) in enumerate(st.session_state.p.items()):
        with cols[i]:
            avg = round(info['ts']/info['c']) 

            st.image(info['icon'], use_container_width=True)
            st.subheader(name)
            st.write("⭐" * int(avg))
            st.badge(info.get("variaty"), color="yellow")
            st.badge(info.get("type"), color="blue")
            st.badge(info["data"], color="gray")
            st.badge(f"Price: ₹{info['price']}", color="orange")
            st.expander("Reviews")
            for r in [r for r in st.session_state.db if r['prod'] == name[::-1]]:
                st.markdown(f''' 
                        <div style='background-color:black; color:white;">
                            <div style="
                                border-left: 5px solid {r['color']};
                                padding-left: 8px;">
                                    <small> {r['email']} 
                            </div>
                        </div>
                    ''',unsafe_allow_html=True)


    st.divider()
    st.badge("Feedback Form", color="red")
    c1, c2 = st.columns(2)
    with c1:
        em = st.text_input("email:")
        pr = st.selectbox("Select Item to review", ["--select--", "Pizza", "Burger", "French fries", "Pasta", "Biryanis"])
        sr = st.select_slider("Rate the Item", [1,2,3,4,5],3)
    with c2:
        tx = st.text_area("write your Feedback,", height=180)
        if st.button("Submit"):
            if not re.match(r"^[a-zA-Z0-9,_%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9,_%+-]{2,}$", em):
                st.error("Enter a valid email address.")
            elif any(r for r in st.session_state.db if r["email"] == em and r["product"] == pr):
                st.warning("Already submitted feedback with this Email.")
            elif tx:
                sent, col = analyse(tx)
                st.session_state.db.append({
                    "email": em,
                    "product": pr,
                    "text": tx,
                    "rating": sr,
                    "sentiment": sent,
                    "color": col})
                st.session_state.p[pr]["c"] += 1
                st.success(f"{em} \n Thankyou for your feedback ")
                time.sleep(1)
                st.rerun()

elif options == "Analytics":
    st.badge("Analytics Dashboard", color = "blue")

#step 4: Analytics


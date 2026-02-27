import streamlit as st
import json
import os

st.set_page_config(page_title="news2：ニュース掲示板", layout="wide")
st.title("📰 NewsAPI × Streamlit ニュース")

if os.path.exists("latest_news.json"):
    with open("latest_news.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    st.success(f"✅ 最終更新：{data['updated_at']}")
    
    tabs = st.tabs(list(data['categories'].keys()))
    for i, cat_name in enumerate(data['categories']):
        with tabs[i]:
            for item in data['categories'][cat_name]:
                with st.container(border=True):
                    st.subheader(item['title'])
                    st.caption(f"📍 {item['source']}")
                    st.write(item['summary'])
                    st.link_button("🌐 原文をチェック", item['link'])
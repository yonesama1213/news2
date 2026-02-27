import streamlit as st
import json
import os

st.set_page_config(page_title="news2：ニュース掲示板", layout="wide")
st.title("📰 NewsAPI × Streamlit ニュース")

if os.path.exists("latest_news.json"):
    with open("latest_news.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    st.success(f"✅ 最終更新：{data['updated_at']}")
    
    # 💡 ここでカテゴリーがあるかチェックする
    categories = list(data.get('categories', {}).keys())
    
    if len(categories) > 0:
        tabs = st.tabs(categories)
        for i, cat_name in enumerate(categories):
            with tabs[i]:
                for item in data['categories'][cat_name]:
                    with st.container(border=True):
                        st.subheader(item['title'])
                        st.caption(f"📍 {item['source']}")
                        st.write(item['summary'])
                        st.link_button("🌐 原文をチェック", item['link'])
    else:
        # データが空の場合のメッセージ
        st.info("📢 現在、表示できるニュースがありません。しばらくしてから再度ご確認ください。")
else:
    st.warning("⚠️ ニュースデータが見つかりません。")
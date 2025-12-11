import os
import streamlit as st
from openai import OpenAI

# 取得 API key（可以用 Streamlit secrets 或環境變數）
api_key = st.secrets.get("OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("尚未設定 OPENAI_API_KEY，請到 Secrets 或環境變數中設定。")
else:
    client = OpenAI(api_key=api_key)

st.title("AI 小幫手 Demo")

st.write("這個 demo 提供兩個功能：")
st.markdown("1. **筆記整理：** 幫你產生標題與摘要。")
st.markdown("2. **中翻英：** 將中文翻譯成英文。")

mode = st.radio(
    "請選擇功能：",
    ("筆記整理（標題＋摘要）", "中翻英翻譯"),
)

text = st.text_area("請輸入文字：", height=200)

if st.button("送出"):
    if not api_key:
        st.error("尚未設定 OPENAI_API_KEY，無法呼叫模型。")
    elif not text.strip():
        st.warning("請先輸入一些文字再按送出。")
    else:
        with st.spinner("AI 思考中..."):
            if mode == "筆記整理（標題＋摘要）":
                user_prompt = (
                    "請幫我為以下內容產生：\n"
                    "1. 一個不超過 20 字的標題\n"
                    "2. 一段 1~3 句的摘要\n\n"
                    f"內容如下：\n{text}"
                )
            else:  # 中翻英
                user_prompt = (
                    "請把下面的中文翻譯成自然的英文，保持原本的語氣與意思：\n\n"
                    f"{text}"
                )

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一個會說繁體中文的助手，請用清楚、簡潔的方式回答使用者。"
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ]
                )

                result = response.choices[0].message.content
                st.markdown("### ✅ AI 回應")
                st.write(result)

            except Exception as e:
                st.error(f"呼叫 OpenAI API 發生錯誤：{e}")

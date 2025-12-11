import streamlit as st

st.title("AI 小幫手 Demo（無 API 版）")

st.write("這個 demo 提供兩個功能（不連線到任何外部 API，只做本地示範）：")
st.markdown("1. **筆記整理：** 用簡單規則產生標題與摘要。")
st.markdown("2. **中翻英：** 用簡單字典做示意翻譯（不是真正的 AI 翻譯）。")

mode = st.radio(
    "請選擇功能：",
    ("筆記整理（標題＋摘要）", "中翻英示意翻譯"),
)

text = st.text_area("請輸入文字：", height=200)


def simple_summarize(txt: str):
    """非常簡單的本地『假 AI』摘要函式。"""
    txt = txt.strip().replace("\n", " ")
    if not txt:
        return "（沒有輸入內容）", "（沒有摘要）"

    # 標題：取前 15 個字 + ...
    title = txt[:15]
    if len(txt) > 15:
        title += "..."

    # 摘要：取前 60 個字
    summary = txt[:60]
    if len(txt) > 60:
        summary += "..."

    return title, summary


def simple_zh2en(txt: str):
    """非常簡單的『示意翻譯』，只做部分字詞替換。"""
    mapping = {
        "你好": "hello",
        "謝謝": "thank you",
        "老師": "teacher",
        "同學": "classmate",
        "報告": "report",
        "作業": "homework",
        "航空": "aviation",
        "飛機": "airplane",
        "機師": "pilot",
    }

    result = txt
    for zh, en in mapping.items():
        result = result.replace(zh, en)

    return (
        "※ 以下為示意翻譯（非真正 AI 翻譯）：\n\n"
        + result
    )


if st.button("送出"):
    if not text.strip():
        st.warning("請先輸入一些文字再按送出。")
    else:
        if mode == "筆記整理（標題＋摘要）":
            title, summary = simple_summarize(text)
            st.markdown("### 📝 產生的標題")
            st.success(title)
            st.markdown("### 📌 產生的摘要")
            st.info(summary)
            st.caption("※ 本功能為規則式示意，不使用真正的 AI API。")

        else:  # 中翻英示意翻譯
            result = simple_zh2en(text)
            st.markdown("### 🌐 示意翻譯結果")
            st.code(result)
            st.caption("※ 僅做部分關鍵字替換，用於展示 Demo 流程。")

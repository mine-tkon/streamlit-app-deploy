import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

# APIキーの取得（Streamlit Secrets または .env）
api_key = os.getenv("OPENAI_API_KEY")
if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# 加点4. 専門家設定の辞書管理
EXPERT_PROMPTS = {
    "プログラミング講師": "あなたは親切で分かりやすいプログラミング講師です。初心者が理解できるように丁寧に解説してください。",
    "ビジネスコンサルタント": "あなたは論理的で実績豊富なビジネスコンサルタントです。要点を明確にし、実用的なアドバイスを提供してください。"
}

# 必須2. 関数の定義と利用（2引数の受け渡し）
def get_answer(user_text, expert_choice):
    # 加点1. エラーハンドリング
    try:
        # 必須1. LangChainの使用
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        system_message = EXPERT_PROMPTS[expert_choice]
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_text)
        ]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        st.error(f"エラー: {e}")
        return None

# アプリUI設定
st.title("AI専門家相談アプリ 🤖")

# 必須5. アプリ説明テキストの表示
st.markdown("このアプリでは質問内容を送ると、選択した専門家としてAIから回答が表示されます。")

# 加点3. 会話履歴管理（初期化）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 必須3. ラジオボタンによる専門家切替
expert_choice = st.radio(
    "回答してもらう専門家を選択してください:",
    list(EXPERT_PROMPTS.keys())
)

user_text = st.text_area("質問を入力してください:")

if st.button("回答を生成する"):
    if user_text:
        # 加点2. ローディング表示
        with st.spinner("回答を生成中です..."):
            response = get_answer(user_text, expert_choice)
            if response:
                # 会話履歴に追加
                st.session_state.messages.append({"role": "user", "content": user_text, "expert": expert_choice})
                st.session_state.messages.append({"role": "assistant", "content": response, "expert": expert_choice})
                
                # 必須4. LLM回答の画面表示
                st.subheader("生成結果")
                st.write(response)
    else:
        st.warning("質問を入力してください。")

# 会話履歴の表示
if st.session_state.messages:
    st.divider()
    st.subheader("過去の会話履歴")
    for msg in st.session_state.messages:
        label = f"あなた（{msg['expert']}へ）" if msg["role"] == "user" else f"AI（{msg['expert']}）"
        st.markdown(f"**{label}:** {msg['content']}")
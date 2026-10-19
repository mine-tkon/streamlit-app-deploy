import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. 環境変数の読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit Cloud環境の場合はSecretsからキーを取得
if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# 2. 画面の作成
st.title("AI 回答アプリ 🤖")
st.write("質問を入力して実行ボタンを押すと、AIが答えてくれます。")

# 3. ユーザーの入力フォーム
user_input = st.text_area("質問を入力してください:")

# 4. ボタンが押されたときの処理
if st.button("回答を生成する"):
    if not api_key:
        st.error("エラー: OpenAI APIキーが設定されていません。")
    elif not user_input.strip():
        st.warning("質問内容を入力してください。")
    else:
        client = OpenAI(api_key=api_key)
        
        with st.spinner("AIが考え中..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "あなたは親切なAIです。"},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                st.subheader("生成結果")
                st.write(answer)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
import subprocess
import streamlit as st
import openai
import asyncio

# ChatGPT APIのエンドポイント
chatgpt_url = "https://api.openai.com/v1/chat/completions"
# ChatGPT APIのトークン読み込み/GPT-3.5 TurboのAPIキーを設定
openai.api_key = st.secrets["chatgpt_api_key"]

async def get_audio_query():
    # audio_queryコマンドを実行
    audio_query_cmd = 'curl -s -X POST "localhost:50021/audio_query?speaker=1" --get --data-urlencode text@text.txt > ' \
                      'query.json '
    subprocess.run(audio_query_cmd, shell=True, check=True)

    # synthesisコマンドを実行
    synthesis_cmd = 'curl -s -H "Content-Type: application/json" -X POST -d @query.json ' \
                    '"localhost:50021/synthesis?speaker=1" '
    response = subprocess.run(synthesis_cmd, shell=True, check=True, capture_output=True)

    # 音声をファイルに保存する
    with open("audio.wav", "wb") as file:
        file.write(response.stdout)

# Streamlitアプリのタイトルとテキスト入力
st.title("Voicevox Core with ChatGPT Streamlit Demo For AIIT System Programming Report 4")
text_input = st.text_area("Enter a prompt:", value="AIITの大喜利をして20文字以内", key="text_input")  # keyを追加

if st.button("Generate Voice", key="generate_button"):  # keyを追加
    # ChatGPTによるテキスト生成
    messages = [{"role": "user", "content": text_input + " 10文字以上50文字以内で答えよ"}]
    st.write("Messages:", messages)  # 追加
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response_data = completion["choices"][0]["message"]["content"].strip()
    st.write("Response Data:", response_data)  # 追加

    # テキストをファイルに書き出す
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(response_data)

    # 非同期処理を実行する
    st.spinner("音声生成中...")
    asyncio.run(get_audio_query())
    st.success("音声生成が完了しました！")
    st.audio("audio.wav", format="audio/wav")
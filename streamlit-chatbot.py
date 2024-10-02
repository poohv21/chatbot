# streamlit_chatbot.py

# 필요한 라이브러리 임포트
import streamlit as st
from openai import OpenAI

# 사이드바 설정
with st.sidebar:
    # OpenAI API 키 입력 필드 생성
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    # API 키 획득 링크
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    # 소스 코드 링크
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    # GitHub Codespaces 링크
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

# 앱 제목 설정
st.title("💬 Chatbot")

# 세션 상태에 메시지 목록이 없으면 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 저장된 모든 메시지 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    # API 키가 없으면 경고 메시지 표시 후 중지
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 사용자 메시지 화면에 표시
    st.chat_message("user").write(prompt)
    # OpenAI API를 사용하여 응답 생성
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # 응답 메시지 추출
    msg = response.choices[0].message.content
    # 응답을 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": msg})
    # 응답 화면에 표시
    st.chat_message("assistant").write(msg)

import streamlit as st
import json
import zipfile
import os
import shutil  
import openai
from datetime import datetime

# 압축 파일이 있는 디렉토리 경로 설정 (실제 경로로 변경)
zip_dir = r"jinlo"  # 압축 파일들이 있는 디렉토리 경로

# 디렉토리 유효성 검사
if not os.path.exists(zip_dir):
    raise FileNotFoundError(f"지정된 경로를 찾을 수 없습니다: {zip_dir}")

# 압축 파일 목록 확인
zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]

if zip_files:
    print(f"Found {len(zip_files)} zip files in the directory: {zip_files}")
else:
    raise FileNotFoundError("No zip files found. Please check the directory path.")

# 압축 파일 해제 및 데이터 파일 읽기
def load_all_data(zip_dir, zip_files):
    all_data = []
    extracted_dir_base = "extracted_data"

    for zip_file in zip_files:
        zip_path = os.path.join(zip_dir, zip_file)
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"ZIP 파일을 찾을 수 없습니다: {zip_path}")
        extracted_dir = os.path.join(extracted_dir_base, zip_file[:-4])  # 각 압축 파일의 이름으로 디렉토리 생성

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)

        # JSON 파일 리스트를 가져옵니다.
        json_files = [f for f in os.listdir(extracted_dir) if f.endswith('.json')]

        # 각 JSON 파일에서 데이터 추출
        for json_file in json_files:
            file_path = os.path.join(extracted_dir, json_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Ensure the data is parsed as JSON
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
        shutil.rmtree(extracted_dir)
    return all_data

# 상담 데이터를 추출하여 필요한 형식으로 변환하는 함수
def extract_data(json_data):
    extracted_data = []
    for counseling_record in json_data:
        if isinstance(counseling_record, dict):
            meta = counseling_record.get("Meta", {})
            conversations = counseling_record.get("Conversation", {})

            # 상담 정보 추출
            counseling_info = {
                "student_id": meta.get("student idx", ""),
                "counseling_index": meta.get("counseling_idx", ""),
                "counselor_id": meta.get("counsellor_idx", ""),
                "counseling_purpose": meta.get("CounsellingPurpose", ""),
                "counseling_satisfaction": meta.get("counselling_satisfaction", ""),
                "counseling_date": meta.get("counselling_date", ""),
                "utterances": []
            }

            # 대화 내용 추출
            for conv_idx, conv_data in conversations.items():
                utterances = conv_data.get("Utterances", [])
                for utterance in utterances:
                    counseling_info["utterances"].append({
                        "speaker_id": utterance.get("speaker_idx", ""),
                        "utterance_text": utterance.get("utterance", "")
                    })

            extracted_data.append(counseling_info)

    return extracted_data

# CareerCounselingChatbot 클래스 정의
class CareerCounselingChatbot:
    def __init__(self, counseling_data):
        self.counseling_data = counseling_data
        self.questions = [
            "안녕하세요! 진로 상담을 시작하겠습니다. 진로 상담을 받고 싶으신 이유는 무엇인가요?",
            "어떤 분야에 관심이 있으신가요? (예: 기술, 서비스, 생산, 사무)",
            "어떤 일을 할 때 가장 즐거우셨나요?",
            "주로 어떤 능력을 발휘하고 싶으신가요? (예: 기술적 능력, 대인 관계 능력)",
            "원하는 직업의 근무 환경은 어떤가요? (예: 실내, 실외, 혼합)"
        ]
        self.answers = []
        self.current_question_idx = 0

    def recommend_career(self):
        # 사용자 응답을 바탕으로 직업을 추천하는 로직
        interest = self.answers[1] if len(self.answers) > 1 else ""
        enjoyment = self.answers[2] if len(self.answers) > 2 else ""
        skills = self.answers[3] if len(self.answers) > 3 else ""
        environment = self.answers[4] if len(self.answers) > 4 else ""

        # 여기서는 간단히 예시를 위해 특정 키워드에 따라 직업을 추천합니다.
        if "기술" in interest:
            return "소프트웨어 개발자"
        elif "서비스" in interest:
            return "고객 서비스 담당자"
        elif "생산" in interest:
            return "생산 관리자"
        elif "사무" in interest:
            return "사무 관리자"
        else:
            return "다양한 직업이 있습니다. 추가 정보를 제공해주세요."

    def chat(self, user_input=None):
        if user_input:
            self.answers.append(user_input)
            self.current_question_idx += 1

        if self.current_question_idx < len(self.questions):
            response = self.questions[self.current_question_idx]
        else:
            response = self.recommend_career()

        return response

    def get_initial_question(self):
        if self.current_question_idx < len(self.questions):
            return self.questions[self.current_question_idx]
        else:
            return "질문이 완료되었습니다. 직업을 추천합니다."

# 데이터 로딩
zip_dir = r"jinlo"  # ZIP 파일들이 위치한 디렉토리
zip_files = ['TL_01. 학교급_01. 초등.zip', 'TL_01. 학교급_02. 중등.zip', 'TL_01. 학교급_03. 고등.zip', 
             'TL_02. 추천직업 카테고리_01. 기술계열.zip', 'TL_02. 추천직업 카테고리_02. 서비스계열.zip', 
             'TL_02. 추천직업 카테고리_03. 생산계열.zip', 'TL_02. 추천직업 카테고리_04. 사무계열.zip', 
             'TS_01. 학교급_01. 초등.zip', 'TS_01. 학교급_02. 중등.zip', 'TS_01. 학교급_03. 고등.zip']  # 처리할 ZIP 파일 목록

# 압축 파일에서 모든 데이터 로드
all_data = load_all_data(zip_dir, zip_files)
# 데이터를 필요한 형식으로 추출
extracted_data = extract_data(all_data)

# Streamlit 앱
title_html = """
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; border: 2px solid black;">
    <h1 style="text-align: center; color: #333333;">🎓 진로 상담 챗봇 👨‍🏫</h1>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)

# 사이드바 생성
with st.sidebar:
    # OpenAI API 키 입력받기
    openai.api_key = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

    st.markdown("---")

    # GPT 모델을 선택하기 위한 라디오 버튼 생성
    model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

    st.markdown("---")

    # 리셋 버튼 생성
    if st.button(label="초기화"):
        # 리셋 코드 
        st.session_state["chat"] = []
        st.session_state["messages"] = [{"role": "system", "content": "You are a has personality assistant. Respond to all input in 25 words and answer in korea"}]

# 세션 상태 초기화
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    st.session_state.question_idx = 0
    st.session_state.answers = []
    st.session_state.user_input = ''  # 사용자 입력 상태 초기화

# 챗봇 인스턴스 생성 (초기화는 한 번만 수행)
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.initial_question_displayed = False  # 초기 질문이 표시되었는지 여부를 나타내는 변수 추가

# 입력이 변경되었을 때의 콜백 함수 정의
def on_change():
    user_input = st.session_state.input_question
    if user_input:
        # API 키 확인
        if openai.api_key:
            # 채팅을 시각화하기 위해 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state.get("chat", []) + [("🙋", now, user_input)]
            # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state.get("messages", []) + [{"role": "user", "content": user_input}]
            st.session_state["user_input"] = user_input

            if not st.session_state.chatbot:
                st.session_state.chatbot = CareerCounselingChatbot(extracted_data)

            if not st.session_state.initial_question_displayed:
                st.session_state["initial_question_displayed"] = True  # 초기 질문 표시 상태 업데이트

            # 챗봇 응답 생성
            response = st.session_state.chatbot.chat(user_input)
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("🙇", now, response)]
            st.session_state["user_input"] = ""
        else:
            st.error("OpenAI API 키를 입력하세요.")

# 초기 질문 출력
if not st.session_state.get("initial_question_displayed", False):
    initial_question = "안녕하세요! 진로 상담을 시작하겠습니다. 진로 상담을 받고 싶으신 이유는 무엇인가요?"
    st.session_state["chat"] = st.session_state.get("chat", []) + [("🙇", datetime.now().strftime("%H:%M"), initial_question)]
    st.session_state["initial_question_displayed"] = True  # 초기 질문 출력 후에 상태를 True로 설정

# 대화 히스토리를 저장하는 함수
def save_conversation():
    # 대화 히스토리 저장
    with open("conversation_history.txt", "a", encoding="utf-8") as f:
        f.write("대화 히스토리\n")
        for sender, time, message in st.session_state.get("chat", []):
            f.write(f"{sender} {time}: {message}\n")

    # 상담 종료 메시지 추가
    now = datetime.now().strftime("%H:%M")
    st.session_state["chat"] = st.session_state.get("chat", []) + [("🙇", now, "상담을 종료합니다.")]
    st.session_state["initial_question_displayed"] = False  # 초기 질문 상태 초기화

# 기능 구현 공간
col1, col2 = st.columns(2)
with col1:
    # 현재 대화 내용 출력
    for sender, time, message in st.session_state.get("chat", []):
        if sender == "🙋":
            color = "black"
            st.write(f'<div style="color:{color};font-size:16px;">🙋익명 {time}</div><div style="background-color:#f0f0f0;color:black;border-radius:12px;padding:10px 10px;margin:10px 0;float:left;">{message}</div>', unsafe_allow_html=True)
        else:
            color = "black"
            st.write(f'<div style="color:{color};font-size:16px;text-align:right;">🙇진로상담사 {time}</div><div style="background-color:#ffcccb;color:black;border-radius:12px;padding:10px 10px;margin:10px 0; float:right; width:98%; height:50%;">{message}</div>', unsafe_allow_html=True)

with col2:
    st.write("")
# 상담 종료 버튼 생성
if st.button("상담 종료"):
    save_conversation()  # 대화 히스토리 저장
    st.session_state.chat = []  # 대화 초기화
    st.info("상담이 종료되었습니다.")

# 텍스트 입력 상자 및 버튼을 아래에 배치
question = st.text_input("질문을 입력하세요", key="input_question", on_change=on_change)

if not openai.api_key:
    st.error("OpenAI API 키를 입력하세요. *-입력하지 않을 시 답변이 제한적입니다.-*")
else:
    if st.button("질문"):
        if question:
            # 채팅을 시각화하기 위해 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state.get("chat", []) + [("🙋", now, question)]
            # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state.get("messages", []) + [{"role": "user", "content": question}]
            st.session_state["user_input"] = question

            # 챗봇 응답 생성
            response = st.session_state.chatbot.chat(question)
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("🙇", now, response)]
            st.session_state["user_input"] = ""
        else:
            st.error("질문을 입력하세요.")

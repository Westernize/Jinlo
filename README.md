# 🎓 진로 상담 챗봇 (Career Counseling Chatbot)

Streamlit과 OpenAI GPT API를 활용하여 개발한 진로 상담 챗봇입니다.  
실제 상담 데이터를 기반으로 사용자의 관심 분야, 성향, 환경 등을 분석하여 적절한 직업을 추천합니다.

---

## 🧾 프로젝트 개요

- **목적**: 상담 데이터를 기반으로 한 진로 추천 프로세스를 자동화해보고, GPT를 활용한 자연스러운 상담 시나리오를 구성
- **주요 기술**: `Streamlit`, `OpenAI API`, `Python`, `JSON`, `파일 입출력`, `pytz`
- **사용자 흐름**: 질문 → 답변 → 직업 추천 → 대화 기록 저장

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 📦 ZIP 데이터 자동 처리 | 상담 데이터가 들어 있는 ZIP 파일 자동 해제 및 JSON 파싱 |
| 🧠 GPT 진로 상담 | GPT-3.5 또는 GPT-4 기반 대화형 질문 시퀀스 |
| 📝 직업 추천 | 입력된 관심 분야, 성향, 환경 기반으로 간단한 로직으로 직업 추천 |
| 💬 대화 기록 저장 | 상담 종료 시 `conversation_history.txt`에 전체 대화 저장 |
| 🎛️ 사용자 UI | Streamlit으로 간단하고 직관적인 웹 UI 구성 |

---

## 🧑‍💻 사용 기술

- **Python 3.9+**
- **Streamlit**: 웹 인터페이스 구현
- **OpenAI API**: 챗봇 대화 생성 (GPT-3.5, GPT-4)
- **pandas / JSON**: 상담 데이터 처리
- **pytz**: 로컬 시간 출력 처리 (Asia/Seoul)

---

## 💡 실행 방법

1. 리포지토리 클론

```bash
git clone https://github.com/your-username/career-counseling-chatbot.git
cd career-counseling-chatbot
가상 환경 생성 (선택)

bash
코드 복사
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
패키지 설치

bash
코드 복사
pip install -r requirements.txt
jinlo/ 폴더에 상담 관련 .zip 파일을 넣습니다.

실행

bash
코드 복사
streamlit run jinlo.py
📁 폴더 구조
python
코드 복사
📦 프로젝트 루트
├── jinlo.py                    # Streamlit 메인 앱
├── requirements.txt            # 의존성 패키지
├── 📁 jinlo/                    # 상담 데이터 위치
│   ├── TL_01. 학교급_03. 고등.zip
│   ├── TL_02. 추천직업 카테고리_01. 기술계열.zip
│   ├── TL_02. 추천직업 카테고리_02. 서비스계열.zip
│   ├── TL_02. 추천직업 카테고리_03. 생산계열.zip
│   ├── TL_02. 추천직업 카테고리_04. 사무계열.zip
│   ├── TS_01. 학교급_03. 고등.zip
│   └── 📁 (자동 생성된 압축 해제 폴더들)
└── conversation_history.txt    # 상담 종료 시 생성되는 대화 로그
🎯 상담 흐름 예시
scss
코드 복사
Q1. 진로 상담을 받고 싶은 이유는 무엇인가요?
Q2. 어떤 분야에 관심이 있으신가요? (예: 기술, 서비스, 생산, 사무)
Q3. 어떤 일을 할 때 가장 즐거우셨나요?
Q4. 주로 어떤 능력을 발휘하고 싶으신가요? (기술적 능력, 대인관계 등)
Q5. 원하는 직업의 근무 환경은 어떤가요? (실내, 실외 등)
입력된 응답을 바탕으로 예를 들어 "기술", **"코딩이 즐겁다"**는 응답을 입력하면 → 소프트웨어 개발자 추천

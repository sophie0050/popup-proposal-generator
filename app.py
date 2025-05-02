import streamlit as st
import openai

# UI 구성
st.set_page_config(page_title="📄 팝업스토어 제안서 초안 생성기", layout="wide")
st.title("🧾 팝업스토어 제안서 자동 생성기")

# 입력값 받기
with st.form("proposal_form"):
    brand = st.text_input("브랜드명", placeholder="예: 하감자")
    target = st.text_input("타깃 (나이대, 성별 등)", placeholder="예: 20대 여성")
    location = st.text_input("장소", placeholder="예: 성수동")
    period = st.text_input("운영 기간", placeholder="예: 3일")
    theme = st.text_input("콘셉트 / 키워드", placeholder="예: 감성, 체험, SNS 인증")
    goal = st.text_area("목표 (선택사항)", placeholder="예: 브랜드 인지도 제고, 고객 참여 유도")
    api_key = st.text_input("OpenAI API 키", type="password")
    submitted = st.form_submit_button("제안서 초안 생성하기")

# GPT 프롬프트 구성 함수
def generate_prompt(brand, target, location, period, theme, goal):
    prompt = f"""
당신은 브랜드 기획 전문가입니다.
아래 정보를 바탕으로 팝업스토어 기획 제안서 초안을 작성해주세요.

- 브랜드명: {brand}
- 타깃: {target}
- 장소: {location}
- 운영 기간: {period}
- 콘셉트 키워드: {theme}
"""
    if goal:
        prompt += f"- 목적: {goal}\n"

    prompt += """
제안서 구성은 아래 항목을 포함해주세요:
1. 프로젝트 개요
2. 타깃 분석
3. 콘셉트 제안
4. 공간 및 프로그램 구성
5. 운영 계획 (간단하게)
6. 기대 효과

형식은 마치 실제 문서처럼 자연스럽고 읽기 좋게 작성해주세요.
문장체로 써주시고, 각 항목은 제목을 달아 구분해주세요.
A4 1~2장 분량 정도로 작성해주세요.
"""
    return prompt

# GPT 호출 함수
def get_proposal(prompt, api_key):
    try:
        openai.api_key = api_key
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[오류] {e}"

# 실행
if submitted:
    if not all([brand, target, location, period, theme, api_key]):
        st.warning("필수 입력값을 모두 채워주세요.")
    else:
        with st.spinner("제안서 생성 중..."):
            prompt = generate_prompt(brand, target, location, period, theme, goal)
            result = get_proposal(prompt, api_key)
        st.markdown("### ✨ 제안서 초안")
        st.write(result)

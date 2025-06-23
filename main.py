#!/usr/bin/env python3
"""
인스타툰 스토리보드 생성기
GPT-4.1 모델을 사용하여 사용자 입력을 기반으로 인스타툰 스토리보드를 JSON 형태로 생성합니다.
"""

import json
import sys
from typing import Dict, List, Optional
import requests
from gpt_client import GPTClient, GPTConfig
from config import Config


class InstaToonGenerator:
    def __init__(self):
        self.model = "gpt-4.1"
        self.prompt_template = self._load_prompt_template()
        self.gpt_client = None
        self._initialize_gpt_client()
    
    def _initialize_gpt_client(self):
        """GPT 클라이언트를 초기화합니다."""
        try:
            self.gpt_client = GPTClient()
            print("GPT-4.1 모델 연결 성공")
        except ValueError as e:
            print(f"GPT 클라이언트 초기화 실패: {e}")
            print("API 키 설정이 필요합니다.")
            self.gpt_client = None
    
    def _load_prompt_template(self) -> str:
        """프롬프트 템플릿을 로드합니다."""
        return """###지시사항
아래에 제공된 정보를 바탕으로, 독창적이면서도 명확한 스토리보드를 기획하십시오.

###작성지침
1. 필수 키워드·주제는 스토리 전반에 자연스럽게 녹여 넣으십시오.
2. 정방형(1 : 1) 이미지 10컷(10 페이지) 이내에서 플롯이 매끄럽게 이어지도록 균형 있게 배분하십시오.
3. 각 페이지마다 반드시 등장인물·배경·대사·표정/포즈를 기재하십시오.
4. 대사는 캐릭터 이름을 앞에 붙여 표기하십시오 예) 지민: "대사…".
5. 표정/포즈는 연출자가 즉시 이해할 만큼 구체적으로 기술하십시오.
6. 1 컷(페이지) = 1 JSON 객체이며, page 번호를 필수로 포함하십시오(업로드 순서 고정 목적).
7. 세이프 존(1080×1080 px 기준, 가장자리 120 px) 밖에 핵심 텍스트·캐릭터가 걸치지 않도록 유의하십시오.

###추가 세부 가이드
- 디자인‧연출: 컬러 팔레트·폰트·톤&매너를 일관되게 유지, 컷 간 시선 흐름(좌→우·상→하) 고려

###출력형식
json
{{
"wholeTitle": "<완결성 있는 한글 제목>",
"storyTopic": "<핵심 주제·메시지를 1-2문장으로 요약>",
"hashtags": ["<hashtag1>", "<hashtag2>", "<hashtag3>", "<hashtag4>", "<hashtag5>"],
"pages": [
{{
"page": 1,
"character": ["<캐릭터1>", ...],
"background": "<배경 설명>",
"dialogue": {{
"character1": "<대사1>",
"character2": "<대사2>"
}},
"expressionPose": "<주요 인물들의 표정과 액션>"
}}
]
}}

###등장인물
{characters}

###필수 키워드 및 주제
{keywords}

###줄거리
{plot}

###분량
{pages}장"""

    def validate_input(self, plot: str, pages: str) -> bool:
        """필수 입력값을 검증합니다."""
        if not plot or not plot.strip():
            print("오류: 줄거리는 필수 입력 항목입니다.")
            return False
        
        if not pages or not pages.strip():
            print("오류: 분량은 필수 입력 항목입니다.")
            return False
        
        try:
            page_num = int(pages)
            if page_num < 1 or page_num > 10:
                print("오류: 분량은 1-10 페이지 사이여야 합니다.")
                return False
        except ValueError:
            print("오류: 분량은 숫자로 입력해주세요.")
            return False
        
        return True

    def get_user_input(self) -> Dict[str, str]:
        """사용자로부터 입력을 받습니다."""
        print("=== 인스타툰 스토리보드 생성기 ===\n")
        
        characters = input("등장인물 (이름, 역할 등 간단히 입력): ").strip()
        keywords = input("필수 키워드 및 주제 (선택사항): ").strip()
        plot = input("* 줄거리 (필수): ").strip()
        pages = input("* 분량 (1-10페이지, 권장: 4-8페이지): ").strip()
        
        return {
            "characters": characters,
            "keywords": keywords,
            "plot": plot,
            "pages": pages
        }

    def generate_storyboard(self, user_input: Dict[str, str]) -> Optional[Dict]:
        """GPT 모델을 사용하여 스토리보드를 생성합니다."""
        if not self.gpt_client:
            print("GPT 클라이언트가 초기화되지 않았습니다. API 키를 확인해주세요.")
            return None
        
        prompt = self.prompt_template.format(
            characters=user_input["characters"] or "없음",
            keywords=user_input["keywords"] or "없음",
            plot=user_input["plot"],
            pages=user_input["pages"]
        )
        
        return self.gpt_client.generate_storyboard(prompt)

    def save_result(self, storyboard: Dict, filename: str = "storyboard.json"):
        """생성된 스토리보드를 JSON 파일로 저장합니다."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(storyboard, f, ensure_ascii=False, indent=2)
            print(f"스토리보드가 '{filename}' 파일로 저장되었습니다.")
            return True
        except Exception as e:
            print(f"파일 저장 중 오류가 발생했습니다: {e}")
            return False

    def run(self):
        """메인 실행 함수"""
        try:
            # 사용자 입력 받기
            user_input = self.get_user_input()
            
            # 입력값 검증
            if not self.validate_input(user_input["plot"], user_input["pages"]):
                return
            
            # 스토리보드 생성
            storyboard = self.generate_storyboard(user_input)
            
            if storyboard:
                # 결과 출력
                print("\n=== 생성된 스토리보드 ===")
                print(json.dumps(storyboard, ensure_ascii=False, indent=2))
                
                # 파일로 저장
                save_choice = input("\n파일로 저장하시겠습니까? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes', '예', 'ㅇ']:
                    filename = input("파일명 (기본값: storyboard.json): ").strip()
                    if not filename:
                        filename = "storyboard.json"
                    self.save_result(storyboard, filename)
            else:
                print("스토리보드 생성에 실패했습니다.")
                
        except KeyboardInterrupt:
            print("\n프로그램이 중단되었습니다.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


if __name__ == "__main__":
    generator = InstaToonGenerator()
    generator.run()
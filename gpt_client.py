"""
GPT-4.1 모델 연동을 위한 클라이언트 모듈
OpenAI API를 사용하여 GPT-4.1 모델과 통신합니다.
"""

import os
import json
import re
from typing import Dict, Optional
import requests
from dataclasses import dataclass


@dataclass
class GPTConfig:
    """GPT API 설정"""
    api_key: str
    model: str = "gpt-4.1"
    base_url: str = "https://api.openai.com/v1"
    max_tokens: int = 4000
    temperature: float = 0.7


class GPTClient:
    """GPT-4.1 모델과 통신하는 클라이언트"""
    
    def __init__(self, config: Optional[GPTConfig] = None):
        if config:
            self.config = config
        else:
            # 환경변수에서 API 키 로드
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY 환경변수를 설정해주세요.")
            
            self.config = GPTConfig(api_key=api_key)
    
    def _make_request(self, prompt: str) -> Optional[str]:
        """GPT API에 요청을 보냅니다."""
        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.config.model,
            'messages': [
                {
                    'role': 'system',
                    'content': '당신은 인스타툰 스토리보드 전문가입니다. 주어진 요구사항에 따라 정확한 JSON 형식의 스토리보드를 생성해주세요. 응답은 반드시 유효한 JSON 형식으로만 제공해주세요.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': self.config.max_tokens,
            'temperature': self.config.temperature
        }
        
        try:
            response = requests.post(
                f"{self.config.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"API 오류: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"네트워크 오류: {e}")
            return None
        except Exception as e:
            print(f"예상치 못한 오류: {e}")
            return None
    
    def _extract_json_from_response(self, response: str) -> Optional[str]:
        """응답에서 JSON을 추출합니다."""
        if not response:
            return None
        
        # 방법 1: ```json 코드 블록에서 추출
        json_block_pattern = r'```json\s*(.*?)\s*```'
        match = re.search(json_block_pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # 방법 2: ``` 코드 블록에서 추출 (json 키워드 없이)
        code_block_pattern = r'```\s*(.*?)\s*```'
        match = re.search(code_block_pattern, response, re.DOTALL)
        if match:
            potential_json = match.group(1).strip()
            if potential_json.startswith('{') and potential_json.endswith('}'):
                return potential_json
        
        # 방법 3: 첫 번째와 마지막 중괄호 사이의 내용 추출
        first_brace = response.find('{')
        last_brace = response.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
            return response[first_brace:last_brace + 1]
        
        # 방법 4: 전체 응답이 JSON인지 확인
        response_stripped = response.strip()
        if response_stripped.startswith('{') and response_stripped.endswith('}'):
            return response_stripped
        
        return None
    
    def _clean_json_string(self, json_str: str) -> str:
        """JSON 문자열을 정리합니다."""
        if not json_str:
            return json_str
        
        # 불필요한 공백 및 제어 문자 제거
        json_str = json_str.strip()
        
        # 시작과 끝의 백틱이나 기타 마크다운 문자 제거
        json_str = re.sub(r'^[`\s]*', '', json_str)
        json_str = re.sub(r'[`\s]*$', '', json_str)
        
        # json 키워드 제거 (시작 부분에 있는 경우)
        json_str = re.sub(r'^json\s*', '', json_str, flags=re.IGNORECASE)
        
        return json_str
    
    def generate_storyboard(self, prompt: str) -> Optional[Dict]:
        """스토리보드를 생성합니다."""
        print(f"GPT-{self.config.model} 모델로 스토리보드 생성 중...")
        
        response = self._make_request(prompt)
        
        if not response:
            print("GPT API로부터 응답을 받지 못했습니다.")
            return None
        
        print(f"GPT 응답 길이: {len(response)} 문자")
        
        # JSON 추출 시도
        json_str = self._extract_json_from_response(response)
        
        if not json_str:
            print("응답에서 JSON을 찾을 수 없습니다.")
            print(f"원본 응답 (처음 500자): {response[:500]}...")
            return None
        
        # JSON 문자열 정리
        json_str = self._clean_json_string(json_str)
        
        # JSON 파싱 시도
        try:
            storyboard = json.loads(json_str)
            print("JSON 파싱 성공!")
            
            # 필수 필드 검증
            required_fields = ['wholeTitle', 'storyTopic', 'hashtags', 'pages']
            missing_fields = [field for field in required_fields if field not in storyboard]
            
            if missing_fields:
                print(f"필수 필드가 누락되었습니다: {missing_fields}")
                return None
            
            return storyboard
            
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            print(f"파싱 시도한 JSON (처음 1000자):")
            print(json_str[:1000])
            print("..." if len(json_str) > 1000 else "")
            
            # 일반적인 JSON 오류 수정 시도
            try:
                # 후행 쉼표 제거
                fixed_json = re.sub(r',\s*}', '}', json_str)
                fixed_json = re.sub(r',\s*]', ']', fixed_json)
                
                # 이스케이프되지 않은 따옴표 수정 시도
                storyboard = json.loads(fixed_json)
                print("JSON 수정 후 파싱 성공!")
                return storyboard
                
            except json.JSONDecodeError as e2:
                print(f"JSON 수정 후에도 파싱 실패: {e2}")
                return None
        
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            return None
    
    def test_connection(self) -> bool:
        """API 연결을 테스트합니다."""
        test_prompt = "안녕하세요! 연결 테스트입니다. 간단한 JSON 응답을 주세요: {\"test\": \"success\"}"
        
        try:
            response = self._make_request(test_prompt)
            return response is not None
        except Exception:
            return False


def setup_api_key():
    """API 키 설정을 도와주는 함수"""
    print("OpenAI API 키 설정이 필요합니다.")
    print("1. 환경변수로 설정: export OPENAI_API_KEY='your-api-key'")
    print("2. .env 파일 생성하여 설정")
    
    api_key = input("API 키를 직접 입력하시겠습니까? (입력하지 않으려면 Enter): ").strip()
    
    if api_key:
        # .env 파일에 저장
        try:
            with open('.env', 'w') as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            print(".env 파일에 API 키가 저장되었습니다.")
            return api_key
        except Exception as e:
            print(f"파일 저장 오류: {e}")
    
    return None


if __name__ == "__main__":
    # 테스트 코드
    try:
        client = GPTClient()
        print("GPT 클라이언트 초기화 성공")
        
        if client.test_connection():
            print("API 연결 테스트 성공")
        else:
            print("API 연결 테스트 실패")
            
    except ValueError as e:
        print(f"설정 오류: {e}")
        setup_api_key()
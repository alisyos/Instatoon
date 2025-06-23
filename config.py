"""
설정 파일
환경변수 및 기본 설정을 관리합니다.
"""

import os
from typing import Optional


class Config:
    """애플리케이션 설정 클래스"""
    
    # GPT 모델 설정
    GPT_MODEL = "gpt-4.1"
    GPT_MAX_TOKENS = 4000
    GPT_TEMPERATURE = 0.7
    
    # 파일 설정
    DEFAULT_OUTPUT_FILENAME = "storyboard.json"
    
    # 페이지 설정
    MIN_PAGES = 1
    MAX_PAGES = 10
    RECOMMENDED_PAGES = (4, 8)
    
    # 이미지 설정
    IMAGE_SIZE = 1080  # 1080x1080 px
    SAFE_ZONE_MARGIN = 120  # px
    
    @classmethod
    def get_openai_api_key(cls) -> Optional[str]:
        """OpenAI API 키를 환경변수에서 가져옵니다."""
        return os.getenv('OPENAI_API_KEY')
    
    @classmethod
    def load_from_env(cls, env_files: list = None):
        """환경변수 파일에서 설정을 로드합니다."""
        if env_files is None:
            env_files = ['.env.local', '.env']
        
        for env_file in env_files:
            if os.path.exists(env_file):
                print(f"환경변수 파일 로드: {env_file}")
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value.strip('"\'')
                return  # 첫 번째로 찾은 파일만 로드
        
        print("환경변수 파일을 찾을 수 없습니다. (.env.local 또는 .env)")


# 환경변수 로드
Config.load_from_env()
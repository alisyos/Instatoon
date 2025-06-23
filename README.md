# 인스타툰 스토리보드 생성기

GPT-4.1 모델을 사용하여 사용자 입력을 기반으로 인스타툰 스토리보드를 JSON 형태로 자동 생성하는 도구입니다.

## 기능

- 사용자 친화적인 인터랙티브 입력 인터페이스
- GPT-4.1 모델을 통한 고품질 스토리보드 생성
- 정방형(1:1) 인스타그램 형식에 최적화
- JSON 형태의 구조화된 출력
- 세이프 존(1080×1080 px 기준, 가장자리 120 px) 고려

## 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정

다음 중 하나의 방법으로 설정:

**방법 1: .env.local 파일 생성 (권장)**
```bash
cp .env.example .env.local
# .env.local 파일을 열어서 실제 API 키로 수정
```

**방법 2: .env 파일 생성**
```
OPENAI_API_KEY=your-openai-api-key
```

**방법 3: 환경변수로 설정**
```bash
export OPENAI_API_KEY='your-openai-api-key'
```

## 사용법

### 웹 인터페이스 (추천)

```bash
python run.py
```

또는 직접:

```bash
python app.py
```

브라우저에서 `http://localhost:5000`으로 접속

### 커맨드라인 인터페이스

```bash
python main.py
```

### 입력 항목

| 항목 | 필수여부 | 설명 |
|------|----------|------|
| 등장인물 | 선택사항 | 이름, 역할 등 간단히 입력 |
| 필수 키워드 및 주제 | 선택사항 | 꼭 들어가야 하는 키워드나 주제 |
| 줄거리 | **필수** | 인스타툰을 만들기 위한 줄거리 |
| 분량 | **필수** | 1-10페이지 (권장: 4-8페이지) |

### 출력 형식

```json
{
  "wholeTitle": "전체 제목",
  "storyTopic": "핵심 주제·메시지",
  "hashtags": ["#해시태그1", "#해시태그2", ...],
  "pages": [
    {
      "page": 1,
      "character": ["캐릭터1", "캐릭터2"],
      "background": "배경 설명",
      "dialogue": {
        "캐릭터1": "대사1",
        "캐릭터2": "대사2"
      },
      "expressionPose": "표정/포즈 설명"
    }
  ]
}
```

## 파일 구조

```
instatoon/
├── run.py               # 통합 실행 스크립트
├── app.py               # Flask 웹 애플리케이션
├── main.py              # CLI 실행 파일
├── gpt_client.py        # GPT-4.1 API 클라이언트
├── config.py            # 설정 관리
├── requirements.txt     # 프로젝트 요구사항
├── templates/           # HTML 템플릿
│   └── index.html      # 메인 웹 페이지
├── static/             # 정적 파일
│   ├── style.css       # CSS 스타일
│   └── script.js       # JavaScript
└── README.md           # 사용 설명서
```

## 특징

- **GPT-4.1 모델 사용**: 최신 GPT 모델로 고품질 스토리보드 생성
- **웹 인터페이스**: 직관적이고 아름다운 웹 UI 제공
- **인스타그램 최적화**: 1:1 비율과 세이프 존을 고려한 레이아웃
- **구조화된 출력**: JSON 형식으로 체계적인 데이터 구조
- **반응형 디자인**: 모바일과 데스크톱 모두 지원
- **실시간 검증**: 입력값 실시간 검증 및 오류 처리
- **다중 실행 모드**: 웹 UI와 CLI 모드 선택 가능

## 주의사항

- OpenAI API 키가 필요합니다
- 인터넷 연결이 필요합니다
- API 사용량에 따른 비용이 발생할 수 있습니다

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
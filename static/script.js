// 인스타툰 스토리보드 생성기 JavaScript

class StoryboardGenerator {
    constructor() {
        this.form = document.getElementById('storyboard-form');
        this.generateBtn = document.getElementById('generate-btn');
        this.resultSection = document.getElementById('result-section');
        this.errorMessage = document.getElementById('error-message');
        
        this.initEventListeners();
    }

    initEventListeners() {
        // 폼 제출 이벤트
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // 다운로드 버튼
        document.getElementById('download-btn').addEventListener('click', () => this.downloadDOCX());
        
        // 복사 버튼
        document.getElementById('copy-btn').addEventListener('click', () => this.copyText());
        
        // 새 스토리 버튼
        document.getElementById('new-story-btn').addEventListener('click', () => this.newStory());
        
        // 입력 필드 실시간 검증
        document.getElementById('plot').addEventListener('input', () => this.validateForm());
        document.getElementById('pages').addEventListener('change', () => this.validateForm());
    }

    validateForm() {
        const plot = document.getElementById('plot').value.trim();
        const pages = document.getElementById('pages').value;
        
        const isValid = plot.length > 0 && pages !== '';
        this.generateBtn.disabled = !isValid;
        
        return isValid;
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            this.showError('필수 항목을 모두 입력해주세요.');
            return;
        }

        // 로딩 상태 시작
        this.setLoading(true);
        this.hideError();
        this.hideResult();

        try {
            // 폼 데이터 수집
            const formData = new FormData(this.form);
            const data = {
                characters: formData.get('characters') || '',
                keywords: formData.get('keywords') || '',
                plot: formData.get('plot') || '',
                pages: formData.get('pages') || ''
            };

            // API 호출
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.displayResult(result.storyboard);
                this.currentFilename = result.filename;
                this.currentStoryboard = result.storyboard;
                this.currentTextContent = result.text_content;
            } else {
                throw new Error(result.error || '스토리보드 생성에 실패했습니다.');
            }

        } catch (error) {
            console.error('Error:', error);
            this.showError(error.message || '네트워크 오류가 발생했습니다.');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(isLoading) {
        const btnText = this.generateBtn.querySelector('.btn-text');
        const spinner = this.generateBtn.querySelector('.loading-spinner');
        
        if (isLoading) {
            btnText.textContent = '생성 중...';
            spinner.style.display = 'block';
            this.generateBtn.disabled = true;
        } else {
            btnText.textContent = '스토리보드 생성하기';
            spinner.style.display = 'none';
            this.generateBtn.disabled = false;
        }
    }

    displayResult(storyboard) {
        // 제목과 주제 표시
        document.getElementById('story-title').textContent = storyboard.wholeTitle;
        document.getElementById('story-topic').textContent = storyboard.storyTopic;
        
        // 해시태그 표시
        const hashtagsContainer = document.getElementById('hashtags');
        hashtagsContainer.innerHTML = '';
        storyboard.hashtags.forEach(tag => {
            const span = document.createElement('span');
            span.className = 'hashtag';
            span.textContent = tag;
            hashtagsContainer.appendChild(span);
        });

        // 페이지들 표시
        const pagesContainer = document.getElementById('pages-container');
        pagesContainer.innerHTML = '';
        
        storyboard.pages.forEach(page => {
            const pageCard = this.createPageCard(page);
            pagesContainer.appendChild(pageCard);
        });

        // 결과 섹션 표시
        this.showResult();
    }

    createPageCard(page) {
        const card = document.createElement('div');
        card.className = 'page-card';
        
        card.innerHTML = `
            <div class="page-number">페이지 ${page.page}</div>
            <div class="page-content">
                <div class="content-section">
                    <div class="content-label">등장인물</div>
                    <div class="characters">
                        ${page.character.map(char => `<span class="character-tag">${char}</span>`).join('')}
                    </div>
                </div>
                
                <div class="content-section">
                    <div class="content-label">배경</div>
                    <div class="content-value">${page.background}</div>
                </div>
                
                <div class="content-section">
                    <div class="content-label">대사</div>
                    <div class="dialogue">
                        ${Object.entries(page.dialogue).map(([char, line]) => 
                            `<div class="dialogue-item"><strong>${char}:</strong> "${line}"</div>`
                        ).join('')}
                    </div>
                </div>
                
                <div class="content-section">
                    <div class="content-label">표정/포즈</div>
                    <div class="content-value">${page.expressionPose}</div>
                </div>
            </div>
        `;
        
        return card;
    }

    async downloadDOCX() {
        if (!this.currentStoryboard) {
            this.showError('다운로드할 스토리보드가 없습니다.');
            return;
        }

        try {
            const response = await fetch('/api/download-docx', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    storyboard: this.currentStoryboard
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                // 파일명 생성
                const timestamp = new Date().toISOString().replace(/[:.-]/g, '').slice(0, 14);
                a.download = `storyboard_${timestamp}.docx`;
                
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // 다운로드 성공 표시
                const downloadBtn = document.getElementById('download-btn');
                const originalText = downloadBtn.textContent;
                downloadBtn.textContent = '다운로드 완료!';
                downloadBtn.style.background = '#10b981';
                
                setTimeout(() => {
                    downloadBtn.textContent = originalText;
                    downloadBtn.style.background = '';
                }, 2000);
                
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'DOCX 파일 다운로드 실패');
            }
        } catch (error) {
            console.error('DOCX 다운로드 오류:', error);
            this.showError(`다운로드 중 오류가 발생했습니다: ${error.message}`);
        }
    }

    async copyText() {
        if (!this.currentTextContent) {
            this.showError('복사할 텍스트가 없습니다.');
            return;
        }

        try {
            await navigator.clipboard.writeText(this.currentTextContent);
            
            // 복사 성공 표시
            const copyBtn = document.getElementById('copy-btn');
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '복사됨!';
            copyBtn.style.background = '#10b981';
            
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.background = '';
            }, 2000);
            
        } catch (error) {
            // 폴백: 텍스트 영역을 사용한 복사
            try {
                const textarea = document.createElement('textarea');
                textarea.value = this.currentTextContent;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                
                // 성공 표시
                const copyBtn = document.getElementById('copy-btn');
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '복사됨!';
                copyBtn.style.background = '#10b981';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = '';
                }, 2000);
                
            } catch (fallbackError) {
                console.error('텍스트 복사 실패:', fallbackError);
                this.showError('텍스트 복사에 실패했습니다.');
            }
        }
    }

    newStory() {
        // 폼 초기화
        this.form.reset();
        
        // 결과 숨기기
        this.hideResult();
        this.hideError();
        
        // 저장된 데이터 초기화
        this.currentStoryboard = null;
        this.currentTextContent = null;
        this.currentFilename = null;
        
        // 폼 검증 초기화
        this.validateForm();
        
        // 첫 번째 입력 필드에 포커스
        document.getElementById('characters').focus();
    }

    showResult() {
        // Empty state 숨기기
        const emptyState = document.getElementById('empty-state');
        if (emptyState) {
            emptyState.style.display = 'none';
        }
        
        // Result section 표시
        this.resultSection.style.display = 'flex';
    }

    hideResult() {
        // Result section 숨기기
        this.resultSection.style.display = 'none';
        
        // Empty state 표시
        const emptyState = document.getElementById('empty-state');
        if (emptyState) {
            emptyState.style.display = 'flex';
        }
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.style.display = 'block';
        this.errorMessage.scrollIntoView({ behavior: 'smooth' });
    }

    hideError() {
        this.errorMessage.style.display = 'none';
    }
}

// 애플리케이션 초기화
document.addEventListener('DOMContentLoaded', () => {
    new StoryboardGenerator();
});

// 서비스 워커 등록 (PWA 지원)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
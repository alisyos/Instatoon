#!/usr/bin/env python3
"""
인스타툰 스토리보드 생성기 실행 스크립트
웹 서버와 CLI 모드를 선택할 수 있습니다.
"""

import sys
import os
from app import app
from main import InstaToonGenerator


def run_web_server():
    """웹 서버 모드로 실행"""
    print("🌐 웹 서버 모드로 실행합니다...")
    print("📍 브라우저에서 http://localhost:5000 으로 접속하세요")
    print("⏹️  종료하려면 Ctrl+C를 누르세요\n")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 서버가 종료되었습니다.")


def run_cli_mode():
    """CLI 모드로 실행"""
    print("💻 CLI 모드로 실행합니다...\n")
    generator = InstaToonGenerator()
    generator.run()


def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("📖 인스타툰 스토리보드 생성기")
    print("=" * 50)
    print()
    print("실행 모드를 선택하세요:")
    print("1. 웹 인터페이스 (추천)")
    print("2. 커맨드라인 인터페이스")
    print("3. 종료")
    print()
    
    while True:
        try:
            choice = input("선택 (1-3): ").strip()
            
            if choice == '1':
                run_web_server()
                break
            elif choice == '2':
                run_cli_mode()
                break
            elif choice == '3':
                print("👋 프로그램을 종료합니다.")
                break
            else:
                print("❌ 올바른 번호를 입력해주세요 (1-3)")
                
        except KeyboardInterrupt:
            print("\n👋 프로그램이 중단되었습니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
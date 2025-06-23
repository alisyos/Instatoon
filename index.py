from app import app

# Vercel 배포를 위한 진입점
# Vercel의 Python 런타임이 인식할 수 있도록 app을 export
handler = app
application = app

if __name__ == "__main__":
    app.run(debug=True) 
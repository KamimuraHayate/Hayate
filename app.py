# app.py
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dockerized Flask App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
                color: #333;
                text-align: center;
            }
            .container {
                background-color: #fff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #007bff;
            }
            p {
                font-size: 1.1em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello from Dockerized Flask!</h1>
            <p>このWebアプリはDockerコンテナ内で動作しています。</p>
            <p>ポート番号は <strong>8000</strong> です。</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask
from threading import Thread
import json

app = Flask('')

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Card Scraper Bot</title>
            <style>
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    padding: 40px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }
                h1 { font-size: 3em; margin-bottom: 10px; }
                .status { font-size: 1.5em; color: #4ade80; }
                .cards { font-size: 1.2em; margin-top: 20px; }
                .emoji { font-size: 2em; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="emoji">💳</div>
                <h1>Card Scraper Bot</h1>
                <div class="status">🟢 Bot is Running</div>
                <div class="cards">
                    Visa | Mastercard | Amex | Discover
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/status')
def status():
    return json.dumps({
        'status': 'active',
        'message': 'Scraping Visa, Mastercard, Amex, and Discover cards',
        'version': '2.0'
    })

def run():
    app.run(host='0.0.0.0', port=8080)

def live():
    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    live()

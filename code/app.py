from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
        <html>
            <head>
                <title>Hello</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f0f0f0;
                    }
                    h1 {
                        color: #3498db;
                        font-size: 4em;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <h1>Hello From D!nesh</h1>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


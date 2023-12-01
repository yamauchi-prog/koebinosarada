from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import datetime
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import pendulum

# firebaseへの接続準備
cred = credentials.Certificate('./hacku-adminsdk.json')
firebase_app = firebase_admin.initialize_app(cred) 
db = firestore.client()

# Flaskの初期化
app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# 直接HTMLを返す
@app.route("/")
def home():
        return render_template('question.html')

    # return send_file("templates/question.html")

# 質問を受け付けるルーティング
@app.route('/answer', methods=['POST', 'OPTIONS'])
def submitQuestion():
    if request.method == 'POST':
        try:
            request_data = request.json
            faculty = request_data.get('faculty')
            question_sentence = request_data.get('question_sentence')

            print(f"Received data - Faculty: {faculty}, Question: {question_sentence}")

            ref = db.collection('answer_log')
            new_doc = ref.document()
            x = datetime.datetime.now(pendulum.timezone('Asia/Tokyo'))
            print(x)
            new_doc.set({
                'id': new_doc.id,
                'faculty': faculty,
                'question': question_sentence,
                'date': x,
                'like': 0
            })

        # フロントエンドへ結果を渡す
            return jsonify({'answer': '質問が受け付けられました。'})

        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port='5001')

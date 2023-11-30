# モジュールのインポート
import datetime
from flask import Flask, request, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# firebaseへの接続準備
cred = credentials.Certificate('./hacku-adminsdk.json')
firebase_app = firebase_admin.initialize_app(cred) 
db = firestore.client()

# Flaskの初期化
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ホームページ
@app.route("/")
def home():
    return render_template('question.html')

# 有名人からの回答を得るルーティング
@app.route('/answer', methods=['POST'])
def getAnswer():
    if request.method == 'POST':
        # リクエスト情報の取得
        faculty = request.form.get('faculty')
        question_sentence = request.form.get('question_sentence')

        # 得られたデータをFirestoreへ保存
        ref = db.collection('answer_log')
        new_doc = ref.document()
        new_doc.set({
            'id': new_doc.id,
            'faculty': faculty,
            'question': question_sentence,
            'date': datetime.datetime.today(),
            'like': 0
        })

        # フロントエンドへ結果を渡す
        return jsonify({'answer': '質問が受け付けられました。'})

# Flaskサーバーを起動する
if __name__ == '__main__':
    app.run(debug=True, port=5001)

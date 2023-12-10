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
app = Flask(__name__,static_folder='./static/icon')
CORS(app)
app.config['JSON_AS_ASCII'] = False

# ホームページ
@app.route("/")
def home():
        return render_template('question.html')

# お問い合わせ
@app.route("/inquiry", methods=['GET'])
def inquiry():
        return render_template('inquiry.html')

# 雑談
@app.route("/zatudan", methods=['GET'])
def zatudan():
        return render_template('zatudan.html')

# プロフィール
@app.route("/profile", methods=['GET'])
def profile():
        return render_template('profile.html')
@app.route('/iconimage')
def iconimage():
        return send_file('../static/icon/image1.png', mimetype='static/icon/image1.png')



# 質問を受けつけるルーティング
@app.route('/answer', methods=['POST', 'OPTIONS'])
def submitQuestion():
    if request.method == 'POST':
        try:
            request_data = request.json
            faculty = request_data.get('faculty')
            question_sentence = request_data.get('question_sentence')
            ref = db.collection('answer_log')
            new_doc = ref.document()
            new_doc.set({
                'id': new_doc.id,
                'faculty': faculty,
                'question': question_sentence,
                'date': datetime.datetime.now(pendulum.timezone('Asia/Tokyo')),
                'like': 0
            })

        # フロントエンドへ結果を渡す
            return jsonify({'answer': '質問が受け付けられました。'})

        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': 'Internal server error'}), 500

# 過去の回答を取得するルーティング
@app.route('/dblogpage', methods=['GET', 'POST'])
def dblogpage():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('answer_log')

    ref = ref.order_by('date', direction=firestore.Query.DESCENDING)
    


    # if request.method == 'POST':
    #     request_data = request.json
    #     print(request.json)
    #     faculty_r = request_data.get('faculty_r')
    #     print(faculty_r)
    #     ref = ref.where('faculty', '==', faculty_r)
    #     print('データを受信しました')

    docs = ref.stream()
    # Firestoreからデータを取得
    answer_log_data_list = []
    for doc in docs:
        # 取得したデータをpythonで取り扱えるように変換
        doc_dict = doc.to_dict()

        # 取得したデータの改行コードをHTMLの改行に変換
        question = doc_dict['question'].replace('\n', '<br>')
        
        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'question': question,
            'date': doc_dict['date'].strftime('%Y/%m/%d %H:%M:%S'),
            'like': doc_dict['like']
        }
        answer_log_data_list.append(append_data)
        print(answer_log_data_list)

    # テンプレートに取得データのJsonリストを渡す
    return render_template(
        'question_dblog.html',
        answer_log_data_list=answer_log_data_list
    )

# 過去の回答を取得するルーティング(NEW)
@app.route('/dbselect', methods=['POST', 'OPTIONS'])
def dbselect():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('answer_log')

    ref = ref.order_by('date', direction=firestore.Query.DESCENDING)
    


    if request.method == 'POST':
        request_data = request.json
        print(request.json)
        faculty_r = request_data.get('faculty_r')
        print(faculty_r)
        ref = ref.where('faculty', '==', faculty_r)
        print('データを受信しました')

    docs = ref.stream()
    # Firestoreからデータを取得
    answer_log_data_list = []
    for doc in docs:
        # 取得したデータをpythonで取り扱えるように変換
        doc_dict = doc.to_dict()

        # 取得したデータの改行コードをHTMLの改行に変換
        question = doc_dict['question'].replace('\n', '<br>')
        
        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'question': question,
            'date': doc_dict['date'].strftime('%Y/%m/%d %H:%M:%S'),
            'like': doc_dict['like']
        }
        answer_log_data_list.append(append_data)
    print(answer_log_data_list)
    # テンプレートに取得データのJsonリストを渡す
    return render_template(
        'question_dblog.html',
        answer_log_data_list=answer_log_data_list
    )



# 回答を受けつけるルーティング
@app.route('/response', methods=['POST', 'OPTIONS'])
def submitAnswer():
    if request.method == 'POST':
        try:
            request_data = request.json
            faculty = request_data.get('faculty')
            answer_sentence = request_data.get('answer_sentence')
            ref = db.collection('response_log')
            new_doc = ref.document()
            new_doc.set({
                'id': new_doc.id,
                'faculty': faculty,
                'answer': answer_sentence,
                'date': datetime.datetime.now(pendulum.timezone('Asia/Tokyo')),
                'like': 0
            })

        # フロントエンドへ結果を渡す
            return jsonify({'response': '質問が受け付けられました。'})

        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': 'Internal server error'}), 500


# 過去の返信を取得するルーティング
@app.route('/answerpage', methods=['GET', 'POST'])
def answerpage():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('response_log')

    ref = ref.order_by('date', direction=firestore.Query.DESCENDING)
    


    # if request.method == 'POST':
    #     request_data = request.json
    #     print(request.json)
    #     faculty_r = request_data.get('faculty_r')
    #     print(faculty_r)
    #     ref = ref.where('faculty', '==', faculty_r)
    #     print('データを受信しました')

    docs = ref.stream()
    # Firestoreからデータを取得
    response_log_data_list = []
    for doc in docs:
        # 取得したデータをpythonで取り扱えるように変換
        doc_dict = doc.to_dict()

        # 取得したデータの改行コードをHTMLの改行に変換
        answer = doc_dict['answer'].replace('\n', '<br>')
        
        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'answer': answer,
            'date': doc_dict['date'].strftime('%Y/%m/%d %H:%M:%S'),
            'like': doc_dict['like']
        }
        response_log_data_list.append(append_data)
        print(response_log_data_list)

    # テンプレートに取得データのJsonリストを渡す
    return render_template(
        'question_answer.html',
        response_log_data_list=response_log_data_list
    )

# 過去の返信を取得するルーティング(NEW)
@app.route('/anchoice', methods=['POST', 'OPTIONS'])
def choice():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('response_log')

    ref = ref.order_by('date', direction=firestore.Query.DESCENDING)
    


    if request.method == 'POST':
        request_data = request.json
        print(request.json)
        faculty_r = request_data.get('faculty_r')
        print(faculty_r)
        ref = ref.where('faculty', '==', faculty_r)
        print('データを受信しました')

    docs = ref.stream()
    # Firestoreからデータを取得
    response_log_data_list = []
    for doc in docs:
        # 取得したデータをpythonで取り扱えるように変換
        doc_dict = doc.to_dict()

        # 取得したデータの改行コードをHTMLの改行に変換
        response = doc_dict['response'].replace('\n', '<br>')
        
        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'response': response,
            'date': doc_dict['date'].strftime('%Y/%m/%d %H:%M:%S'),
            'like': doc_dict['like']
        }
        response_log_data_list.append(append_data)
    print(response_log_data_list)
    # テンプレートに取得データのJsonリストを渡す
    return render_template(
        'question_answer.html',
        response_log_data_list=response_log_data_list
    )

#Flask起動
if __name__ == '__main__':
    app.run(debug=True, port='5001')

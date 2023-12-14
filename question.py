from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import datetime
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import pendulum
import pytz


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

# 返信
@app.route("/response", methods=['GET'])
def response():
        return render_template('question_answer.html')



# 質問を受けつけるルーティング
@app.route('/answer', methods=['POST', 'OPTIONS'])
def submitQuestion():
    if request.method == 'POST':
        try:
            request_data = request.json
            faculty = request_data.get('faculty')
            question_sentence = request_data.get('question_sentence')
            ref = db.collection('answer_log')#question_logに変更する
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

# 過去の質問を取得するルーティング
@app.route('/dblogpage', methods=['GET', 'POST'])
def dblogpage():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('answer_log')#question_logに変更する

    ref = ref.order_by('date', direction=firestore.Query.DESCENDING)
    
    docs = ref.stream()
    # Firestoreからデータを取得
    answer_log_data_list = []
    for doc in docs:
        # 取得したデータをpythonで取り扱えるように変換
        doc_dict = doc.to_dict()

        # 取得したデータの改行コードをHTMLの改行に変換
        question = doc_dict['question'].replace('\n', '<br>')
        
        # 日本時間に変換
        date_jp = doc_dict['date'].astimezone(pytz.timezone('Asia/Tokyo'))
        formatted_date = date_jp.strftime('%Y/%m/%d %H:%M:%S')


        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'question': question,
            'date': formatted_date,
            'like': doc_dict['like']
        }
        answer_log_data_list.append(append_data)
        print(answer_log_data_list)
        

    # テンプレートに取得データのJsonリストを渡す
    return render_template(
        'question_dblog.html',
        answer_log_data_list=answer_log_data_list
    )

# 過去の質問を選別して取得するルーティング(NEW)
@app.route('/dbselect', methods=['POST', 'OPTIONS'])
def dbselect():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('answer_log')#question_logに変更する

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

            # 日本時間に変換
        date_jp = doc_dict['date'].astimezone(pytz.timezone('Asia/Tokyo'))
        formatted_date = date_jp.strftime('%Y/%m/%d %H:%M:%S')
    
        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'question': question,
            'date': formatted_date,
            'like': doc_dict['like']
        }
        answer_log_data_list.append(append_data)
    print(answer_log_data_list)
    # テンプレートに取得データのJsonリストを渡す
    return jsonify(answer_log_data_list)

# 雑談を受けつけるルーティング
@app.route('/zatudan', methods=['POST', 'OPTIONS'])
def submitZatudan():
    if request.method == 'POST':
        try:
            request_data = request.json
            faculty = request_data.get('faculty')
            question_sentence = request_data.get('question_sentence')
            ref = db.collection('zatudan_log')
            new_doc = ref.document()
            new_doc.set({
                'id': new_doc.id,
                'faculty': faculty,
                'question': question_sentence,
                'date': datetime.datetime.now(pendulum.timezone('Asia/Tokyo')),
                'like': 0
            })

        # フロントエンドへ結果を渡す
            return jsonify({'answer': '雑談が受け付けられました。'})

        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': 'Internal server error'}), 500


# 過去の雑談を取得するルーティング
@app.route('/zdlogpage', methods=['GET', 'POST'])
def zdlogpage():
    db = firestore.client()

    # Firestoreから並び替えたデータを取得する準備
    ref = db.collection('zatudan_log')

    ref = ref.order_by('date', direction=firestore.Query.DESCENDING)
    
    docs = ref.stream()
    # Firestoreからデータを取得
    zatudan_log_data_list = []
    for doc in docs:
        # 取得したデータをpythonで取り扱えるように変換
        doc_dict = doc.to_dict()

        # 取得したデータの改行コードをHTMLの改行に変換
        question = doc_dict['question'].replace('\n', '<br>')
        
        # 日本時間に変換
        date_jp = doc_dict['date'].astimezone(pytz.timezone('Asia/Tokyo'))
        formatted_date = date_jp.strftime('%Y/%m/%d %H:%M:%S')

        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'question': question,
            'date': formatted_date,
            'like': doc_dict['like']
        }
        zatudan_log_data_list.append(append_data)
        print(zatudan_log_data_list)

    # テンプレートに取得データのJsonリストを渡す
    return render_template(
        'zatudan_dblog.html',
        zatudan_log_data_list=zatudan_log_data_list
    )


#★★★↓追加↓★★★（山内が見たらこのコメントは消して良し）
# 「いいね」をカウントアップするルーティング
@app.route('/postlike', methods=['POST'])
def postlike():
    # 「いいね」の対象となる質問のIDを取得
    promptJson = request.json
    answer_log_id = promptJson['id']

    # 質問IDに一致する質問をFirestoreから取得
    ref = db.collection('answer_log')#question_logに変更する
    docs = ref.where('id', '==', answer_log_id).stream()
    
    # 更新前のデータを取得する。（forだが1回しか処理が実行されない）
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_like = doc_dict['like']

    # 取得した回答の「いいね」をカウントアップ
    ref.document(answer_log_id).update({'like': doc_like+1})

    # カウントアップ後の「いいね」の値をフロントエンドに渡す
    return {'result':doc_like+1}



# ↓　山内変更　↓
# 回答を受けつけるルーティング
@app.route('/response', methods=['POST', 'OPTIONS'])
def submitAnswer():
    if request.method == 'POST':
        try:
            request_data = request.json
            faculty = request_data.get('faculty')
            answer_sentence = request_data.get('answer_sentence')
            response_sentence = request_data.get('response_sentence')
            ref = db.collection('response_log')
            new_doc = ref.document()
            new_doc.set({#どのidの質問に答えたかも記録する
                'id': new_doc.id,
                'faculty': faculty,
                'answer': answer_sentence,
                'response':response_sentence,
                'date': datetime.datetime.now(pendulum.timezone('Asia/Tokyo')),
            })

        # フロントエンドへ結果を渡す
            return jsonify({'response': '質問が受け付けられました。'})

        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    # 「いいね（返信）」の対象となる質問のIDを取得
    promptJson = request.json
    answer_log_id = promptJson['id']

    # 質問IDに一致する質問をFirestoreから取得
    ref = db.collection('response_log')#question_logに変更する
    docs = ref.where('id', '==', answer_log_id).stream()
    
    # 更新前のデータを取得する。（forだが1回しか処理が実行されない）
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_question = doc_question['question']


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
        response = doc_dict['response'].replace('\n', '<br>')
        
        # 日本時間に変換
        date_jp = doc_dict['date'].astimezone(pytz.timezone('Asia/Tokyo'))
        formatted_date = date_jp.strftime('%Y/%m/%d %H:%M:%S')

        # 取得してきたデータをJsonのリストに変換
        append_data = {#どのidの質問に答えたかも記録する
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'answer': answer,
            'response':response,
            'date': formatted_date,
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
        
        # 日本時間に変換
        date_jp = doc_dict['date'].astimezone(pytz.timezone('Asia/Tokyo'))
        formatted_date = date_jp.strftime('%Y/%m/%d %H:%M:%S')

        # 取得してきたデータをJsonのリストに変換
        append_data = {
            'id': doc_dict['id'],
            'faculty': doc_dict['faculty'],
            'response': response,
            'date': formatted_date,
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

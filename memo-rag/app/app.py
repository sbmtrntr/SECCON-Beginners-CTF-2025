import os
import uuid
import json
import logging
import sys
from flask import Flask, request, redirect, render_template, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql
from openai import OpenAI

openai_client = OpenAI()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET")

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="redis://redis:6379",
)

# DB接続
def get_db():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset='utf8mb4',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

def query_db(sql, args=(), fetchone=False):
    con = get_db()
    with con.cursor() as cur:
        cur.execute(sql, args)
        result = cur.fetchone() if fetchone else cur.fetchall()
    con.close()
    return result

def execute_db(sql, args=()):
    con = get_db()
    with con.cursor() as cur:
        cur.execute(sql, args)
    con.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(f"/users/{session['user_id']}")
    return redirect(url_for('login'))

# ユーザー登録
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # username の重複をチェック
        existing = query_db("SELECT 1 FROM users WHERE username=%s", (username,), fetchone=True)
        if existing:
            return 'このユーザー名は既に使われています。', 409
        user_id = str(uuid.uuid4())
        execute_db("INSERT INTO users (id, username, password) VALUES (%s, %s, %s)", (user_id, username, password))
        session['user_id'] = user_id
        return redirect(f"/users/{user_id}")
    return render_template('register.html')

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db("SELECT * FROM users WHERE username=%s AND password=%s", (username, password), fetchone=True)
        if user:
            session['user_id'] = user['id']
            return redirect(f"/users/{user['id']}")
        return 'ユーザー名またはパスワードが間違っています。', 403
    return render_template('login.html')

# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ユーザーページ（自分のメモは非公開も表示、他人のメモは公開のみ）
@app.route('/users/<uid>')
def user_page(uid):
    current = session.get('user_id')
    if current == uid:
        sql = """
            SELECT id, body, visibility FROM memos WHERE user_id=%s AND visibility IN ('public','private')
            UNION 
            SELECT id, '🔒秘密メモ' AS body, 'secret' AS visibility FROM memos WHERE user_id=%s AND visibility='secret'
        """
        memos = query_db(sql, (uid, uid))
    else:
        memos = query_db("SELECT id, body, visibility FROM memos WHERE user_id=%s AND visibility='public'", (uid,))
    return render_template('index.html', memos=memos)

# メモの詳細表示（secret の場合はパスワードを要求）
@app.route('/memo/<mid>', methods=['GET', 'POST'])
def memo_detail(mid):
    uid = session.get('user_id')
    memo = query_db('SELECT * FROM memos WHERE id=%s', (mid,), fetchone=True)
    if not memo:
        return 'Not found', 404
    if memo['user_id'] != uid:
        return 'Forbidden', 403
    if memo['visibility'] == 'secret':
        if request.method == 'POST' and request.form.get('password') == memo.get('password'):
            return render_template('detail.html', memo=memo, authorized=True)
        return render_template('detail.html', memo=memo, authorized=False) if request.method == 'GET' else ('Wrong password', 403)
    return render_template('detail.html', memo=memo, authorized=True)

# メモの作成
@app.route('/memo/create', methods=['GET', 'POST'])
def memo_create():
    uid = session.get('user_id')
    if not uid:
        return redirect('/')
    if request.method == 'POST':
        memo_count = query_db("SELECT COUNT(*) AS count FROM memos WHERE user_id=%s", (uid,), fetchone=True)['count']
        if memo_count >= 3:
            return "メモは3つまでしか作成できません。", 403

        body = request.form.get('body', '')
        if len(body) > 100:
            return "メモは100文字以下で入力してください。", 400

        visibility = request.form.get('visibility', 'public')
        password = request.form.get('password', '') if visibility == 'secret' else None
        mid = str(uuid.uuid4())
        execute_db(
            'INSERT INTO memos (id,user_id,body,visibility,password) VALUES (%s,%s,%s,%s,%s)',
            (mid, uid, body, visibility, password)
        )
        return redirect(f'/memo/{mid}')
    return render_template('create.html')

# 指定ユーザーのメモをキーワードで検索
def search_memos(keyword: str, include_secret: bool, user_id: str) -> list:
    visibilities = ("public","private","secret") if include_secret else ("public","private")
    placeholders = ','.join(['%s'] * len(visibilities))
    sql = f"SELECT id, body FROM memos WHERE user_id=%s AND visibility IN ({placeholders})"
    rows = query_db(sql, (user_id, *visibilities))
    return [r for r in rows if keyword.lower() in r['body'].lower()]

# 指定キーワードを含むメモの投稿者を取得
def get_author_by_body(keyword: str) -> list:
    row = query_db("SELECT user_id FROM memos WHERE body LIKE %s ORDER BY created_at ASC LIMIT 1", (f"%{keyword}%",), fetchone=True)
    return [{'user_id': row['user_id']}] if row else []

# RAG機能：検索や投稿者取得をfunction callingで実施
def rag(query: str, user_id: str) -> list:
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'search_memos',
                'description': 'Search for memos by keyword and visibility settings.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'keyword': {'type': 'string'},
                        'include_secret': {'type': 'boolean'},
                        'target_uid': {'type': 'string'}
                    },
                    'required': ['keyword', 'include_secret', 'target_uid'],
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'get_author_by_body',
                'description': 'Find the user who wrote a memo containing a given keyword.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'keyword': {'type': 'string'}
                    },
                    'required': ['keyword']
                }
            }
        }
    ]
    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are an assistant that helps search user memos using the available tools.'},
            {'role': 'assistant', 'content': 'Target User ID: ' + user_id},
            {'role': 'user', 'content': query}
        ],
        tools=tools,
        tool_choice='required',
        max_tokens=100,
    )
    choice = response.choices[0]
    if choice.message.tool_calls:
        call = choice.message.tool_calls[0]
        name = call.function.name
        args = json.loads(call.function.arguments)
        if name == 'search_memos':
            return search_memos(args.get('keyword', ''), args.get('include_secret', False), args.get('target_uid', ''))
        elif name == 'get_author_by_body':
            return get_author_by_body(args['keyword'])
    return []

# メモを文脈にして質問に答える
def answer_with_context(query: str, memos: list) -> str:
    context_text = "\n---\n".join([m['body'] for m in memos])
    prompt = f"""Here are your memos. Answer the following question based on them:

{context_text}

Question: {query}
"""
    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are an assistant that answers questions using the user\'s memos as context.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=100,
    )
    content = response.choices[0].message.content.strip()
    return content

# RAGによるメモ検索
@app.route('/memo/search', methods=['GET'])
def search_form():
    uid = session.get('user_id')
    if not uid:
        return redirect('/')
    return render_template('search.html', answer=None, query='')

@app.route('/memo/search', methods=['POST'])
@limiter.limit("5 per minute")
def search():
    uid = session.get('user_id')
    if not uid:
        return redirect('/')
    query = request.form.get('query', '')
    memos = rag(query, uid)
    if not (memos and isinstance(memos, list)):
        answer = "関連するメモが見つかりませんでした。"
    else:
        if 'user_id' in memos[0]:
            answer = f"User ID: {memos[0]['user_id']}"
        else:
            answer = answer_with_context(query, memos)
            # 回答にFLAGが含まれている場合は警告を表示
            if "ctf4b" in answer:
                answer = "FLAGのメモは取得できません。"
    return render_template('search.html', answer=answer, query=query)

# ログ出力の設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
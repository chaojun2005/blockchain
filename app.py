from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from main import BlockchainCertificator
from flask import send_file
import os
import datetime

app = Flask(__name__)

# 定義 datetimeformat 過濾器
@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

app.secret_key = os.urandom(24)


# 初始化區塊鏈
certificator = BlockchainCertificator()

# 主頁面路由
@app.route('/')
def index():
    # 分頁邏輯
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 每頁顯示 10 筆資料
    total = len(certificator.chain)
    start = (page - 1) * per_page
    end = start + per_page
    chain_paginated = certificator.chain[start:end]

    return render_template('index.html', chain=chain_paginated, page=page, total=total, per_page=per_page)

# 查詢證書頁面
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        student_id = request.form['student_id']
        result = [block for block in certificator.chain if block['student_id'] == student_id]
        if result:
            return render_template('search_result.html', result=result)
        else:
            flash('未找到相關證書')
            return redirect(url_for('search'))
    return render_template('search.html')

# API：獲取完整鏈條資料
@app.route('/api/get_chain', methods=['GET'])
def get_chain():
    return jsonify(certificator.chain)

# 提供下載 CSV 檔案的功能
@app.route('/download_csv')
def download_csv():
    csv_file_path = 'data.csv'  # 確認檔案路徑
    return send_file(csv_file_path, as_attachment=True, download_name='students.csv')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_id = request.form.get('student_id')  # 獲取用戶輸入的學號
        results = [block for block in certificator.chain if block['student_id'] == query_id]

        if not results:
            message = "未找到相關數據，請檢查學號是否正確！"
            return render_template('query.html', message=message)

        return render_template('query.html', results=results)

    # 初始加載查詢頁面
    return render_template('query.html')

# 啟動應用
if __name__ == '__main__':
    # 確保 Flask 專案結構完整
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')

    # 啟動伺服器
    app.run(debug=True, host='0.0.0.0', port=5000)

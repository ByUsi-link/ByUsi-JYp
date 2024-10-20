import os
import threading
import magic  # 导入 python-magic 库
from flask import Flask, request, send_file, render_template, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '加密管理面板密码的密钥'  # 用于加密 session 数据，设置一个随机字符串作为密钥

PASSWORD = "管理面板密码"  # 设置密码

def check_upload_folder():
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

def get_uploaded_files(search_query=None):
    uploads_dir = 'uploads'
    if os.path.exists(uploads_dir):
        files = os.listdir(uploads_dir)
        if search_query:
            # Filter files based on the search query (case-insensitive)
            files = [file for file in files if search_query.lower() in file.lower()]
        return files
    return []

def save_file(filename, file_data):
    check_upload_folder()
    with open(os.path.join('uploads', filename), 'wb') as f:
        f.write(file_data)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_data = uploaded_file.read()  # 将文件内容读取到内存
        thread = threading.Thread(target=save_file, args=(uploaded_file.filename, file_data))
        thread.start()
        return jsonify({'status': 'success', 'filename': uploaded_file.filename})
    return jsonify({'status': 'error'})

@app.route('/', methods=['GET'])
def upload_file():
    files = get_uploaded_files()
    return render_template('upload.html', files=files)

@app.route('/view/<filename>')
def view_file(filename):
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        mime_type = magic.from_file(file_path, mime=True)  # 使用 python-magic 获取 MIME 类型
        file_ext = os.path.splitext(filename)[1].lower()  # 获取文件扩展名
        
        # 根据扩展名做进一步的 MIME 类型调整
        if file_ext in ['.mp3', '.wav', '.aac', '.flac', '.m4a']:
            mime_type = 'audio/' + file_ext.lstrip('.')

        # 根据 MIME 类型渲染不同的模板
        if mime_type.startswith('image/'):
            return render_template('view_image.html', filename=filename)
        elif mime_type.startswith('video/'):
            return render_template('view_video.html', filename=filename)
        elif mime_type.startswith('audio/'):
            return render_template('view_audio.html', filename=filename)
        else:
            return render_template('download.html', filename=filename)
    return '找不到文件'

@app.route('/file/<filename>')
def download_file(filename):
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    return '找不到文件'

# 管理后台的路由，显示文件列表
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        if 'password' in request.form:
            # 用户提交的密码
            input_password = request.form['password']
            # 检查密码是否正确
            if input_password == PASSWORD:
                session['logged_in'] = True  # 密码正确，设置 session
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', error='密码错误')

        elif 'search' in request.form:
            search_query = request.form['search']
            files = get_uploaded_files(search_query)  # 使用搜索关键字过滤文件
            return render_template('admin_dashboard.html', files=files, search_query=search_query)

    # 检查用户是否已经登录
    if session.get('logged_in'):
        files = get_uploaded_files()  # 列出所有上传的文件
        return render_template('admin_dashboard.html', files=files)
    else:
        return render_template('admin_login.html')  # 未登录，显示登录页面

# 删除文件的路由
@app.route('/admin/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))  # 如果没有登录，重定向到登录页面
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('admin_dashboard'))  # 删除后重定向到管理后台
    return '找不到文件'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2266)
import os
import threading
import magic  # 导入 python-magic 库
import uuid  # 用于生成唯一文件 ID
import json  # 导入 json 模块
from flask import Flask, request, send_file, render_template, jsonify, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = '加密管理面板密码的密钥'  # 用于加密 session 数据，设置一个随机字符串作为密钥

PASSWORD = "管理面板密码"  # 设置密码
file_id_map = {}  # 用于存储文件名和文件 ID 的映射关系
WID_FILE = 'wid.json'  # 存储文件 ID 的文件
SCAN_INTERVAL = 10  # 扫描间隔（秒）

def check_upload_folder():
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

def load_file_id_map():
    """加载文件 ID 映射关系"""
    global file_id_map
    if os.path.exists(WID_FILE):
        with open(WID_FILE, 'r') as f:
            try:
                file_id_map = json.load(f)  # 使用 json.load() 读取并转换为字典
            except json.JSONDecodeError:
                file_id_map = {}  # 如果文件为空或无效 JSON，则初始化为空字典
    else:
        file_id_map = {}  # 如果文件不存在，初始化为空字典

def save_file_id_map():
    """保存文件 ID 映射关系"""
    with open(WID_FILE, 'w') as f:
        json.dump(file_id_map, f)  # 使用 json.dump() 保存字典为文件

def get_uploaded_files(search_query=None):
    uploads_dir = 'uploads'
    if os.path.exists(uploads_dir):
        files = os.listdir(uploads_dir)
        if search_query:
            # 根据搜索关键字过滤文件（不区分大小写）
            files = [file for file in files if search_query.lower() in file.lower()]
        return [{'filename': file, 'id': file_id_map.get(file, generate_file_id(file))} for file in files]
    return []

def generate_file_id(filename):
    """如果文件没有 ID，生成新的文件 ID 并更新映射关系"""
    if filename not in file_id_map:
        file_id = str(uuid.uuid4())
        file_id_map[filename] = file_id
        save_file_id_map()  # 保存映射关系到文件中
    return file_id_map[filename]

def save_file(filename, file_data):
    check_upload_folder()
    with open(os.path.join('uploads', filename), 'wb') as f:
        f.write(file_data)
    # 生成文件 ID，并保存到映射关系中
    generate_file_id(filename)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_data = uploaded_file.read()  # 将文件内容读取到内存
        thread = threading.Thread(target=save_file, args=(uploaded_file.filename, file_data))
        thread.start()
        file_id = generate_file_id(uploaded_file.filename)  # 获取或生成文件 ID
        return jsonify({'status': 'success', 'filename': uploaded_file.filename, 'id': file_id})
    return jsonify({'status': 'error'})

@app.route('/', methods=['GET'])
def upload_file():
    files = get_uploaded_files()
    return render_template('upload.html', files=files)

@app.route('/view/id/<file_id>')
def view_file_by_id(file_id):
    """根据文件 ID 预览文件"""
    filename = next((name for name, fid in file_id_map.items() if fid == file_id), None)
    if filename:
        return view_file(filename)
    return '找不到文件'

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

@app.route('/file/id/<file_id>')
def download_file_by_id(file_id):
    """根据文件 ID 下载文件"""
    filename = next((name for name, fid in file_id_map.items() if fid == file_id), None)
    if filename:
        return download_file(filename)
    return '找不到文件'

@app.route('/file/<filename>')
def download_file(filename):
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    return '找不到文件'

# API 功能

@app.route('/api/files', methods=['GET'])
def api_list_files():
    search_query = request.args.get('search', None)
    files = get_uploaded_files(search_query)
    return jsonify({'files': files})

@app.route('/api/delete/<filename>', methods=['DELETE'])
def api_delete_file(filename):
    auth_password = request.headers.get('Authorization')
    if auth_password == PASSWORD:  # 验证密码
        uploads_dir = 'uploads'
        file_path = os.path.join(uploads_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'status': 'success', 'message': '文件删除成功'})
        return jsonify({'status': 'error', 'message': '文件未找到'})
    return jsonify({'status': 'error', 'message': '未授权'}), 403

# 管理后台的路由，显示文件列表
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        if 'password' in request.form:
            input_password = request.form['password']
            if input_password == PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', error='密码错误')
        elif 'search' in request.form:
            search_query = request.form['search']
            files = get_uploaded_files(search_query)
            return render_template('admin_dashboard.html', files=files, search_query=search_query)
    if session.get('logged_in'):
        files = get_uploaded_files()
        return render_template('admin_dashboard.html', files=files)
    else:
        return render_template('admin_login.html')

@app.route('/admin/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('admin_dashboard'))
    return '找不到文件'

def scan_for_files():
    """定期扫描文件夹以更新文件 ID 映射"""
    while True:
        time.sleep(SCAN_INTERVAL)  # 等待指定的扫描间隔
        current_files = set(os.listdir('uploads'))
        existing_files = set(file_id_map.keys())
        
        # 查找需要生成 ID 的新文件
        for filename in current_files:
            if filename not in existing_files:
                generate_file_id(filename)  # 为新文件生成 ID
        
        # 可选：查找已删除的文件并移除其 ID
        for filename in list(existing_files):
            if filename not in current_files:
                file_id_map.pop(filename, None)  # 移除已删除文件的 ID
        
        save_file_id_map()  # 更新 ID 映射到文件

# 启动扫描线程
threading.Thread(target=scan_for_files, daemon=True).start()

# 启动应用时加载文件 ID 映射
load_file_id_map()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2266)
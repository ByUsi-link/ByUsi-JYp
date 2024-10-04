from flask import Flask, request, send_file, render_template_string, jsonify
import os
import mimetypes

app = Flask(__name__)

# 检查并创建上传目录
def check_upload_folder():
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

# 获取上传目录中的文件列表
def get_uploaded_files():
    uploads_dir = 'uploads'
    if os.path.exists(uploads_dir):
        files = os.listdir(uploads_dir)
        return files
    return []

# AJAX 文件上传处理
@app.route('/upload', methods=['POST'])
def upload():
    check_upload_folder()
    uploaded_file = request.files['file']
    if uploaded_file:
        uploaded_file.save(os.path.join('uploads', uploaded_file.filename))
        return jsonify({'status': 'success', 'filename': uploaded_file.filename})
    return jsonify({'status': 'error'})

# 上传文件的页面和显示文件列表
@app.route('/', methods=['GET'])
def upload_file():
    files = get_uploaded_files()  # 获取上传目录中的文件列表
    file_list = ''
    for file in files:
        file_list += f'<li><a href="/view/{file}">在线预览文件 - {file}</a></li>'
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>ByUsi-JYp - 简单云服务</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f6;
                color: #333;
                text-align: center;
                margin: 0;
                padding: 2%;
            }}
            h1 {{
                color: #007BFF;
                margin-top: 2em;
            }}
            form {{
                background-color: white;
                padding: 2%;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                display: inline-block;
                max-width: 80%;
                width: 100%;
                margin: 0 auto;
            }}
            input[type=file], input[type=submit] {{
                padding: 1em;
                margin: 1em 0;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}
            input[type=submit] {{
                background-color: #007BFF;
                color: white;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }}
            input[type=submit]:hover {{
                background-color: #0056b3;
            }}
            .file-list {{
                margin-top: 2em;
                text-align: left;
                max-width: 90%;
                margin: 2em auto;
            }}
            .file-list ul {{
                list-style-type: none;
                padding: 0;
            }}
            .file-list li {{
                background-color: #fff;
                margin: 1em 0;
                padding: 1.5em;
                border-radius: 8px;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
            }}
            .file-list li a {{
                text-decoration: none;
                color: #007BFF;
                font-weight: bold;
                display: block;
            }}
            .file-list li a:hover {{
                text-decoration: underline;
            }}
            .upload-status {{
                margin: 1em 0;
                color: #007BFF;
                font-weight: bold;
            }}
            footer {{
                margin-top: 3em;
                font-size: 0.9em;
                color: #aaa;
            }}
        </style>
        <script>
            function uploadFile() {{
                var fileInput = document.getElementById('fileInput');
                var uploadStatus = document.getElementById('uploadStatus');
                var formData = new FormData();
                formData.append('file', fileInput.files[0]);

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload', true);

                xhr.onloadstart = function() {{
                    uploadStatus.textContent = '正在上传...';
                }};

                xhr.onload = function () {{
                    uploadStatus.textContent = '';  // 清除状态信息
                    if (xhr.status === 200) {{
                        var response = JSON.parse(xhr.responseText);
                        if (response.status === 'success') {{
                            var fileList = document.getElementById('fileList');
                            var newFile = '<li><a href="/view/' + response.filename + '">在线预览文件 - ' + response.filename + '</a></li>';
                            fileList.innerHTML += newFile;
                        }} else {{
                            alert('上传失败，请重试');
                        }}
                    }}
                }};
                xhr.send(formData);
            }}
        </script>
    </head>
    <body>
        <h1>ByUsi-JYp - 简单云服务</h1>
        <form id="uploadForm" onsubmit="event.preventDefault(); uploadFile();">
            <input type="file" id="fileInput" name="file" required>
            <br>
            <input type="submit" value="上传文件">
        </form>
        <div class="upload-status" id="uploadStatus"></div>
        <div class="file-list">
            <h2>已上传文件</h2>
            <ul id="fileList">
                {file_list}
            </ul>
        </div>
        <footer>
            <p>ByUsi &copy; 2024</p>
        </footer>
    </body>
    </html>
    '''

# 根据文件类型选择不同的播放器
@app.route('/view/<filename>')
def view_file(filename):
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # 根据 MIME 类型返回不同的播放器
        if mime_type:
            if mime_type.startswith('image/'):
                return render_template_string(f'''
                <!doctype html>
                <html>
                <body style="text-align: center; margin: 2em;">
                    <h1>图片预览 - {filename}</h1>
                    <img src="/file/{filename}" alt="{filename}" style="max-width: 90%; height: auto;">
                </body>
                </html>
                ''')
            elif mime_type.startswith('video/'):
                return render_template_string(f'''
                <!doctype html>
                <html>
                <body style="text-align: center; margin: 2em;">
                    <h1>视频预览 - {filename}</h1>
                    <video controls style="max-width: 90%; height: auto;">
                        <source src="/file/{filename}" type="{mime_type}">
                        您的浏览器不支持视频播放。
                    </video>
                </body>
                </html>
                ''')
            elif mime_type.startswith('audio/'):
                return render_template_string(f'''
                <!doctype html>
                <html>
                <body style="text-align: center; margin: 2em;">
                    <h1>音频预览 - {filename}</h1>
                    <audio controls>
                        <source src="/file/{filename}" type="{mime_type}">
                        您的浏览器不支持音频播放。
                    </audio>
                </body>
                </html>
                ''')
            else:
                return render_template_string(f'''
                <!doctype html>
                <html>
                <body style="text-align: center; margin: 2em;">
                    <h1>下载文件 - {filename}</h1>
                    <a href="/file/{filename}" download style="font-size: 1.2em; color: #007BFF;">点击下载文件</a>
                </body>
                </html>
                ''')
        else:
            return '无法确定文件类型'
    return '找不到文件'

# 用于下载文件
@app.route('/file/<filename>')
def download_file(filename):
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    return '找不到文件'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2266)
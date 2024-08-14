from flask import Flask, request, send_file
import os

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

# 上传文件的页面和显示文件列表
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    check_upload_folder()  # 检查并创建上传目录

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            uploaded_file.save(os.path.join('uploads', uploaded_file.filename))
            return '<h1>文件上传成功！</h1> <a href="/view">查看上传文件去</a>'
    
    files = get_uploaded_files()  # 获取上传目录中的文件列表
    file_list = '<h1>已上传的文件列表：</h1><ul>'
    for file in files:
        file_list += f'<li><a href="/view/{file}">在线预览文件 - {file}</a></li>'
    file_list += '</ul>'
    
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>BySi-简单云</title>
        <link rel="shortcut icon" href="http://juyp.hucl.link/f/WjtZ/20231118_014550_0000.png" type="image/x-icon">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 50px;
                text-align: center;
            }}
            h1 {{
                color: #333;
            }}
            form {{
                margin-top: 30px;
            }}
            input[type=file], input[type=submit] {{
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            input[type=submit] {{
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
                margin: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            a {{
                text-decoration: none;
                color: #000;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>BySi-简单云</h1>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <br>
            <input type=submit value=上传吧>
        </form>
        {file_list}
    </body>
    </html>
    '''

# 预览上传的文件
@app.route('/view/<filename>')
def view_file(filename):
    uploads_dir = 'uploads'
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    return '找不到文件'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2266)
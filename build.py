import os
import PyInstaller.__main__

app_name = "flask_app"
output_dir = "dist"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

PyInstaller.__main__.run([
    '--name=%s' % app_name,
    '--onefile',
    '--distpath=%s' % output_dir,
    'ai_model.py'
])
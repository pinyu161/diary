# PythonAnywhere WSGI 設定檔
# 請將 YOUR_USERNAME 換成你的 PythonAnywhere 帳號名稱

import sys
import os

# ⚠️ 把下面這行的 YOUR_USERNAME 換成你的帳號！
project_home = '/home/YOUR_USERNAME/pudding_diary'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from app import app, init_db
init_db()          # 自動建立資料庫與資料表

application = app  # PythonAnywhere 要求變數名稱是 application

# 🐶 布丁狗日記 — 部署說明

## 本地執行（測試用）

```bash
pip install flask
python app.py
# 打開瀏覽器 → http://127.0.0.1:5000
```

---

## 部署到 PythonAnywhere（免費）

### 步驟一：註冊帳號
前往 https://www.pythonanywhere.com 註冊免費帳號

### 步驟二：上傳專案
1. 登入後點選上方的 **Files** 頁籤
2. 在 `/home/你的帳號/` 下建立資料夾 `pudding_diary`
3. 把以下所有檔案上傳進去（保持資料夾結構）：
   ```
   pudding_diary/
   ├── app.py
   ├── wsgi.py
   ├── requirements.txt
   ├── templates/
   │   ├── index.html
   │   ├── record.html
   │   ├── calendar.html
   │   └── stats.html
   └── static/
       └── style.css
   ```

### 步驟三：安裝套件
點選上方 **Consoles** → 開啟 **Bash**，輸入：
```bash
pip3 install --user flask
```

### 步驟四：設定 Web App
1. 點選上方 **Web** 頁籤
2. 點 **Add a new web app**
3. 選 **Manual configuration**（不要選 Flask，要手動設定）
4. Python 版本選 **3.10**
5. 設定 WSGI 檔案：
   - 找到 **WSGI configuration file** 的連結，點進去
   - 把裡面所有內容**全部刪掉**，貼上 `wsgi.py` 的內容
   - ⚠️ 記得把 `YOUR_USERNAME` 換成你的帳號名稱！
   - 儲存

### 步驟五：設定靜態檔案
在 Web 頁籤找到 **Static files**，加入：
- URL: `/static/`
- Directory: `/home/你的帳號/pudding_diary/static`

### 步驟六：啟動！
點 **Reload** 按鈕，然後打開 `你的帳號.pythonanywhere.com` 就完成了！

---

## 資料庫說明

- 使用 **SQLite**，資料會自動儲存在 `diary.db`
- 第一次啟動時會自動建立資料表，不需要手動設定
- 資料表：`daily_records`（詳見 app.py 的 `init_db()` 函式）

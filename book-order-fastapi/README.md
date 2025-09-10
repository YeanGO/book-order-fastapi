# Book Order API (FastAPI + SQLAlchemy + Neon)

這是把原本的 Streamlit 書籍訂購程式抽成 **後端 API** 的最小可行版本。
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 + Neon (Postgres)
- CORS 已開，方便前端（Streamlit/React/HTMX）呼叫
- 內建 `GET /books` 回傳固定書單 & 價格（你可再搬到資料表）
- CRUD：`/orders`（新增、查詢、調整數量、刪除）

## 1. 環境變數
複製 `.env.example` → `.env`，填寫 `DATABASE_URL`（Neon 連線字串，一定要 `?sslmode=require`）。

## 2. 本機啟動
```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
# 開啟 http://127.0.0.1:8000/docs 測試
```

## 3. 部署（Render / Railway 二選一）
### Render
1. 新建 Web Service → 連 GitHub repo
2. Build command：`pip install -r requirements.txt`
3. Start command：`uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. 環境變數：`DATABASE_URL`, `ALLOWED_ORIGINS`

### Railway
1. New Project → Deploy from GitHub
2. Variables：`DATABASE_URL`, `ALLOWED_ORIGINS`, （有需要則 `PORT=8000`）
3. Start command 同上

## 4. 與前端串接
前端只要改成打這些 API：
- `GET /books`
- `GET /orders?skip=0&limit=100`
- `POST /orders`
- `PATCH /orders/{id}`
- `DELETE /orders/{id}`

範例（Python/requests）請見下方說明：
```python
import requests
API_BASE = "https://<你的後端網址>"
requests.post(f"{API_BASE}/orders", json={
    "buyer_name": "Alice",
    "book_title": "python人工智慧",  # 或 "其他(自填)"
    "quantity": 2,
    "unit_price": 450,            # 自填書名時要傳，內建書單時會由後端覆蓋
    "note": "備註"
})
```

## 5. Schema 變更 & Alembic
若要正式管理資料表結構，建議導入 Alembic（`alembic init` 後用 `revision --autogenerate` 產生修改）。

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
from uuid import uuid4

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
async def process(request: Request,
                  pptx_file: UploadFile = File(...),
                  transcript_file: UploadFile = File(...)):

    pptx_path = f"tmp_{uuid4()}.pptx"
    txt_path = f"tmp_{uuid4()}.txt"
    output_path = os.path.join(OUTPUT_DIR, f"result_{uuid4()}.txt")

    # 保存
    with open(pptx_path, "wb") as f:
        shutil.copyfileobj(pptx_file.file, f)
    with open(txt_path, "wb") as f:
        shutil.copyfileobj(transcript_file.file, f)

    # ここで処理（Bedrockや疑似変換）
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned_text = text.replace("えーっと", "").replace("あのー", "").strip() + "\n\n(※仮整形)"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    # 削除
    os.remove(pptx_path)
    os.remove(txt_path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result_url": f"/download/{os.path.basename(output_path)}"
    })

@app.get("/download/{filename}")
async def download(filename: str):
    return FileResponse(os.path.join(OUTPUT_DIR, filename), media_type="text/plain", filename=filename)

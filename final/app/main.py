from fastapi import FastAPI, Request, UploadFile, File, Body, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import boto3
import shutil
from uuid import uuid4
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME", "your-default-bucket")
REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client("s3", region_name=REGION)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get_presigned_url")
async def get_presigned_url(filename: str = Query(...), content_type: str = Query(...)):
    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename, 'ContentType': content_type},
            ExpiresIn=3600
        )
        return {"url": presigned_url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/process_s3")
async def process_s3(pptx_key: str = Body(...), transcript_key: str = Body(...)):
    try:
        pptx_path = f"/tmp/{pptx_key.replace('/', '_')}"
        txt_path = f"/tmp/{transcript_key.replace('/', '_')}"

        s3.download_file(BUCKET_NAME, pptx_key, pptx_path)
        s3.download_file(BUCKET_NAME, transcript_key, txt_path)

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned_text = text.replace("えーっと", "").replace("あのー", "").strip() + "\n\n(※仮整形)"

        output_key = f"results/result_{uuid4()}.txt"
        output_path = f"/tmp/{output_key.replace('/', '_')}"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        s3.upload_file(output_path, BUCKET_NAME, output_key)

        presigned_download_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': output_key},
            ExpiresIn=3600
        )

        return {"download_url": presigned_download_url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

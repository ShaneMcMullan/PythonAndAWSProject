import boto3;
from fastapi import FastAPI
from fastapi import File, UploadFile, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Initialize S3 client with env variables
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@app.get("/")
def read_root():
    return {"message": "Hello AWS Project!"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    from datetime import datetime, timezone
    timeStamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    file.filename = f"{timeStamp}_{file.filename}"
    try:
        s3.upload_fileobj(
            Fileobj = file.file,
            Bucket = "my-fastapi-uploader-12345",
            Key = f"uploadedFiles/{file.filename}",
            ExtraArgs={
                "Metadata": {
                    "Timestamp": timeStamp
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

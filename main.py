import os
from fastapi import FastAPI, UploadFile, File
from pymupdf4llm import to_markdown

app = FastAPI(title="PDF to TextService", version="1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/pdf2markdown")
async def pdf2markdown(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        return {"error": "Only PDF files are supported"}
    
    temp_file_path = f"/tmp/{file.filename}"
    
    try:
        # Save uploaded file to temporary location
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        # Convert PDF to markdown
        markdown_output = to_markdown(temp_file_path)
        
        return {"text": markdown_output}
    
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}
    
    finally:
        # Clean up temporary file if it exists
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

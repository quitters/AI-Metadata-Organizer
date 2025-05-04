import io
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from .core.metadata import extract_metadata as extract_metadata_core

app = FastAPI()

# Allow CORS from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/extract-metadata")
async def extract_metadata(request: Request, image: UploadFile = File(...)):
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        metadata = extract_metadata_core(img)
        if metadata is None:
            return JSONResponse({"error": "Could not extract metadata from image."}, status_code=400)
        # Convert datetime to isoformat for JSON serialization
        result = metadata.__dict__.copy()
        if isinstance(result.get("created_date"), (str, type(None))):
            pass
        else:
            result["created_date"] = result["created_date"].isoformat()
        return JSONResponse(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": f"Internal server error: {str(e)}"}, status_code=500)


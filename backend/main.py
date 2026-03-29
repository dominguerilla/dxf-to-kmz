import os
import shutil
import tempfile
import zipfile
from typing import List

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from converter import convert_dxf_to_kmz

app = FastAPI(title="DXF to KMZ Converter")

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open(FRONTEND_PATH) as f:
        return f.read()


@app.post("/convert")
async def convert(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
):
    temp_dir = tempfile.mkdtemp()
    background_tasks.add_task(shutil.rmtree, temp_dir, True)

    output_files: list[tuple[str, str]] = []
    errors: list[str] = []

    for file in files:
        if not file.filename.lower().endswith(".dxf"):
            errors.append(f"{file.filename}: not a DXF file")
            continue

        base_name = os.path.splitext(file.filename)[0]
        dxf_path = os.path.join(temp_dir, file.filename)
        kmz_path = os.path.join(temp_dir, base_name + ".kmz")

        content = await file.read()
        with open(dxf_path, "wb") as f:
            f.write(content)

        try:
            convert_dxf_to_kmz(dxf_path, kmz_path)
            output_files.append((base_name + ".kmz", kmz_path))
        except Exception as exc:
            errors.append(f"{file.filename}: {exc}")

    if not output_files:
        raise HTTPException(status_code=422, detail="; ".join(errors) or "No valid DXF files provided")

    if len(output_files) == 1:
        kmz_name, kmz_path = output_files[0]
        return FileResponse(
            kmz_path,
            media_type="application/vnd.google-earth.kmz",
            filename=kmz_name,
        )

    zip_path = os.path.join(temp_dir, "converted_kmz_files.zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        for kmz_name, kmz_path in output_files:
            zf.write(kmz_path, kmz_name)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="converted_kmz_files.zip",
    )

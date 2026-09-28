from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI(title="OpenMetadata Documentation")

DOCS_DIR = Path(__file__).resolve().parent / "docs"

# Rutas conocidas → archivo dentro de docs/
DOCUMENTATION_ROUTES = {
    "/documentation": "open.doc.json",
    "/rraae-documentation": "rraae.doc.json",
    "/redi-documentation": "redi.doc.json",
    "/freeradius-documentation": "freeradius.doc.json",
    "/nube-documentation": "nube.doc.json",
    "/fondos-documentation": "fondos.doc.json",
    "/grafana-red-documentation": "grafana-red.doc.json",
    "/ipman-documentation": "ipman.doc.json",
    "/zoom-documentation": "zoom.doc.json"
}


def _docs_file(filename: str) -> Path:
    """Resuelve un archivo dentro de docs/ de forma segura."""
    target = (DOCS_DIR / filename).resolve()
    if not str(target).startswith(str(DOCS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Ruta inválida")
    if not target.is_file():
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {filename}")
    return target


def _serve_doc(filename: str) -> FileResponse:
    path = _docs_file(filename)
    return FileResponse(
        path=path,
        media_type="application/json",
        filename=path.name,
        content_disposition_type="inline",
    )


@app.get("/docs", summary="Listar archivos de documentación")
async def list_documentation() -> dict:
    if not DOCS_DIR.is_dir():
        return {"files": []}
    files = sorted(p.name for p in DOCS_DIR.iterdir() if p.is_file())
    return {"files": files}


@app.get(
    "/docs/{filename}",
    response_class=FileResponse,
    summary="Obtener un archivo de documentación por nombre",
)
async def get_documentation_file(filename: str) -> FileResponse:
    return _serve_doc(filename)


@app.get(
    "/documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de open.doc",
)
async def get_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/documentation"])


@app.get(
    "/rraae-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de rraae.doc",
)
async def get_rraae_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/rraae-documentation"])


@app.get(
    "/redi-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de redi.doc",
)
async def get_redi_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/redi-documentation"])


@app.get(
    "/freeradius-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de freeradius.doc",
)
async def get_freeradius_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/freeradius-documentation"])

@app.get(
    "/nube-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de nube.doc",
)
async def get_freeradius_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/nube-documentation"])

@app.get(
    "/fondos-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de fondos.doc",
)
async def get_fondos_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/fondos-documentation"])

@app.get(
    "/grafana-red-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de grafana-red.doc",
)
async def get_grafana_red_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/grafana-red-documentation"])

@app.get(
    "/ipman-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de ipman.doc",
)
async def get_ipman_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/ipman-documentation"])

@app.get(
    "/zoom-documentation",
    response_class=FileResponse,
    summary="Obtener la documentación de zoom.doc",
)
async def get_zoom_documentation() -> FileResponse:
    return _serve_doc(DOCUMENTATION_ROUTES["/zoom-documentation"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)

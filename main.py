from links.schemas import StatusResponse
from links.api import router
from links.postgres import find_url
from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI(
    title="model_trainer",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(router, prefix="/links")


@app.get('/')
async def root(response_model=StatusResponse, status_code=HTTPStatus.OK):
    return StatusResponse(status='OK')

@app.get('/{short_code}')
async def get_url(short_code: str):
    url = await find_url(alias=short_code)
    if url:
        return RedirectResponse(url)
    return StatusResponse(status=f'ERROR: alias {short_code} not found')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

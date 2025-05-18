from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers.v1 import users

app = FastAPI(
    title="RogersComcastBackend",
    version="0.1.0",
    description="Rogers integration layer",
)

app.include_router(users.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse(url="/docs")


# import uvicorn
# uvicorn.run(app)


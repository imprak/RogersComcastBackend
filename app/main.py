from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers.v1 import (
    api_endpoints,
    hub_endpoints,
    site_intent_endpoints,
    ppod_intent_endpoints,
    transaction_endpoints,
    order_endpoints,
)

app = FastAPI(
    title="RogersComcastBackend",
    version="0.1.0",
    description="Rogers integration layer",
)

app.include_router(api_endpoints.router, prefix="/api/v1")
app.include_router(hub_endpoints.router, prefix="/api/v1")
app.include_router(site_intent_endpoints.router, prefix="/api/v1")
app.include_router(ppod_intent_endpoints.router, prefix="/api/v1")
app.include_router(transaction_endpoints.router, prefix="/api/v1")
app.include_router(order_endpoints.router, prefix="/api/v1")


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
#
# uvicorn.run(app)

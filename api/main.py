from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.routes.predict import router as predict_router
from api.monitoring import setup_monitoring

app = FastAPI(title="Stock Price LSTM API")
setup_monitoring(app)

# Setup para templates HTML (home)
templates = Jinja2Templates(directory="api/static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Rotas de predição
app.include_router(predict_router, prefix="/api")

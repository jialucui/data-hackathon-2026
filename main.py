from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from data_processor import get_top_trends, generate_campaign

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/campaign", response_class=HTMLResponse)
async def campaign(
    request: Request,
    product: str = Form(...),
    audience: str = Form("general audience"),
    goal: str = Form("increase brand awareness")
):
    data = generate_campaign(product, audience, goal)
    return templates.TemplateResponse("campaign.html", {"request": request, "data": data})

@app.get("/trends", response_class=HTMLResponse)
async def trends(request: Request):
    top_trends = get_top_trends(20)
    return templates.TemplateResponse("trends.html", {"request": request, "trends": top_trends})

import base64
from fastapi import FastAPI, Request, Form, File, UploadFile
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
    goal: str = Form("increase brand awareness"),
    asset: UploadFile = File(None)
):
    data = generate_campaign(product, audience, goal)
    
    image_b64 = None
    if asset and asset.filename:
        content = await asset.read()
        image_b64 = f"data:{asset.content_type};base64,{base64.b64encode(content).decode('utf-8')}"

    return templates.TemplateResponse("campaign.html", {"request": request, "data": data, "product": product, "image_b64": image_b64})

@app.get("/trends", response_class=HTMLResponse)
async def trends(request: Request):
    top_trends = get_top_trends(20)
    return templates.TemplateResponse("trends.html", {"request": request, "trends": top_trends})

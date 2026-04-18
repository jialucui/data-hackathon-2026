import base64
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from data_processor import generate_campaign, get_top_trends

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def normalize_campaign_data(data: Any) -> Dict[str, Any]:
    """Ensure template never breaks on partial API JSON."""
    if not isinstance(data, dict):
        return {
            "product": "",
            "audience": "",
            "goal": "",
            "campaign_creative_summary": "",
            "videos": [],
            "milestones": [],
        }
    out = dict(data)
    out.setdefault("product", "")
    out.setdefault("audience", "")
    out.setdefault("goal", "")
    out.setdefault("campaign_creative_summary", "")
    out.setdefault("videos", [])
    out.setdefault("milestones", [])
    fixed: List[Dict[str, Any]] = []
    for v in out["videos"] or []:
        if not isinstance(v, dict):
            continue
        row = dict(v)
        sc = row.get("script")
        if not isinstance(sc, dict):
            sc = {}
        row["script"] = {
            "hook": str(sc.get("hook", "")),
            "body": str(sc.get("body", "")),
            "cta": str(sc.get("cta", "")),
        }
        for key in (
            "title",
            "type",
            "format",
            "trend",
            "algorithm_analysis",
            "fine_tuning",
            "best_post_time",
            "content_strategy",
            "music_and_sound",
            "visual_style",
            "thumbnail_direction",
            "product_execution_example",
            "estimated_length",
        ):
            row.setdefault(key, "")
        row.setdefault("schedule_day", 0)
        row.setdefault("goal", "")
        row.setdefault("icon", "")
        fixed.append(row)
    out["videos"] = fixed
    return out


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/campaign", response_class=HTMLResponse)
async def campaign(
    request: Request,
    product: str = Form(...),
    product_details: str = Form(""),
    audience: str = Form("general audience"),
    goal: str = Form("increase brand awareness"),
    assets: Optional[List[UploadFile]] = File(default=None),
):
    data = normalize_campaign_data(
        generate_campaign(product, product_details, audience, goal)
    )

    images_b64: List[str] = []
    for asset in assets or []:
        if asset and getattr(asset, "filename", None):
            content = await asset.read()
            ct = asset.content_type or "image/png"
            images_b64.append(
                f"data:{ct};base64,{base64.b64encode(content).decode('utf-8')}"
            )

    return templates.TemplateResponse(
        "campaign.html",
        {
            "request": request,
            "data": data,
            "product": product,
            "product_details": product_details,
            "audience": audience,
            "goal": goal,
            "images_b64": images_b64,
        },
    )

@app.get("/trends", response_class=HTMLResponse)
async def trends(request: Request):
    top_trends = get_top_trends(20)
    return templates.TemplateResponse("trends.html", {"request": request, "trends": top_trends})

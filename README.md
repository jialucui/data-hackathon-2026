# Trending Piggybacking Simulator

A Windows 95-styled Python web app that generates complete 5-video YouTube marketing campaigns for your product by piggybacking on real trending topics.

## What It Does

Enter your product, target audience, and campaign goal — the app scans a YouTube trending dataset, picks the top viral tags by engagement, and generates:

- **5 unique video scripts** (Hook → Body → CTA), one per trending angle
- **Posting schedule** (Day 1, 3, 5, 8, 12)
- **Campaign milestones** (Views → Followers → CTR → Conversions)
- **Copy-to-clipboard** for all scripts

Video formats included:
| # | Format | Goal |
|---|--------|------|
| 1 | 🎣 Trend Hook | Awareness |
| 2 | 🏆 Challenge Video | Engagement |
| 3 | ⚔️ Comparison Video | Credibility |
| 4 | 💬 Story Video | Trust |
| 5 | 🚀 Results Video | Conversion |

## Tech Stack

- **Backend:** Python + FastAPI
- **Templates:** Jinja2 HTML
- **Styling:** Custom Windows 95 / Minesweeper CSS
- **Data:** Pandas (reads YouTube trending CSV)

## Setup & Run

```bash
# Create virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pandas jinja2 python-multipart

# Drop your YouTube trending CSV into the parent folder as CA_Trending.csv
# Expected columns: tags, likes, title, channel_title, views

# Run
uvicorn main:app --reload --port 8000
```

Open [http://localhost:8000](http://localhost:8000)

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home — input form |
| `/campaign` | 5-video campaign with full scripts |
| `/trends` | Browse top trending tags from dataset |

## Algorithm

1. Parse all rows in `CA_Trending.csv`
2. Aggregate total likes per tag keyword → rank top 100 trends
3. Randomly sample 5 different trends (one per video type)
4. Apply 5 scriptwriting templates with product + trend substitution

> **To upgrade to real AI**: replace `generate_campaign()` in `data_processor.py` with an OpenAI API call — the routes and templates stay unchanged.

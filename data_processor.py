import pandas as pd
import random
import os

CSV_PATH = '../CA_Trending.csv'

# Cache trends so we only read CSV once
_trends_cache = None

def get_top_trends(limit=50):
    global _trends_cache
    if _trends_cache is not None:
        return _trends_cache[:limit]
    
    try:
        if not os.path.exists(CSV_PATH):
            _trends_cache = [{"tag": "viral challenge", "score": 999}]
            return _trends_cache[:limit]
        
        df = pd.read_csv(CSV_PATH)
        tag_scores = {}
        
        for _, row in df.iterrows():
            tags_str = str(row.get('tags', ''))
            likes = int(row.get('likes', 0)) if pd.notnull(row.get('likes')) else 0
            
            if tags_str and tags_str not in ('[none]', 'nan'):
                tags = [t.strip().lower() for t in tags_str.split('|')]
                for tag in tags:
                    if len(tag) > 2:  # skip super short tags
                        tag_scores[tag] = tag_scores.get(tag, 0) + likes
                        
        sorted_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
        _trends_cache = [{"tag": t[0], "score": t[1]} for t in sorted_tags[:200]]
        return _trends_cache[:limit]
    except Exception as e:
        print(f"Error parsing data: {e}")
        _trends_cache = [{"tag": "viral content", "score": 999}]
        return _trends_cache[:limit]


def generate_campaign(product: str, audience: str, goal: str):
    """
    Generate a full 5-video campaign plan with scripts.
    Each video uses a different trending hook and script style.
    """
    # Pick 5 different trends for 5 different videos
    trends = get_top_trends(100)
    selected = random.sample(trends, min(5, len(trends)))
    
    video_types = [
        {
            "type": "借势钩子 (Trend Hook)",
            "format": "Open with the trend, pivot to product",
            "schedule_day": 1,
            "goal": "Awareness — get people to recognize your product",
            "icon": "🎣",
        },
        {
            "type": "挑战视频 (Challenge Video)",
            "format": "Start a challenge that links the trend to your product",
            "schedule_day": 3,
            "goal": "Engagement — get viewers to participate and share",
            "icon": "🏆",
        },
        {
            "type": "对比视频 (Comparison Video)",
            "format": "VS format: trend vs your product, twist ending",
            "schedule_day": 5,
            "goal": "Credibility — prove your product belongs in the conversation",
            "icon": "⚔️",
        },
        {
            "type": "故事视频 (Story Video)",
            "format": "Personal story connecting the trend experience to your product",
            "schedule_day": 8,
            "goal": "Trust — create emotional connection with audience",
            "icon": "💬",
        },
        {
            "type": "结果视频 (Results Video)",
            "format": "30-day results after using the product while following the trend",
            "schedule_day": 12,
            "goal": "Conversion — push viewers to buy",
            "icon": "🚀",
        },
    ]
    
    videos = []
    for i, vtype in enumerate(video_types):
        trend = selected[i % len(selected)]['tag']
        video = generate_video_script(product, audience, goal, trend, vtype)
        videos.append(video)
    
    return {
        "product": product,
        "audience": audience,
        "goal": goal,
        "videos": videos,
        "milestones": [
            {"week": 1, "target": "1,000+ views on launch video", "kpi": "views"},
            {"week": 2, "target": "500+ followers gained", "kpi": "followers"},
            {"week": 3, "target": "5%+ click-through to product page", "kpi": "ctr"},
            {"week": 4, "target": "First sales attributed to campaign", "kpi": "conversions"},
        ]
    }


def generate_video_script(product: str, audience: str, goal: str, trend: str, vtype: dict) -> dict:
    """Generate a complete video script based on the type."""
    
    trend_cap = trend.title()
    
    scripts = {
        "借势钩子 (Trend Hook)": {
            "title": f'Everyone is talking about "{trend_cap}" — but have you seen THIS?',
            "hook": f"[OPEN on a trending {trend_cap} clip or reference]\n"
                    f"VO: \"You've been obsessed with {trend_cap} all week. I get it. But what if I told you there's something that takes that same energy and puts it to WORK for you?\"",
            "body": f"[CUT to product reveal]\n"
                    f"VO: \"Introducing {product} — the {trend_cap} of the {_get_industry(product)} world.\"\n\n"
                    f"[Show product in action, overlaid with trending music/sounds]\n"
                    f"VO: \"While everyone else is chasing {trend_cap}, smart people are using {product} to actually get results.\"\n\n"
                    f"[3 quick benefit callouts, text on screen]\n"
                    f"- Benefit 1: [describe your product benefit here]\n"
                    f"- Benefit 2: [describe your product benefit here]\n"
                    f"- Benefit 3: [describe your product benefit here]",
            "cta": f"[End card]\n\"Link in bio. Be the person who was EARLY on {product}.\"\nHashtags: #{trend.replace(' ', '')} #{product.replace(' ', '')} #trending #viral",
        },
        "挑战视频 (Challenge Video)": {
            "title": f"I did the {trend_cap} Challenge but make it {product} 🔥",
            "hook": f"[HOOK — camera straight to face, energetic]\n"
                    f"\"Okay so the {trend_cap} challenge is everywhere. I'm doing it, but I'm adding a twist that no one has thought of yet.\"",
            "body": f"[Show the challenge beginning normally]\n"
                    f"[TWIST: incorporate {product} into the challenge]\n"
                    f"VO: \"Here's what happens when you bring {product} into the {trend_cap} world...\"\n\n"
                    f"[Demonstrate the combined experience entertainingly]\n"
                    f"[Reaction shots — excitement, surprise]\n\n"
                    f"VO: \"The results? Way better than I expected.\"\n"
                    f"[Show outcome, ideally with measurable result]",
            "cta": f"\"I'm starting the #{product.replace(' ', '')}x{trend_cap.replace(' ', '')}Challenge — tag me when you try it.\"\n"
                   f"\"All my info is in the bio.\"\n"
                   f"Hashtags: #{trend.replace(' ', '')}Challenge #{product.replace(' ', '')} #challenge #fyp",
        },
        "对比视频 (Comparison Video)": {
            "title": f"{trend_cap} vs {product}: I tested BOTH for 7 days",
            "hook": f"[Split screen visual]\n"
                    f"VO: \"Everyone hyping up {trend_cap}. Me? I brought {product} into the fight. Here's who won.\"",
            "body": f"[Day 1 — try the {trend_cap} approach]\n"
                    f"\"Day one using only {trend_cap} content strategy... [result]\"\n\n"
                    f"[Day 4 — switch to {product}]\n"
                    f"\"Day four, I switched to {product}. Here's what happened immediately...\"\n\n"
                    f"[Side-by-side results]\n"
                    f"Category 1: {trend_cap} ← vs → {product} ✅\n"
                    f"Category 2: {trend_cap} ✅ → vs → {product} ←\n"
                    f"Category 3: {trend_cap} ← vs → {product} ✅\n\n"
                    f"\"The verdict? [Honest nuanced take, but {product} wins overall]\"",
            "cta": f"\"Drop a 1 if you're team {trend_cap}, drop a 2 if you want {product}.\"\n"
                   f"\"Link to try {product} yourself is in my bio.\"\n"
                   f"Hashtags: #{trend.replace(' ', '')} #vs #{product.replace(' ', '')} #review #honest",
        },
        "故事视频 (Story Video)": {
            "title": f"How I went from obsessing over {trend_cap} to actually changing my life with {product}",
            "hook": f"[Quiet, personal tone. Low camera angle, cozy setting]\n"
                    f"\"Can I be honest with you for a second? Three months ago I was deep in the {trend_cap} rabbit hole.\"\n"
                    f"\"I thought that was the answer. It wasn't. This is what actually worked.\"",
            "body": f"[The before story — relatable struggle]\n"
                    f"\"I was like everyone else. Following {trend_cap}, watching every video, trying everything.\"\n"
                    f"\"But nothing was moving the needle for {_get_pain_point(product)}.\"\n\n"
                    f"[The discovery moment]\n"
                    f"\"Then someone recommended {product} and I almost didn't try it because [relatable objection].\"\n\n"
                    f"[The journey — show progress, be specific]\n"
                    f"\"Week 1: [small win]\"\n"
                    f"\"Week 2: [bigger win]\"\n"
                    f"\"By week 4: [transformation result]\"\n\n"
                    f"[Emotional payoff]\n"
                    f"\"The thing about {trend_cap} is it gives you the feeling. {product} gives you the result.\"",
            "cta": f"\"If you're where I was three months ago, try {product}.\"\n"
                   f"\"I'll leave my link in the bio. No pressure, but this is my honest story.\"\n"
                   f"Hashtags: #{trend.replace(' ', '')} #{product.replace(' ', '')} #storytime #personaldev",
        },
        "结果视频 (Results Video)": {
            "title": f"30 Days of {product} (while everyone was distracted by {trend_cap}): FINAL RESULTS",
            "hook": f"[Bold text on screen: '30 DAYS LATER']\n"
                    f"VO: \"While everyone was still talking about {trend_cap} for 30 days straight... I was using {product}. Here are my actual results, no filter.\"",
            "body": f"[Montage of 30-day journey, quick cuts]\n"
                    f"Day 1: \"Starting point — [your baseline stat]\"\n"
                    f"Day 7: \"First sign it was working — [early result]\"\n"
                    f"Day 15: \"Midpoint check — [measurable improvement]\"\n"
                    f"Day 30: \"Final result — [transformation number/visual]\"\n\n"
                    f"[What I would have missed if I chased {trend_cap} instead]\n"
                    f"VO: \"Trending content gets views. {product} gets results. Here's the difference.\"\n\n"
                    f"[Visual comparison: before/after or metric chart]",
            "cta": f"\"My 30-day {product} plan is linked in my bio. Start yours today.\"\n"
                   f"\"Comment '30' and I'll send you my exact routine.\"\n"
                   f"Hashtags: #{product.replace(' ', '')}Results #30dayChallenge #{trend.replace(' ', '')} #transformation",
        },
    }
    
    script_data = scripts.get(vtype["type"], scripts["借势钩子 (Trend Hook)"])
    
    return {
        "title": script_data["title"],
        "type": vtype["type"],
        "format": vtype["format"],
        "schedule_day": vtype["schedule_day"],
        "goal": vtype["goal"],
        "icon": vtype["icon"],
        "trend": trend,
        "script": {
            "hook": script_data["hook"],
            "body": script_data["body"],
            "cta": script_data["cta"],
        },
        "estimated_length": "60-90 seconds",
    }


def _get_industry(product: str) -> str:
    """Guess the industry for better phrasing."""
    product_lower = product.lower()
    if any(w in product_lower for w in ['water', 'drink', 'juice', 'tea', 'coffee', 'food', 'snack']):
        return 'beverage'
    if any(w in product_lower for w in ['shoe', 'shirt', 'dress', 'jacket', 'bag', 'watch']):
        return 'fashion'
    if any(w in product_lower for w in ['phone', 'laptop', 'tablet', 'headphone', 'earphone']):
        return 'tech'
    if any(w in product_lower for w in ['cream', 'serum', 'mask', 'skincare', 'makeup', 'lipstick']):
        return 'beauty'
    return 'industry'


def _get_pain_point(product: str) -> str:
    """Return a relatable pain point based on product category."""
    product_lower = product.lower()
    if any(w in product_lower for w in ['water', 'drink', 'juice', 'tea', 'coffee']):
        return 'staying energized and hydrated throughout the day'
    if any(w in product_lower for w in ['shoe', 'shirt', 'dress', 'jacket']):
        return 'finding something that felt like ME'
    if any(w in product_lower for w in ['phone', 'laptop', 'tablet']):
        return 'staying productive without burning out'
    if any(w in product_lower for w in ['cream', 'serum', 'skincare']):
        return 'getting my skin to actually look good'
    return 'getting real results in this area'

from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

from fastapi.staticfiles import StaticFiles
# from pathlib import Path
from pydantic import BaseModel
import tftStats
import starlette.status as status
import pandas as pd
# import altair as alt

app = FastAPI()
app.mount("/site", StaticFiles(directory="static", html = True), name="static")
templates = Jinja2Templates(directory="templates/")

@app.get("/")
async def form_post(request: Request):
    return templates.TemplateResponse('form.html', context={'request': request})

@app.post("/")
async def form_post(request: Request, matchcount: int = Form(...), apikey: str = Form(...), region: str = Form(...), summonername: str = Form(...)):
    print('matchcount:', matchcount,'apikey:', apikey, 'summonername:', summonername,'region:', region)
    
    # chart_info = tftStats.calculateStats(apikey, region, [summonername], str(matchcount))
    summoner_names: list = [summonername] if ',' not in summonername else summonername.split(',')
    chart_info = tftStats.calculateStats(apikey, region, summoner_names, str(matchcount))

    data = pd.DataFrame(
        data = chart_info,
        index=["Summoner #" + str(x) for x in range(1, len(chart_info["Summoner Name"]) + 1)],
        columns=["Summoner Name", "Average Damage", "Average Placement", "Average Players Eliminated", "Average Final Level"]
    )

    # Here, want to optimize by removing duplicates and sorting data table by values (or enabling dynamic chart)
    data = data.drop_duplicates(subset='Summoner Name', keep="first")
    # print(data)

    return templates.TemplateResponse(
        'summary_page.html',
        {'request': request, 'data': data.to_html()}
    )
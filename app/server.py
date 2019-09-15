import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://drive.google.com/uc?export=download&id=1Wl1-6MBKRJ7WzXaoY9-_4hROflrFO0so'
export_file_name = 'export.pkl'

classes = ['burned', 'normal']
path = Path(__file__).parent

export_file_url_utility = 'https://drive.google.com/uc?export=download&id=1-Sh_yMHAfwQd-OQ1-R1wl-iQAGuE3GQF'
export_file_name_utility = 'final.pkl'

classes_utility = ['pole', 'no_pole']
path_utility = Path(__file__).parent


app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

async def setup_learner_utility():
    await download_file(export_file_url_utility, path / export_file_name_utility)
    try:
        learn_utility = load_learner(path, export_file_name_utility)
        return learn_utility
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner()),asyncio.ensure_future(setup_learner_utility())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
learn_utility = loop.run_until_complete(asyncio.gather(*tasks))[1]
loop.close()

@app.route('/')
async def homepage(request):
    return RedirectResponse(url='/wildfires/prevention')

@app.route('/wildfires/rehabilitation')
async def rehabilitation(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())

@app.route('/wildfires/prevention')
async def utility_page(request):
    html_file = path / 'view' / 'utilities.html'
    return HTMLResponse(html_file.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})


@app.route('/analyze_utility', methods=['POST'])
async def analyze_utility(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn_utility.predict(img)[0]
    return JSONResponse({'result': str(prediction)})

if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")

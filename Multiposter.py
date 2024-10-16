import os, sys, subprocess, asyncio, base64, json
from inspect import iscoroutinefunction
from aiohttp import web
from aiohttp_index import IndexMiddleware
from CustomGui import CustomGui

app_path = '.'
if not getattr(sys, 'frozen', False):
    app_path = os.path.dirname(os.path.realpath(__file__))

def _create_gui(loop, buttonCb, interval):
    gui = CustomGui(loop, buttonCb, interval)
    gui.title("Multiposter")
    return gui

async def _starter(cb, interval=1/120):
    app = web.Application(middlewares=[IndexMiddleware()])
    routes = web.RouteTableDef()

    # ROUTES
    routes.static('/', app_path + '/public_html')

    @routes.post('/post')
    async def post(req):
        try:
            data = await req.json()
            post = {
                "content": data['content']
            }
            if data.get('image'):
                image_content = base64.b64decode(data['image']['content'].split('base64,')[1])
                if not os.path.isdir('C:/temp'):
                    os.mkdir('C:/temp')
                with open('C:/tmp/mpop-post-image.png', 'wb') as f:
                    f.write(image_content)
                post['image'] = image_content
                post['image_url'] = data['image']['content']
                post['image_name'] = data['image']['name']
                post['image_type'] = data['image']['type']
                post['image_path'] = 'C:/tmp/mpop-post-image.png'
            try:
                if (iscoroutinefunction(cb)):
                    await cb(post)
                else:
                    cb(post)
                return web.Response(status=200)
            except Exception as e:
                return web.Response(
                    status=400,
                    content_type='application/json',
                    text=json.dumps({"error": str(e)})
                )
        except:
            return web.Response(
                status=400,
                content_type='application/json',
                text=json.dumps({"error": "Invalid data"})
            )

    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 0)
    await site.start()
    self_url = 'http://localhost:' + str(site._server.sockets[0].getsockname()[1])
    def start_browser():
        if sys.platform=='win32':
            os.startfile(self_url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', self_url])
        else:
            try:
                subprocess.Popen(['xdg-open', self_url])
            except OSError:
                print('Please open a browser on: '+self_url)
    loop = asyncio.get_event_loop()
    _create_gui(loop, start_browser, interval)
    start_browser()
    while True:
        await asyncio.sleep(interval)


def start(cb):
    asyncio.run(_starter(cb))
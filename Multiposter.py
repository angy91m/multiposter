import os, sys, subprocess
dir_path = os.path.dirname(os.path.realpath(__file__))
from aiohttp import web
from aiohttp_index import IndexMiddleware
import asyncio
import base64
from CustomGui import CustomGui

def create_gui(loop):
    gui = CustomGui(loop)
    gui.title("Multiposter")
    return gui

async def _starter():
    app = web.Application(middlewares=[IndexMiddleware()])
    routes = web.RouteTableDef()

    # ROUTES
    routes.static('/', dir_path + '/public_html')

    @routes.post('/post')
    async def post(req):
        try:
            data = await req.json()
            post = {
                "title": data['title'],
                "content": data['content']
            }
            if data.get('image'):
                post['image'] = base64.b64decode(data['image']['content'].split('base64,')[1])
            print(post)
            return web.Response(status=200)
        except ValueError:
            return web.Response(status=400)

    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 3091)
    await site.start()
    self_url = 'http://localhost:' + str(site._server.sockets[0].getsockname()[1])
    #self_url = 'http://localhost:3091'
    
    # if sys.platform=='win32':
    #     os.startfile(self_url)
    # elif sys.platform=='darwin':
    #     subprocess.Popen(['open', self_url])
    # else:
    #     try:
    #         subprocess.Popen(['xdg-open', self_url])
    #     except OSError:
    #         print('Please open a browser on: '+self_url)
    loop = asyncio.get_event_loop()
    gui = create_gui(loop)
    loop.run()


def start():
    asyncio.run(_starter())

start()
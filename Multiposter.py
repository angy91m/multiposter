import os, sys, subprocess, asyncio, base64, json, magic, mimetypes
from inspect import iscoroutinefunction
from aiohttp import web
from aiohttp_index import IndexMiddleware
from CustomGui import CustomGui
from ftplib import FTP_TLS

app_path = os.path.dirname(os.path.realpath(__file__))
if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS

def random_hex(length=6):
    return os.urandom(length).hex()

def load_config():
    with open(app_path + '/config.json') as f:
        return json.load(f)

def upload_image(config, image_path, image_name):
    availEncodings = ['Latin-1', 'utf-8']
    uploaded = False
    for encoding in availEncodings:
        try:
            ftp = FTP_TLS(encoding=encoding)
            ftp.connect(config['ftpHost'], config['ftpPort'])
            ftp.login(config['ftpUser'], config['ftpPassword'])
            ftp.prot_p()
            ftp.encoding = 'utf-8'
            ftp.cwd(config['ftpPath'])
            with open(image_path, 'rb') as f:
                ftp.storbinary('STOR '+ image_name, f)
            ftp.quit()
            uploaded = True
            break
        except Exception as e:
            print(e)
    if not uploaded:
        print('Failed to upload image: ' + image_name)
        raise Exception('Failed to upload image: ' + image_name)

def _create_gui(loop, buttonCb, stop_loop, interval):
    gui = CustomGui(loop, buttonCb, stop_loop, interval)
    gui.title("Multiposter")
    return gui

async def _starter(cb, interval=1/120):
    config = load_config()
    app = web.Application(middlewares=[IndexMiddleware()])
    routes = web.RouteTableDef()

    # ROUTES
    routes.static('/', app_path + '/public_html')

    @routes.post('/post')
    async def post(req):
        try:
            data = await req.json()
            if type(data['content']) != str or data['content'].strip() == '':
                return web.Response(
                    status=400,
                    content_type='application/json',
                    text=json.dumps({"error": "Empty content"})
                )
            if (
                type(data['socials']) != list
                or len(data['socials']) == 0
                or any((type(social) != str or social.strip() == '') for social in data['socials'])
            ):
                return web.Response(
                    status=400,
                    content_type='application/json',
                    text=json.dumps({"error": "Empty socials"})
                )
            post = {
                "content": data['content'],
                "socials": data['socials']
            }
            if data.get('image'):
                image_content = base64.b64decode(data['image']['content'].split('base64,')[1])
                image_type = magic.from_buffer(image_content, mime=True)
                if (image_type[0:6] != 'image/'):
                    return web.Response(
                        status=400,
                        content_type='application/json',
                        text=json.dumps({"error": "Invalid image type"})
                    )
                image_ext = mimetypes.guess_extension(image_type)
                if image_ext is None:
                    return web.Response(
                        status=400,
                        content_type='application/json',
                        text=json.dumps({"error": "Invalid image type"})
                    )
                image_name = 'mpop-post-image-' + random_hex() + image_ext
                if not os.path.isdir(app_path + '/uploaded_imgs'):
                    os.mkdir(app_path + '/uploaded_imgs')
                with open(app_path + '/uploaded_imgs/' + image_name, 'wb') as f:
                    f.write(image_content)
                upload_image(config, app_path + '/uploaded_imgs/' + image_name, image_name)
                post['image'] = image_content
                post['image_url'] = config['defaultUrl'] + '/' + image_name
                post['image_original_name'] = data['image']['name']
                post['image_name'] = image_name
                post['image_type'] = image_type
                post['image_path'] = app_path + '/uploaded_imgs/' + image_name
                post['image_b64'] = data['image']['content']
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
        except Exception as e:
            print(e)
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
    continue_loop = True
    def stop_loop():
        nonlocal continue_loop
        continue_loop = False
    
    _create_gui(loop, start_browser, stop_loop, interval)
    start_browser()
    while continue_loop:
        await asyncio.sleep(interval)
    loop.stop()
    exit(0)


def start(cb):
    asyncio.run(_starter(cb))
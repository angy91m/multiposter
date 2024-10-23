from Multiposter import start

def post_data(post, config):
    if 'image' in post:
        if len(post['image']) > 20:
            post['image'] = post['image'][0:20] + b'...'
        if len(post['image_b64']) > 20:
            post['image_b64'] = post['image_b64'][0:20] + '...'
    print('POST:')
    print(post)

if __name__ == '__main__':
    start(post_data)
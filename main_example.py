from Multiposter import start

def post_data(post):
    if post['image']:
        print('IMAGE:')
        print(post['image'])
        print('\n\n')
        del post['image']
    print('POST:')
    print(post)

if __name__ == '__main__':
    start(post_data)
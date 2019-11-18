import os
from concurrent import futures

import requests
from PIL import Image

MAX_WORKERS = 20

URL = (
    'https://image.slidesharecdn.com/'
    'logging-best-practices-public-190202232740/95/'
    'logging-best-practices-{}-638.jpg?cb=1549150230'
)

DOWNLOAD_PATH = os.path.expanduser('~/Desktop/images/')


def save_file(url, local_filename):
    if not os.path.exists(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)
    file = os.path.join(DOWNLOAD_PATH, '{}.jpg'.format(local_filename))
    print(url)
    r = requests.get(url, stream=True)
    with open(file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def download_one(args):
    save_file(*args)


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


def join_image_to_pdf(targe_file='~/Desktop/default.pdf'):
    image_lst = [
        Image.open(os.path.join(DOWNLOAD_PATH, f))
        for f in sorted(os.listdir(DOWNLOAD_PATH), key=lambda x: int(x.split('.')[0]))
        if f.endswith('.jpg')
    ]

    image1 = image_lst[0]
    pdf_name = os.path.expanduser(targe_file)
    image1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=image_lst)


def main(page_count):
    lst = [(URL.format(i), i) for i in range(1, page_count)]
    return download_many(lst)


if __name__ == '__main__':
    page_count = 35
    rv = main(page_count)
    print(rv)
    join_image_to_pdf('~/Desktop/logging-best-practices.pdf')

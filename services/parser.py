from database.connector import engine, get_session, get_connection, execute_query
from models.model import Video, Author, Category, Comment
import requests


CATEGORIES_API = 'https://rutube.ru/api/video/category/'
# [
#     {
#         "id": 78,
#         "category_url": "https://rutube.ru/video/category/78/",
#         "related_showcase": null,
#         "name": "Обзоры и распаковки товаров",
#         "short_name": "goods",
#         "for_kids": false
#     },
#     {
#         "id": 73,
#         "category_url": "https://rutube.ru/video/category/73/",
#         "related_showcase": null,
#         "name": "Лайфстайл",
#         "short_name": "lifestyle",
#         "for_kids": false
#     },
#     ...


VIDEOS_URLS_API = 'https://rutube.ru/api/video/category/{id}/{date}/'
# {
#     "has_next": true,
#     "next": "https://rutube.ru/api/video/category/8/10042024/?page=2",
#     "previous": null,
#     "page": 1,
#     "per_page": 100,
#     "results": [
#         {
#             "id": "6e4d63138f7d572283f44f6d730d0ce0",
#             "thumbnail_url": "https://pic.rutubelist.ru/video/00/50/00507dd1c939b4e56e392b488758f4dd.jpg",
#             "video_url": "https://rutube.ru/video/6e4d63138f7d572283f44f6d730d0ce0/",
#             "duration": 30,
#             "picture_url": "",
#             "author": {
#                 "id": 25256830,
#                 "name": "ТЕЛЕКОМПАНИЯ \"ТЫНДА\"",
#                 "avatar_url": "https://pic.rutubelist.ru/user/77/0a/770a4defb8088d95dcd6371ace440cf5.jpg",
#                 "site_url": "https://rutube.ru/video/person/25256830/"
#             },
#             "pg_rating": {
#                 "age": 12,
#                 "logo": "https://pic.rutubelist.ru/agerestriction/99/0e/990e87f25d8689833de24c0eb7eaec81.png"
#             },
#             "origin_type": "rtb",
#             "embed_url": "https://rutube.ru/play/embed/6e4d63138f7d572283f44f6d730d0ce0",
#             "category": {
#                 "id": 8,
#                 "category_url": "https://rutube.ru/video/category/8/",
#                 "name": "Новости и СМИ"
#             },
#             "feed_url": "https://rutube.ru/video/person/25256830/",
#             "feed_name": "ТЕЛЕКОМПАНИЯ \"ТЫНДА\"",
#             "preview_url": "https://preview.rutube.ru/preview/6e4d63138f7d572283f44f6d730d0ce0.webp?exp=1713104109&s=ZkmivB4P42Q1FVScURjxQQ",
#             "is_club": false,
#             "is_classic": true,
#             "is_paid": false,
#             "product_id": null,
#             "hits": 2,
#             "publication_ts": "2024-04-13T16:08:34",
#             "is_official": true,
#             "stream_type": null,
#             "is_adult": false,
#             "last_update_ts": "2024-04-13T16:08:34",
#             "is_licensed": false,
#             "kind_sign_for_user": false,
#             "is_audio": false,
#             "is_hidden": false,
#             "is_original_content": false,
#             "track_id": 172557943,
#             "title": "РЕКВИЕМ _ КУРОЧКИН Ю.А.",
#             "description": "",
#             "is_livestream": false,
#             "html": "<iframe width=\"720\" height=\"405\" src=\"https://rutube.ru/play/embed/6e4d63138f7d572283f44f6d730d0ce0\" frameborder=\"0\" webkitAllowFullScreen mozallowfullscreen allowfullscreen allow=\"encrypted-media\"></iframe>",
#             "action_reason": {
#                 "id": 0,
#                 "name": ""
#             },
#             "is_original_sticker_2x2": false,
#             "created_ts": "2024-04-10T10:37:25"
#         },

VIDEO_API = 'https://rutube.ru/api/video/{}'# guid/
COMMENTS_API = 'https://rutube.ru/api/comments/video/{}'# guid/
AUTORS_API = 'https://rutube.ru/api/video/person/{}/'# id/
CHILD_COMMENTS_API = 'https://rutube.ru/api/comments/video/{}/?parent_id={}' # guid/ parent_id/

def get_categories():
    return requests.get(CATEGORIES_API).json()

async def parse_categories():
    categories = get_categories()
    for category in categories:
        category_id = category['id']
        category_name = category['name']
        category_url = category['category_url']


        async with get_session() as session:
            category = Category(
                id=category_id,
                name=category_name,
                category_url=category_url
            )
            session.add(category)
            await session.commit()


async def insert_child_comments(url, parent_id):
    fin_url = CHILD_COMMENTS_API.format(url, parent_id)
    response = requests.get(fin_url).json()
    comments = []
    with response["results"] as res:
        for elind in range(len(res)):
            comments.append(Comment(
                id = res[elind]["id"],
                video_id = url,
                root_id = None, # TODO решить, что именно заполняется: ничего или ничего
                text = res[elind]["text"],
                tone = None,
                likes = res[elind]["likes_number"],
                dislikes = res[elind]["dislikes_number"],
                ))
            """ # Ярослав сказал "Рекурсия замкнёт асинхронный вызов" или что-то такое. Но так теряются ответы на ответы. Но таких на Рутьюбе 0
            if res[elind]["replies_number"]:
                asyncio.run(insert_child_comments(url, res[elind]["id"]))
            """
    s = get_session()
    s.add(comments)
    await s.commit()
    
async def insert_comments(url):
    fin_url = COMMENTS_API.format(url)
    response = requests.get(fin_url).json()
    comments = []
    with response["results"] as res:
        for elind in range(len(res)):
            comments.append(Comment(
                id = res[elind]["id"],
                video_id = url,
                root_id = None, # TODO решить, что именно заполняется: ничего или ничего
                text = res[elind]["text"],
                tone = None,
                likes = res[elind]["likes_number"],
                dislikes = res[elind]["dislikes_number"],
                ))
            if res[elind]["replies_number"]:
                asyncio.run(insert_child_comments(url, res[elind]["id"]))
    s = get_session()
    s.add(comments)
    await s.commit()

# def get_vi



if __name__ == '__main__':
    import asyncio
    asyncio.run(parse_categories())

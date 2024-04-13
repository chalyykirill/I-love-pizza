from database.connector import engine, get_session, get_connection, execute_query
from models.model import Video, Author, Category, Comment
from sqlalchemy import select
import requests
import aiohttp
import asyncio
from datetime import datetime

CATEGORIES_API = 'https://rutube.ru/api/video/category/'
VIDEOS_URLS_API = 'https://rutube.ru/api/video/category/{id}/{date}/'


VIDEO_API = 'https://rutube.ru/api/video/{}/'# guid/
COMMENTS_API = 'https://rutube.ru/api/comments/video/{}/'# guid/
AUTORS_API = 'https://rutube.ru/api/video/person/{}/'# id/

CHILD_COMMENTS_API = 'https://rutube.ru/api/comments/video/{}/?parent_id={}' # guid/ parent_id/

VOTE_API = 'https://rutube.ru/api/numerator/video/{}/vote'

VIDEO_LIKES_DISLIKES_API = "https://rutube.ru/api/numerator/video/{}/vote"


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

async def get_videos_guids(category_id:int, date:int, page:int):
    # async increment 'page' param till response is not
    # {
    # "detail": "Неправильная страница"
    # }
    url = VIDEOS_URLS_API.format(id=category_id, date=date)
    async with aiohttp.ClientSession() as session:
        async with session.get(url+f"?page={page}") as response:
            response = await response.json()
            if response.get('detail'):
                return
            else:
                authors = [video['author'] for video in response['results']]
                for author in authors:
                    id = author['id']
                    name = author['name']
                    site_url = author['site_url']
                    async with get_session() as session:
                        # check if author already exists

                        stmt = select(Author).where(Author.id == id)
                        res = await session.execute(stmt)
                        a = res.scalars().first()

                        if a:
                            continue
                        author = Author(
                            id=id,
                            name=name,
                            site_url=site_url
                        )
                        session.add(author)
                await session.commit()

                for video in response['results']:
                    guid = video['id']
                    video_url = video['video_url']
                    category_name = video['category']['name']
                    pg_rating = video['pg_rating']['age']
                    category_id = video['category']['id']
                    author_id = video['author']['id']
                    title = video['title']
                    description = video['description']
                    created_ts = datetime.strptime(video ['created_ts'], "%Y-%m-%dT%H:%M:%S")
                    last_update_ts = datetime.strptime(video ['last_update_ts'], "%Y-%m-%dT%H:%M:%S")
                    hits = video['hits']
                    duration = video['duration']

                    async with get_session() as  session:
                        stmt = select(Video).where(Video.guid == guid)
                        res = await session.execute(stmt)
                        a = res.scalars().first()
                        if a:
                            continue
                        video = Video(
                            guid=guid,
                            video_url=video_url,
                            category_name=category_name,
                            pg_rating=pg_rating,
                            category_id=category_id,
                            autor_id=author_id,
                            title=title,
                            description=description,
                            created_at=created_ts,
                            updated_at=last_update_ts,
                            hits=hits,
                            duration=duration
                        )
                        session.add(video)
                await session.commit()

async def likes_dislikes():
    async with get_session() as  session:
        stmt = select(Video)
        res = await session.execute(stmt)
        videos = []
        for row in res.scalars():
            fin_url = VIDEO_LIKES_DISLIKES_API.format(row["video_url"])
            response = requests.get(fin_url).json()
            videos.append(
                Video(
                    lkes = response["positive"],
                    dislikes = response["negative"]
                )
            )
        session.update(videos)
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

if __name__ == '__main__':
    date = 12042024
    loop = asyncio.get_event_loop()
    # for cat in [8, 16, 67, 51]:
    #     for i in range(50):
            # loop.run_until_complete(get_videos_guids(cat, date, i))
    loop.run_until_complete(likes_dislikes())
    loop.close()

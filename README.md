# Парсилка Рутуба

## Команда Анаморфоза

Состав команды:

* Паламарчук Ярослав Владимирович - капитан
* Филиппенко Данил Романович
* Переверзев Егор Николаевич
* Чалый Кирилл Евгеньевич

Мы потеряли кучу времени на парсинг, пока не нашли внезапно открытые эндпоинты. Вот они:

```python
CATEGORIES_API = 'https://rutube.ru/api/video/category/'
VIDEOS_URLS_API = 'https://rutube.ru/api/video/category/{id}/{date}/'


VIDEO_API = 'https://rutube.ru/api/video/{}/'# guid/
COMMENTS_API = 'https://rutube.ru/api/comments/video/{}/'# guid/
AUTORS_API = 'https://rutube.ru/api/video/person/{}/'# id/

CHILD_COMMENTS_API = 'https://rutube.ru/api/comments/video/{}/?parent_id={}' # guid/ parent_id/

VOTE_API = 'https://rutube.ru/api/numerator/video/{}/vote'

VIDEO_LIKES_DISLIKES_API = "https://rutube.ru/api/numerator/video/{}/vote"
```

Более того, мы нашли дизлайки !!!!!

Пример: [https://rutube.ru/api/numerator/video/7dbe8167b0d6bf6330840ebda6615aa4/vote]

Парсили в ручном режиме, не до мультипроцессинга было :(

Ml тоже приекрутить не успели, но нашли решение, которое лежит в файлике `models/ml.py`

## Sql - скриптики

```sql
-- Имена авторов и количество их видео
select a.name, count(v.id) as count_video
from 
"Video" as v
join
"Author" as a 
on 
v.autor_id = a.id
group by a.name
order by count_video desc;

-- Имена категорий и количество их видео
select c.name, count(v.id) as count_video
from 
"Video" as v
join
"Category" as c 
on 
v.category_id = c.id
group by c.name
order by count_video desc;

-- Имя видео, автор видео, просмотры, продолжительность видео. Где встречается слово "сво"
select 
	v.title, 
	a.name, 
	v.hits,
	v.duration 
from 
	"Video" as v
	join
	"Author" as a 
	on 
	v.autor_id = a.id
where 
	(LOWER(v.title) like '%сво%' 
	or LOWER(v.description) like '%сво%')
order by hits desc;


-- количества видео, в которых встречается слово "россия", для каждого жанра
select c.name, count(v.id) as count_video
from 
	"Video" as v
join
	"Category" as c
on 
	v.category_id = c.id
where 
	(LOWER(v.title) like '%россия%' 
	or LOWER(v.description) like '%россия%')
group by c.name
order by count_video desc 
;

-- Самый залайканный коммент
select text, like 
from "Comment"
order by like desc;
```
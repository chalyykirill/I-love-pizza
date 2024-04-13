def get_video_data(id):
    url_base = 'https://rutube.ru/api/video/'    
    video_url = url_base + video_id
    response = requests.get(video_url)
    
    if response.status_code == 200:
        full_data = response.json()
        full_data['allowed_territories'] = full_data['restrictions']['country']['allowed']
        full_data['disallowed_territories'] = full_data['restrictions']['country']['restricted']

    else:
        full_data = {'error': 'Failed to retrieve data', 'status_code': response.status_code, 'id': video_id}
    
    s = get_session()

    video = Video(guid=full_data['id'], 
                  video_url=video_url, 
                  title=full_data['title'],
                  description=full_data['description'],
                  duration=full_data['duration'],
                  hits=full_data['hits'])
    s.add(video)
    await s.commit()
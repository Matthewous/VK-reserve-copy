from dataclasses import dataclass
import requests
from pprint import pprint


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_profile_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended':1}
        response = requests.get(url, params={**self.params, **params}).json()
        response = response['response']['items']

        photos_list = []

        for photo_info in response:
            likes = photo_info['likes']['count']
            date = photo_info['date']
            # print(likes)
            sizes = photo_info['sizes']
            photo = sizes[-1]
            del(photo['height'])
            del(photo['width'])

            if likes not in photo.values():
                photo['name'] = f"{self.id}/{likes}.jpg"
            else:
                photo['name'] = f"{self.id}/{likes}/{date}.jpg"

            photos_list.append(photo)
            pprint(photos_list)
        return photos_list


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, url, path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"url": url, "path": path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()


    def upload_file_to_disk(self, url, path):
        href = self._get_upload_link(url = url, path = path).get("href", "")
        response = requests.post(href)
        response.raise_for_status()
        if response.status_code == 201 or 202:
            print("File uploded successfully")




access_token = ''
user_id = '28357841'
vk = VK(access_token, user_id)
ya = YandexDisk(token="")

list = vk.get_profile_photos() # получение списка с фотографиями для закгрузки


for photo in list:
    url = photo['url']
    filename = photo['name']
    ya.upload_file_to_disk(url, filename)




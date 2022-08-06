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
        params = {'owner_id': self.id, 'album_id': 'profile'}
        response = requests.get(url, params={**self.params, **params}).json()
        response = response['response']['items']

        photos_list = []

        for photo_info in response:
            sizes = photo_info['sizes']
            photo = sizes[-1]
            del(photo['height'])
            del(photo['width'])
            # pprint(sizes[-1])
            photos_list.append(photo)

        return photos_list

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


if __name__ == '__main__':
    access_token = 'vk1.a.ibbE-OL4k0Q-5qS0VyvnzJcpD9tn6IPh1j-fpYgG0WmM9CkGOMGIy12RFkK3nP1zV4dCmzUcVa6-8HxdRdDNHBrdZRi86kFeGfeYU2gisZq3mlaCSxwpfbm5tPISCFhrMg7wCyDjTjZhlxG8O3fC9XvyOJqZUL707CP16jBdztHfkA0D0CzFsRhFcXKujLzc'
    user_id = '28357841'
    vk = VK(access_token, user_id)
    ya = YandexDisk(token="AQAAAABAMm1eAADLW6b9S6DeTEqPnuTnyrveYOA")
    vk.get_profile_photos()
    ya.upload_file_to_disk("test", "test.txt")



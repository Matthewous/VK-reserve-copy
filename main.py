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

        for photo_info in response:
            sizes = photo_info['sizes']
            photo = sizes[-1]
            del(photo['height'])
            del(photo['width'])
            pprint(sizes[-1])

        return 




access_token = 'vk1.a.ibbE-OL4k0Q-5qS0VyvnzJcpD9tn6IPh1j-fpYgG0WmM9CkGOMGIy12RFkK3nP1zV4dCmzUcVa6-8HxdRdDNHBrdZRi86kFeGfeYU2gisZq3mlaCSxwpfbm5tPISCFhrMg7wCyDjTjZhlxG8O3fC9XvyOJqZUL707CP16jBdztHfkA0D0CzFsRhFcXKujLzc'
user_id = '28357841'
vk = VK(access_token, user_id)
# vk.get_profile_photos()
pprint(vk.get_profile_photos())
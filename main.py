import requests
from pprint import pprint
import os

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
        # pprint(response)

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
                photo['name'] = "{}{}".format(likes, '.jpg')
            else:
                photo['name'] = "{}{}{}".format(likes, date, '.jpg')

            photos_list.append(photo)
            pprint(photos_list)
        return photos_list

    def saving_photos(self, photos_list):
        for photos in photos_list:
            saved_photo = requests.get(photos['url'])
            file = open(photos['name'], "wb")
            file.write(saved_photo.content)
            file.close()
        return 'success'
        
        

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, url, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"url": url, "path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def delete_photo(self, filename):
        os.remove(filename)
        return "file deleted successfully"

    def upload_file_to_disk(self, url, disk_file_path, filename):
        href = self._get_upload_link(url = url, disk_file_path = disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("File uploded successfully")
            ya.delete_photo(self, filename = filename)



if __name__ == '__main__':
    access_token = 'vk1.a.ZjkyK3CWlLayW6w85jrr_3K8Vy6DE660eVjR0MStPbfBzYZtdaZqWuuSRqWqdTiZZbV2pGC6gtQtEfzYsVIfMY8w2qm7oTsFYzvtB1lrqxXNHWn_JK7hoVVMc84tiFf-4XWMH2_3UHWwirzZsIO9uNAWp0NxRbRh06TQ8f4oX7bSdbgutDmpw4RpzZFkmkmT'
    user_id = '28357841'
    vk = VK(access_token, user_id)
    ya = YandexDisk(token="AQAAAABAMm1eAADLW6b9S6DeTEqPnuTnyrveYOA")
    # vk.get_profile_photos()
    # ya.upload_file_to_disk(url, path, path)
    # vk.get_profile_photos()
    # vk.saving_photos(vk.get_profile_photos())
    # ya.upload_file_to_disk()
    
    

    list = vk.get_profile_photos()
    vk.saving_photos(list)
    for photo in list:
        url = photo['url']
        disk_file_path = photo['name']
        filename = photo['name']
        ya.upload_file_to_disk(url, disk_file_path, filename)


    # https://oauth.vk.com/blank.html#access_token=vk1.a.ZjkyK3CWlLayW6w85jrr_3K8Vy6DE660eVjR0MStPbfBzYZtdaZqWuuSRqWqdTiZZbV2pGC6gtQtEfzYsVIfMY8w2qm7oTsFYzvtB1lrqxXNHWn_JK7hoVVMc84tiFf-4XWMH2_3UHWwirzZsIO9uNAWp0NxRbRh06TQ8f4oX7bSdbgutDmpw4RpzZFkmkmT&expires_in=86400&user_id=28357841&state=123456
    # https://cloud-api.yandex.net/v1/disk/resources/upload?url=https://sun9-45.userapi.com/impf/c626123/v626123841/1ed25/nrgwpEDKROc.jpg?size=498x751&quality=96&sign=dacc5e0e0f0b1eaf47352d0bbe589905&c_uniq_tag=a9O98Tk200T8XsftcbUnREiN2WemHy7ayZXm0-BTqFA&type=album&
    # access_token = 'vk1.a.ibbE-OL4k0Q-5qS0VyvnzJcpD9tn6IPh1j-fpYgG0WmM9CkGOMGIy12RFkK3nP1zV4dCmzUcVa6-8HxdRdDNHBrdZRi86kFeGfeYU2gisZq3mlaCSxwpfbm5tPISCFhrMg7wCyDjTjZhlxG8O3fC9XvyOJqZUL707CP16jBdztHfkA0D0CzFsRhFcXKujLzc'
    # url = 'https://sun9-45.userapi.com/impf/c626123/v626123841/1ed25/nrgwpEDKROc.jpg?size=498x751&quality=96&sign=dacc5e0e0f0b1eaf47352d0bbe589905&c_uniq_tag=a9O98Tk200T8XsftcbUnREiN2WemHy7ayZXm0-BTqFA&type=album'
    # path = 'Photo/nrgwpEDKROc.jpg'
   

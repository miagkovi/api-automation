from abc import ABC, abstractmethod
import requests
import configparser


class Configer:
    @staticmethod
    def get_url():
        config = configparser.ConfigParser()
        config.read('configs/environments.ini')
        return config['dev']['url']


class AppInterface(ABC):
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def post_data(self):
        pass

    @abstractmethod
    def put_data(self):
        pass

    @abstractmethod
    def patch_data(self):
        pass

    @abstractmethod
    def delete_data(self):
        pass


class App(AppInterface):
    _url = Configer.get_url()

    def get_data(self, endpoint):
        url = self._url + endpoint
        return requests.get(url)

    def post_data(self, endpoint, data):
        url = self._url + endpoint
        return requests.post(url, data=data)

    def put_data(self, endpoint, data):
        url = self._url + endpoint
        return requests.put(url, data=data)

    def patch_data(self, endpoint, data):
        url = self._url + endpoint
        return requests.patch(url, data=data)

    def delete_data(self, endpoint):
        url = self._url + endpoint
        return requests.delete(url)

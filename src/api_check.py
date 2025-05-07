from abc import ABC, abstractmethod
import requests
from typing import List, Dict, Any


class BaseHeadHunterAPI(ABC):
    """
    Абстрактный базовый класс для подключения к API.
    """

    @abstractmethod
    def get_vacancies(self, keyword: str, page: int) -> List[Dict[str, Any]]:
        """
        Абстрактный метод получения списка вакансий с API.

        :param keyword: Ключевое слово для поиска вакансий.
        :param page: Количество страниц, которые нужно обработать.
        :return: Список словарей с вакансиями.
        """
        pass

    @abstractmethod
    def connect_api(self) -> None:
        """Метод проверки подключения к API."""
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    """
    Класс для работы с API HeadHunter.
    Позволяет подключиться к API и получать список вакансий по ключевому слову.
    """
    BASE_URL = 'https://api.hh.ru'

    def __init__(self) -> None:
        """Инициализирует параметры подключения и хранилище вакансий."""
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.vacancies: List[Dict[str, Any]] = []

    def connect_api(self) -> str:
        """Проверяет подключение к API hh.ru."""
        temp_response = requests.get(self.BASE_URL, params={'text': ""})
        status_code = temp_response.status_code
        if status_code == 200:
            print("Подключение к hh.ru установлено")
        else:
            raise Exception(f"Проблемы с подключением к hh.ru, status_code = {status_code}")

    def get_vacancies(self, keyword: str, page: int = 2) -> List[Dict[str, Any]]:
        """
        Получает вакансии с hh.ru по заданному ключевому слову.

        :param keyword: Ключевое слово для поиска.
        :param page: Количество страниц, которые нужно загрузить (по 5 вакансий на страницу).
        :return: Список найденных вакансий.
        """
        params = {'text': keyword, 'page': 0, 'per_page': 5, 'area': 1}

        while params.get('page') != page:
            response = requests.get(f"{self.BASE_URL}/vacancies", headers=self.__headers, params=params)
            if response.status_code == 200:
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                params['page'] += 1
        return self.vacancies

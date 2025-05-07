from abc import ABC, abstractmethod
import json
from typing import List

from src.vacancy_module import Vacancy


class WorkIsFile(ABC):
    """
    Абстрактный базовый класс для работы с файлами вакансий.
    """

    @abstractmethod
    def save_file(self, vacancies: List[Vacancy]) -> None:
        """
        Абстрактный метод для сохранения списка вакансий в файл.

        :param vacancies: Список объектов вакансий
        """
        pass


class FileChange(WorkIsFile):
    """
    Класс для чтения, записи и обновления файла с вакансиями.
    """

    def __init__(self, file_name: str = "user_vacancies.json") -> None:
        """
        Инициализация объекта FileChange, загрузка данных из файла.

        :param file_name: Название JSON-файла с вакансиями.
        """
        self.__file_name = file_name
        self.data_file: List[dict] = []
        self.load_vacancies_from_file()

    def save_file(self, vacancies: List[Vacancy]) -> None:
        """
        Сохраняет вакансии в файл, проверяя на уникальность по URL.

        :param vacancies: Список объектов вакансий.
        """
        temp_list = [vacancy.to_dict() for vacancy in vacancies]
        temp_url = [data["url"] for data in self.data_file]
        if len(self.data_file) > 0:
            list_uniq = [temp_vacancy for temp_vacancy in temp_list if temp_vacancy["url"] not in temp_url]
            self.data_file.extend(list_uniq)
        else:
            self.data_file.extend(temp_list)
        self.save_file_uniq(self.data_file)

    def save_file_uniq(self, vacancies: List[dict]) -> None:
        """
        Перезаписывает файл с вакансиями, сохраняя переданный список.

        :param vacancies: Список вакансий в виде словарей.
        """
        with open("data/{0}".format(self.__file_name), "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)
        print("Файл успешно записан.")

    def load_vacancies_from_file(self) -> List[dict]:
        """
        Загружает вакансии из файла в атрибут `data_file`.

        :return: Список вакансий из файла или пустой список при ошибке.
        """
        try:
            with open("data/{0}".format(self.__file_name), "r", encoding="utf-8") as f:
                self.data_file = json.load(f)
                temp_data_file = self.data_file
                return temp_data_file
        except FileNotFoundError:
            print("Файл не найден. Создайте файл с вакансиями.")
            return []
        except json.JSONDecodeError:
            print("Ошибка при чтении файла.")
            return []

    def del_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из списка по совпадению URL и перезаписывает файл.

        :param vacancy: Объект вакансии для удаления.
        """
        for i, data in enumerate(self.data_file):
            if data["alternate_url"] == vacancy.url:
                del self.data_file[i]
                break
        self.save_file_uniq(self.data_file)

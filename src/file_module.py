import json
import os
from abc import ABC, abstractmethod
from typing import List

from src.vacancy_module import Vacancy


class WorkIsFile(ABC):
    """
    Абстрактный базовый класс для работы с файлами вакансий.
    """

    @abstractmethod
    def save_file(self, vacancies: List[Vacancy]) -> None:
        """Сохранение списка вакансий в файл"""
        pass

    @abstractmethod
    def write(self, text: list[dict], file_mode: str) -> None:
        """Запись данных в файл"""
        pass

    @abstractmethod
    def open_file(self) -> None:
        """Открытие файла"""
        pass

    @abstractmethod
    def load_vacancies_from_file(self) -> List[dict]:
        """Загрузка данных из файла"""
        pass

    @abstractmethod
    def add_vacancy(self, list_vacancy_hh: list[Vacancy]) -> None:
        """Добавление новой вакансии"""
        pass

    @abstractmethod
    def del_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии (по alternate_url)"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии (по id_vacancy)"""
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

        def open_file(self) -> None:
            """Метод открытия файла"""
            if os.path.exists(self.__filename):
                with open(self.__filename, mode="r", encoding="utf-8") as file:
                    self.data_file = json.load(file)
            else:
                with open(self.__filename, mode="a", encoding="utf-8"):
                    pass

        def write(self, text: list[dict], file_mode: str) -> None:
            """Запись в файл"""
            with open(self.__filename, mode=file_mode, encoding="utf-8") as file:
                file.write(json.dumps(text, ensure_ascii=False, indent=4))
            self.data_file = text

        def add_vacancy(self, list_vacancy_hh: list[Vacancy]) -> None:
            """Метод добавления в файл новых вакансий"""
            list_ids = [values["id_vacancy"] for values in self.data_file]
            list_vacancy = [vacancy.to_dict() for vacancy in list_vacancy_hh if vacancy.requirement not in list_ids]
            self.write(list_vacancy, "a")

        def delete_vacancy(self, vacancy: Vacancy) -> None:
            """Удаление вакансии"""
            for index, data in enumerate(self.data_file):
                if data["id_vacancy"] == vacancy.id_vacancy:
                    del self.data_file[index]
                    break
            self.write(self.data_file, "w")

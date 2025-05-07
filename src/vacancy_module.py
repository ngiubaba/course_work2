from typing import List, Dict, Any, Optional


class Vacancy:
    """
    Класс для представления вакансии с основными полями: название, ссылка, зарплата и обязанности.
    """

    def __init__(self, name: str, url: str, responsibility: str, salary: Optional[Dict[str, Any]]) -> None:
        """
        Инициализирует объект вакансии и валидирует входные данные.

        :param name: Название вакансии.
        :param url: Ссылка на вакансию.
        :param responsibility: Обязанности по вакансии.
        :param salary: Словарь с данными по зарплате.
        """
        self.name = Vacancy._validate_name(name)
        self.url = Vacancy._validate_url(url)
        self.salary_from: Any = "Не указана"
        self.salary_to: Any = "Не указана"
        self.responsibility = Vacancy._validate_responsibility(responsibility)
        self._validate_salary(salary)

    @staticmethod
    def _validate_name(name: str) -> str:
        """
        Валидирует название вакансии.

        :param name: Название вакансии.
        :return: Название, если оно корректное.
        :raises ValueError: Если значение некорректное.
        """
        if isinstance(name, str) and len(name) > 0:
            return name
        raise ValueError("Ожидался str name")

    def _validate_salary(self, salary: Optional[Dict[str, Any]]) -> Optional[tuple]:
        """
        Валидирует и устанавливает значения зарплаты из словаря.

        :param salary: Словарь с ключами 'from' и 'to'.
        :return: Кортеж (salary_to, salary_from) если данные заданы.
        """
        if isinstance(salary, dict) and len(salary) > 0:
            self.salary_from = salary.get("from") if salary.get("from") else "Не указана"
            self.salary_to = salary.get("to") if salary.get("to") else "Не указана"
            return self.salary_to, self.salary_from

    @staticmethod
    def _validate_url(url: str) -> str:
        """
        Валидирует URL вакансии.

        :param url: Ссылка на вакансию.
        :return: URL, если он корректный.
        :raises ValueError: Если значение некорректное.
        """
        if isinstance(url, str) and len(url) > 0:
            return url
        raise ValueError("Ожидался str url")

    @staticmethod
    def _validate_responsibility(responsibility: str) -> str:
        """
        Валидирует описание обязанностей.

        :param responsibility: Строка с обязанностями.
        :return: Строка, если корректна.
        :raises ValueError: Если значение некорректное.
        """
        if isinstance(responsibility, str) and len(responsibility) > 0:
            return responsibility
        raise ValueError("Ожидался str responsibility")

    @classmethod
    def dict_to_list_vacancy(cls, vacancies: List[Dict[str, Any]]) -> List["Vacancy"]:
        """
        Преобразует список словарей в список объектов класса Vacancy.

        :param vacancies: Список словарей, полученных из API.
        :return: Список объектов Vacancy.
        """
        filtered_vacancies = []
        for vacancy in vacancies:
            snippet = vacancy['snippet'] if vacancy.get('snippet') else {}
            responsibility = snippet.get('responsibility', "Нет описания")
            filtered_vacancies.append(cls(
                name=vacancy.get("name"),
                url=vacancy.get("alternate_url"),
                salary=vacancy.get("salary"),
                responsibility=responsibility
            ))
        return filtered_vacancies

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект Vacancy в словарь.

        :return: Словарь с данными по вакансии.
        """
        return {
            "name": self.name,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "responsibility": self.responsibility,
        }

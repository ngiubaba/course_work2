import pytest
from src.vacancy_module import Vacancy


def test_vacancy_creation_valid():
    """
    Тестирует создание объекта Vacancy с валидными данными.
    Проверяется, что все атрибуты вакансии корректно инициализируются.
    """
    salary = {"from": 50000, "to": 70000}
    vacancy = Vacancy(name="Software Engineer", url="https://example.com",
                      responsibility="Develop software using Python.", salary=salary)

    assert vacancy.name == "Software Engineer"
    assert vacancy.url == "https://example.com"
    assert vacancy.salary_from == 50000
    assert vacancy.salary_to == 70000
    assert vacancy.responsibility == "Develop software using Python."


def test_vacancy_creation_invalid_name():
    """
    Тестирует создание объекта Vacancy с некорректным значением имени.
    Ожидается выброс исключения ValueError с соответствующим сообщением.
    """
    with pytest.raises(ValueError, match="Ожидался str name"):
        Vacancy(name="", url="https://example.com", responsibility="Develop software using Python.",
                salary={"from": 50000, "to": 70000})


def test_vacancy_creation_invalid_url():
    """
    Тестирует создание объекта Vacancy с некорректным URL.
    Ожидается выброс исключения ValueError с соответствующим сообщением.
    """
    with pytest.raises(ValueError, match="Ожидался str url"):
        Vacancy(name="Software Engineer", url="", responsibility="Develop software using Python.",
                salary={"from": 50000, "to": 70000})


def test_vacancy_creation_invalid_responsibility():
    """
    Тестирует создание объекта Vacancy с некорректным описанием обязанностей.
    Ожидается выброс исключения ValueError с соответствующим сообщением.
    """
    with pytest.raises(ValueError, match="Ожидался str responsibility"):
        Vacancy(name="Software Engineer", url="https://example.com", responsibility="",
                salary={"from": 50000, "to": 70000})


def test_vacancy_creation_no_salary():
    """
    Тестирует создание объекта Vacancy без указания зарплаты.
    Ожидается, что зарплата будет установлена как "Не указана".
    """
    vacancy = Vacancy(name="Software Engineer", url="https://example.com",
                      responsibility="Develop software using Python.", salary={})
    assert vacancy.salary_from == "Не указана"
    assert vacancy.salary_to == "Не указана"


def test_dict_to_list_vacancy():
    """
    Тестирует метод dict_to_list_vacancy, который преобразует список словарей в список объектов Vacancy.
    Проверяется, что объекты Vacancy правильно создаются на основе данных в словарях.
    """
    vacancies_dict = [
        {
            "name": "Software Engineer",
            "alternate_url": "https://example.com/1",
            "salary": {"from": 50000, "to": 70000},
            "snippet": {"responsibility": "Develop software using Python."}
        },
        {
            "name": "Data Scientist",
            "alternate_url": "https://example.com/2",
            "salary": {"from": 60000, "to": 90000},
            "snippet": {"responsibility": "Analyze data using Python."}
        }
    ]

    vacancies = Vacancy.dict_to_list_vacancy(vacancies_dict)

    assert len(vacancies) == 2
    assert vacancies[0].name == "Software Engineer"
    assert vacancies[0].url == "https://example.com/1"
    assert vacancies[0].salary_from == 50000
    assert vacancies[0].salary_to == 70000
    assert vacancies[0].responsibility == "Develop software using Python."


def test_vacancy_to_dict():
    """
    Тестирует метод to_dict, который преобразует объект Vacancy в словарь.
    Проверяется, что все атрибуты объекта корректно преобразуются в словарь.
    """
    salary = {"from": 50000, "to": 70000}
    vacancy = Vacancy(name="Software Engineer", url="https://example.com",
                      responsibility="Develop software using Python.", salary=salary)

    vacancy_dict = vacancy.to_dict()
    assert vacancy_dict["name"] == "Software Engineer"
    assert vacancy_dict["url"] == "https://example.com"
    assert vacancy_dict["salary_from"] == 50000
    assert vacancy_dict["salary_to"] == 70000
    assert vacancy_dict["responsibility"] == "Develop software using Python."

from typing import Any

from src.user_iteration import filter_vacancies, get_top_vacancies, get_vacancies_by_salary


def test_filter_vacancies() -> None:
    """
    Тестирует функцию filter_vacancies, которая фильтрует вакансии по ключевым словам в описании обязанностей.
    Проверяется, что вакансии с нужными ключевыми словами присутствуют в отфильтрованном списке.
    """
    vacancies = [
        {
            "name": "Software Engineer",
            "url": "https://example.com/1",
            "salary_from": 50000,
            "salary_to": 70000,
            "responsibility": "Develop software using Python.",
        },
        {
            "name": "Data Scientist",
            "url": "https://example.com/2",
            "salary_from": 60000,
            "salary_to": 90000,
            "responsibility": "Analyze data using Python.",
        },
        {
            "name": "Web Developer",
            "url": "https://example.com/3",
            "salary_from": 40000,
            "salary_to": 60000,
            "responsibility": "Develop websites using JavaScript.",
        },
    ]
    keywords = ["python", "java"]

    # Фильтруем вакансии по ключевым словам
    filtered = filter_vacancies(vacancies, keywords)

    # Проверка, что все вакансии содержат хотя бы одно из ключевых слов
    assert len(filtered) == 3
    assert any("python" in v["responsibility"] for v in filtered)
    assert any("java" in v["responsibility"] for v in filtered)


def test_get_vacancies_by_salary() -> None:
    """
    Тестирует функцию get_vacancies_by_salary, которая фильтрует вакансии по заданному диапазону зарплат.
    Проверяется, что функция корректно фильтрует вакансии в пределах указанного диапазона.
    """
    vacancies = [
        {
            "name": "Software Engineer",
            "url": "https://example.com/1",
            "salary_from": 50000,
            "salary_to": 70000,
            "responsibility": "Develop software using Python.",
        },
        {
            "name": "Data Scientist",
            "url": "https://example.com/2",
            "salary_from": 60000,
            "salary_to": 90000,
            "responsibility": "Analyze data using Python.",
        },
        {
            "name": "Web Developer",
            "url": "https://example.com/3",
            "salary_from": 40000,
            "salary_to": 60000,
            "responsibility": "Develop websites using JavaScript.",
        },
    ]
    salary_range = "50000 - 80000"

    filtered_by_salary = get_vacancies_by_salary(vacancies, salary_range)
    assert len(filtered_by_salary) == 1
    assert all(v["salary_from"] >= 50000 and v["salary_to"] <= 80000 for v in filtered_by_salary)


def test_get_top_vacancies(capsys: Any) -> None:
    """
    Тестирует функцию get_top_vacancies, которая выводит топ-N вакансий из списка.
    Проверяется, что выводятся только топ-N вакансий, и что правильные вакансии отображаются в выводе.
    """
    vacancies = [
        {
            "name": "Software Engineer",
            "url": "https://example.com/1",
            "salary_from": 50000,
            "salary_to": 70000,
            "responsibility": "Develop software using Python.",
        },
        {
            "name": "Data Scientist",
            "url": "https://example.com/2",
            "salary_from": 60000,
            "salary_to": 90000,
            "responsibility": "Analyze data using Python.",
        },
        {
            "name": "Web Developer",
            "url": "https://example.com/3",
            "salary_from": 40000,
            "salary_to": 60000,
            "responsibility": "Develop websites using JavaScript.",
        },
    ]
    n = 2
    get_top_vacancies(vacancies, n)

    captured = capsys.readouterr()
    assert "Software Engineer" in captured.out
    assert "Data Scientist" in captured.out
    assert "Web Developer" not in captured.out

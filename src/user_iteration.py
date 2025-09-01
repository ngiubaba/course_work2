from typing import Dict, List


def filter_vacancies(list_vacancy: List[Dict], words: List[str]) -> List[Dict]:
    """
    Фильтрует список вакансий по ключевым словам в описании обязанностей.

    :param list_vacancy: Список словарей с вакансиями.
    :param words: Список ключевых слов для поиска в описании.
    :return: Отфильтрованный список вакансий, содержащих хотя бы одно ключевое слово.
    """
    filtered_vacancies = []
    for vacancy in list_vacancy:
        responsibility = vacancy.get("responsibility", "").lower()
        if any(word.lower() in responsibility for word in words):
            filtered_vacancies.append(
                {
                    "name": vacancy.get("name"),
                    "url": vacancy.get("url"),
                    "salary_from": vacancy.get("salary_from"),
                    "salary_to": vacancy.get("salary_to"),
                    "responsibility": responsibility,
                }
            )
    return filtered_vacancies


def get_vacancies_by_salary(list_vacancy: List[Dict], salary_range: str) -> List[Dict]:
    """
    Фильтрует вакансии по заданному диапазону зарплат.

    :param list_vacancy: Список словарей с вакансиями.
    :param salary_range: Диапазон зарплаты в формате "от - до".
    :return: Список вакансий, удовлетворяющих указанному диапазону.
    """
    salary_list = salary_range.split(" - ")
    user_salary_from = int(salary_list[0])
    user_salary_to = int(salary_list[1])
    salary_filtered_vacancies = []
    for vacancy in list_vacancy:
        salary_list_from = vacancy["salary_from"]
        salary_list_to = vacancy["salary_to"]
        if (isinstance(salary_list_from, int) and salary_list_from >= user_salary_from) and (
            isinstance(salary_list_to, int) and salary_list_to <= user_salary_to
        ):
            salary_filtered_vacancies.append(vacancy)
    return salary_filtered_vacancies


def get_top_vacancies(list_vacancy: List[Dict], n: int) -> None:
    """
    Выводит топ-N вакансий из списка.

    :param list_vacancy: Список словарей с вакансиями.
    :param n: Количество вакансий для вывода.
    """
    for vacancy in list_vacancy[:n]:
        print("🔹 Название:", vacancy.get("name"))
        print(f"💰 Зарплата от: {vacancy.get('salary_from')} до {vacancy.get('salary_to')}")
        print("🔗 Ссылка:", vacancy.get("url"))
        print("📝 Описание:", vacancy.get("responsibility"))
        print("-" * 50)

from src.api_check import HeadHunterAPI
from src.file_module import FileChange
from src.vacancy_module import Vacancy
from src.user_iteration import filter_vacancies, get_vacancies_by_salary, get_top_vacancies


# # Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
connect_test = hh_api.connect_api()
work_file = FileChange()


def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    list_dict_vacancy = hh_api.get_vacancies(search_query)

    list_vacancy = Vacancy.dict_to_list_vacancy(list_dict_vacancy)
    work_file.save_file(list_vacancy)

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
    vacancies_list = work_file.load_vacancies_from_file()
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    get_top_vacancies(ranged_vacancies, top_n)
    print("Программа завершена.")


if __name__ == "__main__":
    user_interaction()
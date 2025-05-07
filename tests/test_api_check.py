import pytest
from src.api_check import HeadHunterAPI


@pytest.fixture
def api_instance():
    """
    Фикстура для создания экземпляра класса HeadHunterAPI.
    """
    return HeadHunterAPI()


def test_connect_api_success(mocker, api_instance):
    """
    Тестирует успешное подключение к API. Проверяется, что метод connect_api
    не вызывает исключений при успешном ответе от сервера (status_code 200).
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch('requests.get', return_value=mock_response)

    assert api_instance.connect_api() is None


def test_connect_api_failure(mocker, api_instance):
    """
    Тестирует неудачное подключение к API. Проверяется, что метод connect_api
    вызывает исключение, если сервер возвращает ошибку (status_code 500).
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(Exception, match=r"Проблемы с подключением к hh\.ru"):
        api_instance.connect_api()


def test_get_vacancies(mocker, api_instance):
    """
    Тестирует метод получения вакансий с API. Проверяется, что метод get_vacancies
    корректно обрабатывает успешный ответ от сервера и возвращает список вакансий.
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"id": "1", "name": "Python Developer"},
            {"id": "2", "name": "Data Scientist"}
        ]
    }

    mocker.patch('requests.get', return_value=mock_response)

    result = api_instance.get_vacancies("python", page=1)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Python Developer"

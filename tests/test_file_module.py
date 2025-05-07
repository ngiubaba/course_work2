import json
import os
import pytest
from src.file_module import FileChange
from src.vacancy_module import Vacancy


@pytest.fixture
def sample_vacancy():
    """
    Фикстура для создания объекта вакансии для тестов.
    """
    return Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        responsibility="Разработка и поддержка",
        salary={"from": 100000, "to": 150000}
    )


@pytest.fixture
def temp_file(tmp_path):
    """
    Фикстура для создания временного файла для тестирования.
    """
    file_path = tmp_path / "test_vacancies.json"
    file_path.write_text("[]", encoding="utf-8")  # пустой json
    return file_path


@pytest.fixture
def file_change(temp_file):
    """
    Фикстура для создания экземпляра класса FileChange с временным файлом.
    """
    return FileChange(file_name=temp_file.name)


def test_save_and_load_file(file_change, sample_vacancy, tmp_path):
    """
    Тестирует сохранение вакансии в файл и последующую загрузку.
    Проверяется, что файл создается, и данные корректно сохраняются и загружаются.
    """
    file_change.save_file([sample_vacancy])
    file_path = os.path.join("data", file_change._FileChange__file_name)
    assert os.path.exists(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["url"] == sample_vacancy.url


def test_load_nonexistent_file(monkeypatch):
    """
    Тестирует загрузку несуществующего файла.
    Проверяется, что при отсутствии файла возвращается пустой список.
    """
    fc = FileChange(file_name="nonexistent.json")
    monkeypatch.setattr("builtins.print", lambda msg: None)  # подавим вывод
    fc.__file_name = "nonexistent.json"
    assert fc.load_vacancies_from_file() == []


def test_save_file_does_not_duplicate(file_change, sample_vacancy):
    """
    Тестирует, что при сохранении одной и той же вакансии несколько раз, она не дублируется в файле.
    """
    file_change.save_file([sample_vacancy])
    count_after_first = len(file_change.data_file)

    file_change.save_file([sample_vacancy])
    count_after_second = len(file_change.data_file)

    assert count_after_first == count_after_second

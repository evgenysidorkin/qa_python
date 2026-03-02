import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        assert len(collector.get_books_genre()) == 2

    # проверка добавления книги с невалидными колличеством символов
    @pytest.mark.parametrize( 
        'name',
        ['', 'Что делать, если ваш кот хочет вас убить?'] 
    )
    def test_add_new_book_with_invalid_name_not_added(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        
        assert len(collector.get_books_genre()) == 0   
    
    # проверка что у добавленной книги нет жанра
    def test_add_new_book_initial_genre_is_empty(self):
        
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        
        books_genre = collector.get_book_genre('Гордость и предубеждение и зомби')
    
        assert books_genre == ''

    # проверка установки жанра 
    def test_set_book_genre_changes_genre_of_existing_book(self):
        
        collector = BooksCollector()
    
        collector.add_new_book('Гордость и предубеждение и зомби')  
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
    
        books_genre = collector.get_book_genre('Гордость и предубеждение и зомби')
    
        assert books_genre == 'Ужасы'

    # проверка получения списка книг определенного жанра
    def test_get_books_with_specific_genre_returns_list_of_books_with_that_genre(self):
        
        collector = BooksCollector()
    
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Кладбище домашних животных')

        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Кладбище домашних животных', 'Ужасы')
    
        book_list = collector.get_books_with_specific_genre('Ужасы')
    
        assert book_list == ['Гордость и предубеждение и зомби', 'Кладбище домашних животных']

    # проверка что книги жанра "Ужасы" не попадают в детские
    def test_get_books_for_children_does_not_include_horror_books(self):
        
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Три кота и море приключений')

        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Три кота и море приключений', 'Мультфильмы')

        children_books = collector.get_books_for_children()

        assert 'Три кота и море приключений' in children_books and 'Гордость и предубеждение и зомби' not in children_books
        
    
    # проверка успешного добавления существующей книги в избранное
    def test_add_book_in_favorites_successfully_adds_book(self):

        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Кладбище домашних животных')
    
        collector.add_book_in_favorites('Гордость и предубеждение и зомби')

        favorites = collector.get_list_of_favorites_books()
       
        assert 'Гордость и предубеждение и зомби' in favorites and len(favorites) == 1

    # проверка успешного удаления книги из избранного
    def test_delete_book_from_favorites_successfully_removes_book(self):

        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Кладбище домашних животных')
    
        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector.add_book_in_favorites('Кладбище домашних животных')

        collector.delete_book_from_favorites('Кладбище домашних животных')

        favorites = collector.get_list_of_favorites_books()
       
        assert 'Гордость и предубеждение и зомби' in favorites and len(favorites) == 1

    
    # проверка возврата полного словаря книг
    def test_get_books_genre_returns_complete_dict(self):

        collector = BooksCollector()

        books = {
        'О дивный новый мир': 'Фантастика',
        'Кладбище домашних животных': 'Ужасы',
        'Безмолвный пациент': 'Детективы',
        'Три кота и море приключений': 'Мультфильмы',
        'Трое в лодке, не считая собаки': 'Комедии'
        }

        for name, genre in books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        assert collector.get_books_genre() == books


    # проверка получения жанра книги по её имени
    @pytest.mark.parametrize(
            'book_name, expected_genre', [
                ['О дивный новый мир', 'Фантастика'],
                ['Кладбище домашних животных', 'Ужасы'],
                ['Безмолвный пациент', 'Детективы'],
                ['Три кота и море приключений', 'Мультфильмы'],
                ['Трое в лодке, не считая собаки', 'Комедии']                
                ])
    def test_get_book_genre_for_existing_book_returns_its_genre(self, book_name, expected_genre):
        collector = BooksCollector()
    
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, expected_genre)
    
        assert collector.get_book_genre(book_name) == expected_genre


    # проверка получения списка избранных книг
    def test_get_list_of_favorites_books_returns_list_with_multiple_books(self):

        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Кладбище домашних животных')
        collector.add_new_book('Трое в лодке, не считая собаки')

    
        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector.add_book_in_favorites('Кладбище домашних животных')
        collector.add_book_in_favorites('Трое в лодке, не считая собаки')

        favorites = collector.get_list_of_favorites_books()
       
        assert favorites == ['Гордость и предубеждение и зомби', 'Кладбище домашних животных', 'Трое в лодке, не считая собаки'] and len(favorites) == 3    

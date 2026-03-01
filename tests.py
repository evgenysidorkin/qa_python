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
    @pytest.mark.parametrize(
        'genre, expected_books', [
        ('Ужасы', ['Гордость и предубеждение и зомби', 'Кладбище домашних животных']),
        ('Комедии', [])
    ]
    )
    def test_get_books_with_specific_genre_returns_list_of_books_with_that_genre(self, genre, expected_books):

        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Кладбище домашних животных')
    
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Кладбище домашних животных', 'Ужасы')
        
        book_list = collector.get_books_with_specific_genre(genre)

        assert book_list == expected_books

    # проверка что книги жанра "Ужасы" не попадают в детские
    def test_get_books_for_children_does_not_include_horror_books(self):
        
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Красная шапочка')

        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Красная шапочка', 'Мультфильмы')

        children_books = collector.get_books_for_children()

        assert 'Красная шапочка' in children_books and 'Гордость и предубеждение и зомби' not in children_books
        
    
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

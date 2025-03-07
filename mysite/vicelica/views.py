from django.shortcuts import render, redirect
import random


# Вспомогательные функции
def get_dictionary_word_list():
    """Возвращает случайное слово из словаря."""
    with open('russian.txt') as f:
        return random.choice(f.read().split())


def initialize_secret_word(word):
    """Инициализирует секретное слово с заменой всех букв на '_', кроме символа '-'."""
    secret_letters = ['-' if char == '-' else '_' for char in word]
    return secret_letters


def check_letter_in_word(letter, word, secret_letters):
    """Проверяет наличие буквы в слове и обновляет секретное слово."""
    match_count = 0
    if len(letter) != 1:
        return 'invalid_input'

    for i, char in enumerate(word):
        if letter == secret_letters[i]:
            return 'duplicate'
        elif letter == char:
            secret_letters[i] = char
            match_count += 1

    return match_count


# Основное представление игры
def vicelica_game(request):
    # Проверка выбора режима игры
    if request.method == "POST":
        # Если режим игры не выбран, обрабатываем выбор режима
        if 'choice' not in request.session:
            choice = request.POST.get('choice').lower()
            if choice in ["standart", "premium"]:
                # Сохраняем выбор режима игры в сессии
                request.session['choice'] = choice

                # Инициализация игры в зависимости от режима
                if choice == "standart":
                    word_before_cut = get_dictionary_word_list()
                else:
                    word_before_cut = 'паша-дотер-бегемотер'

                # Инициализация игры
                secret_letters = initialize_secret_word(word_before_cut)
                request.session['word'] = list(word_before_cut)
                request.session['secret_letters'] = secret_letters
                request.session['attempts_left'] = 10
                request.session['incorrect_letters'] = []  # Инициализация списка неправильных букв

            else:
                message = "Некорректный режим игры. Попробуйте снова."
                return render(request, 'vicelica/game.html', {
                    'message': message,
                })

        # Логика обработки ввода буквы
        elif 'letter' in request.POST:
            letter = request.POST.get("letter").lower()
            if not letter:
                message = "Вы не ввели букву."
                return render(request, 'vicelica/game.html', {
                    'secret_letters': " ".join(request.session.get('secret_letters', [])),
                    'attempts_left': request.session.get('attempts_left', 6),
                    'message': message,
                })

            word = list(request.session.get("word"))
            secret_letters = request.session.get("secret_letters")
            attempts_left = request.session.get("attempts_left")
            incorrect_letters = request.session.get("incorrect_letters", [])

            # Проверка на ранее введённые буквы
            if letter in incorrect_letters or letter in secret_letters:
                message = 'Вы уже вводили эту букву.'
            else:
                result = check_letter_in_word(letter, word, secret_letters)

                if result == 'duplicate':
                    message = 'Вы уже вводили эту букву.'
                elif result == 'invalid_input':
                    message = 'Нужно ввести букву.'
                elif result > 0:
                    message = f'Вы угадали {"букву" if result == 1 else "несколько букв"}!'
                else:
                    # Обработка неправильной буквы
                    if letter not in incorrect_letters:
                        incorrect_letters.append(letter)
                        attempts_left -= 1
                    message = f'Вы не угадали букву. У вас осталось {attempts_left} попыток.'

                # Обновление данных сессии
                request.session['secret_letters'] = secret_letters
                request.session['attempts_left'] = attempts_left
                request.session['incorrect_letters'] = incorrect_letters

                # Проверка на победу или проигрыш
                if secret_letters == word:
                    request.session.flush()
                    return render(request, 'vicelica/win.html', {'word': "".join(word)})

                if attempts_left <= 0:
                    request.session.flush()
                    return render(request, 'vicelica/lose.html', {'word': "".join(word)})

            return render(request, 'vicelica/game.html', {
                'secret_letters': " ".join(secret_letters),
                'attempts_left': attempts_left,
                'message': message,
            })

    # Начало игры (GET-запрос)
    if 'choice' not in request.session:
        return render(request, 'vicelica/game.html')  # Отображаем форму выбора режима игры

    # Отображаем текущее состояние игры, если режим уже выбран
    return render(request, 'vicelica/game.html', {
        'secret_letters': " ".join(request.session.get('secret_letters', [])),
        'attempts_left': request.session.get('attempts_left', 6),
    })

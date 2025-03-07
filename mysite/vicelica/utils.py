import random


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

    if len(letter) != 1 or len(letter) == 0:
        print('Нужно ввести одну букву.')
        return 'invalid_input'

    for i, char in enumerate(word):
        if letter == secret_letters[i]:
            return 'duplicate'
        elif letter == char:
            secret_letters[i] = char
            match_count += 1

    return match_count


def play_vicelica(word):
    """Основная логика игры."""
    secret_letters = initialize_secret_word(word)
    attempts_left = 6

    while attempts_left > 0:
        print(' '.join(secret_letters))

        if secret_letters == word:
            print(f'Вы победили! Загаданное слово: {"".join(word)}')
            return

        letter = input('Введите букву: ').strip().lower()
        result = check_letter_in_word(letter, word, secret_letters)

        if result == 'duplicate':
            print('Вы уже вводили эту букву.')
        elif result == 'invalid_input':
            continue
        elif result > 0:
            print(f'Вы угадали {"букву" if result == 1 else "несколько букв"}!')
        else:
            attempts_left -= 1
            print(f'Вы не угадали букву. У вас осталось {attempts_left} попыток.')

    print(f'Вы проиграли. Загаданное слово было: {"".join(word)}')


# Основной блок выполнения
def main():
    simple_or_special = input('Введите в какую часть игры вы хотите сыграть:\n'
                              'simple - если в обычную\n'
                              'special - если в необычную\n'
                              'Ну так в какую: ').strip().lower()

    if simple_or_special == 'simple':
        word_before_cut = get_dictionary_word_list()
    elif simple_or_special == 'special':
        word_before_cut = 'паша-дотер-бегемотер'
    else:
        print('Не дури мне головы')
        return

    play_vicelica(list(word_before_cut))


if __name__ == '__main__':
    main()

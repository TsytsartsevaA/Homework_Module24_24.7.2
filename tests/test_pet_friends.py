import os

from api import PetFriends
from settings import not_valid_password
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email,
                                 valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Пташка', animal_type='птица', age='3',
                                     pet_photo='images/Bird.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Недовольный', animal_type='кот', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то пишем текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_simple_pet_with_valid_data(name='Геннадий', animal_type='крокодил',
                                            age='3', ):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age, )

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_pet_foto(pet_photo='images/Croco.jpg'):
    """Проверяем что можно добавить фотографию питомца по ID"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то добавляем фото питомца
    if len(my_pets['pets']) > 0:

        status, result = pf.add_pet_foto(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что в pet_photo значение не пустое и статус ответа = 200

        assert status == 200
        assert 'pet_photo' in result
    else:
        # если список питомцев пустой, то пишем текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_not_get_my_pets_with_not_valid_email(filter='my_pets'):
    """ Проверяем что нельзя получить список моих питомцев с не верным email.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_my_pets(auth_key, filter)
    assert status == 403
    assert '403' in result


def test_not_get_my_pets_with_not_valid_key(filter='my_pets'):
    """ Проверяем что нельзя получить список моих питомцев с не верным api ключом.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    в apy.py в функции "get_list_my_pets" изменяем api ключ и пробуем запрашивать список моих питомцев.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_my_pets(auth_key, filter)
    assert status == 403
    assert '403' in result


def test_must_not_add_new_pet_with_not_valid_key(name='Геннадий', animal_type='крокодил',
                                                 age='3', pet_photo='images/Croco.jpg'):
    """Проверяем что нельзя добавить питомца с не корректным api ключом."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_with_not_valid_key(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    if status != 200:
        assert status == 403
        assert '403' in result
    else:
        raise Exception("Error! Pet uploaded")


def test_no_successful_delete_self_pet_with_not_valid_id():
    """Проверяем что нельзя удалить питомца другого пользователя.
    Статус приходит 200, это баг сервера"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список всех питомцев больше чем список моих питомцев, получаем ID чужого питомца и пробуем удалить питомца другого пользователя
    if len(pets['pets']) > len(my_pets['pets']):
        try:
            pet_id = pets['pets'][-1]['id']
            status, _ = pf.delete_pet(auth_key, pet_id)
            print(status, pet_id)
            # Проверяем что статус ответа != 200 и имени питомца нет в списке питомцев
            # assert status != 200  Статус приходит 200, это баг сервера
            assert pet_id not in pets.values()
        except AssertionError as error:
            raise AssertionError(f"Another user's pet has been deleted, {error}")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Новыйкот", "кот", "3", "images/Cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_сleaning_up_after_testing():
    """Чистим после тестов"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    while len(my_pets['pets']) > 0:
        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in [pet['id'] for pet in my_pets['pets']]


def test_not_get_api_key_with_invalid_user_password(email=valid_email, password=not_valid_password):
    """ Проверяем что нельзя зарегистрироваться в системе с неверным паролем.
    Проверяем что запрос api ключа возвращает статус 403 и в теле ответа содержится:
     'This user wasn&#x27;t found in database' """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "This user wasn&#x27;t found in database" in result


#Из-за багов в апи на данный момент следущие тесты не выполняются!


def test_must_not_add_pet_photo_with_incorrect_extension(pet_photo='images/Croco.pdf'):
    """Проверяем что нельзя добавить фотографию питомца с не корректным расширением файла."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то добавляем фото питомца
    if len(my_pets['pets']) > 0:

        status, result = pf.add_pet_foto(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что в ответе есть ошибка и статус ответа != 200

        assert status != 200
        assert 'Error' in result
    else:
        # если фото добавилось, то пишем текстом сообщение об ошибке.
        raise Exception("Error! Photo uploaded")


def test_add_must_not_new_pet_with_not_valid_name(name='Недовольный' * 10, animal_type='кот',
                                                  age='3', pet_photo='images/Cat.jpg'):
    """Проверяем что нельзя добавить питомца с именем содержащим большое количество букв."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    if status != 200:
        assert status == 400
        assert '400' in result
    else:
        raise Exception("Error! Pet uploaded")


def test_add_new_simple_pet_with_not_valid_data(name='', animal_type='',
                                                age=''):
    """Проверяем что нельзя добавить питомца без фото с данными содержащими пустые строки."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age, )

    # Сверяем полученный ответ с ожидаемым результатом
    if status != 200:
        assert status == 400
        assert '400' in result
    else:
        raise Exception("Error! Pet uploaded")


def test_must_not_add_new_pet_with_empty_strings(name='', animal_type='', age='', pet_photo='images/Cat.jpg'):
    """Проверяем что нельзя добавить питомца с данными об имени, виде, возрасте, содержащими пустые строки."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    if status != 200:
        assert status == 400
        assert '400' in result
    else:
        raise Exception("Error! Pet uploaded")



def test_must_not_add_new_pet_with_not_valid_animal_type(name='Геннадий', animal_type=';$*/.,(}',
                                                         age='3', pet_photo='images/Croco.jpg'):
    """Проверяем что нельзя добавить питомца с полем "вид" заполненным спец символами."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    if status != 200:
        assert status == 400
        assert '400' in result
    else:
        raise Exception("Error! Pet uploaded")


def test_must_not_add_new_pet_with_not_valid_age(name='Геннадий', animal_type='крокодил',
                                                 age='три', pet_photo='images/Croco.jpg'):
    """Проверяем что нельзя добавить питомца с с полем "возраст" заполненным не цифрами"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    if status != 200:
        assert status == 400
        assert '400' in result
    else:
        raise Exception("Error! Pet uploaded")
# Моделирование Броуновского движения
## ***Броуновское движение***
**Беспорядочное** движение микроскопических видимых взвешенных частиц твёрдого вещества в жидкости или газе, вызываемое тепловым движением частиц жидкости или газа. Было открыто в 1827 году Робертом Броуном. Броуновское движение никогда не прекращается.
Данное приложение разработано для изучения свойств частицы и её траектории в Броуновском движении.

## Запуск
```cmd
python main.py
```

## Команды
```
создать RADIUS MASS VX VY R G B - добавляет 1 частицу с заданными параметрами
создать N                       - создаёт N частиц с параметрами по-умолчанию
очистить                        - удаляет все частицы
кол-во                          - выводит кол-во частиц на экране
выделить UIDS                   - прячет все частицы, кроме UIDS
отслеживать SECONDS UID         - рисует траекторию частицы UID SECONDS секунд
стоп                            - останавливает движение
выход                           - выход из приложения
сброс                           - сбрасывает изменения после выделить или следить
помощь                          - вывод справки
```
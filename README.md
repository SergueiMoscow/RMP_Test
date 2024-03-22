В проекте используется python 3.12.
## Тестовое задание RMP
#### (Сушков Сергей)
Github: `https://github.com/SergueiMoscow/RMP_Test`
## Запуск
`git clone https://github.com/SergueiMoscow/RMP_Test`

`cd RMP_Test`

`docker build -t rmp_test .`

`docker run -d -p 80:8000 rmp_test`

### Используемые пакеты:
`pandas` - для импорта XLS

`pytest` - для тестирования

`openpyxl` - для получения невалидного XLS файла для тестирования 

#### Запуск тестов: `make test`
#### Запуск web сервера: `make run`
#### Папка files - файлы, используемые в коде, в т.ч. в тестах

# Todo

- [x] add get static file
- [x] split or spot get/post method
- [x] split system env and view`s env by fronts
- [ ] add support add custom 404Page
- [ ] reorg error  
- [ ] make stadart config view (add Debug behaver)
- [ ] add custom env for render_template in ViewResult
- [x] optim template by jija (move navigate to other page)
- [ ] connect logger (fix config)
- [ ] add admin panel
- [ ] add viewAdmin Type like in flask
- [ ] add static var
- [x] switch dict view url finder to tree
- [ ] test url tree (/<a:int>/)

## Task

- [ ] Реализовать создание профиля студента (регистрация). Список студентов.
    Механику записи студента на курс.
- [ ] Далее можно сделать всё или одно на выбор, применив при этом один из структурных
паттернов, либо аргументировать, почему эти паттерны не были использованы:

- [ ] Создать страницу для изменения курса. После изменения отправлять уведомления
всем студентам на курсе по SMS, email (для имитации можно просто выводить
сообщения в консоль). Также известно, что скоро способов уведомления будет
больше.
- [ ] Добавить возможность применять цикл for к объекту категории курса (в каждой
итерации получаем курс) и объекта курса (в каждой итерации получаем студента).
Например: for student in course: ... for course in group.
- [ ] Создать API для курсов. По определённому адресу выводить не веб-страницу,
    а отдавать пользователю данные о списке курсов в формате json.
- [ ] Улучшить логгер (или добавить, если его нет).
    Добавить в логгер возможность писать в файл, в консоль.
    Также известно, что в будущем вариантов сохранения может стать ещё больше.

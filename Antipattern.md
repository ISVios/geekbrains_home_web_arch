## Magic Number // Магические числа
 В коде присудствуют магические числа:
 
 ```python
 def get_mapper(obj) -> "tuple[Type, Mapper] | None":
        for _, v in MapperRegistry.mappers.items():
            if isinstance(obj, v[0]):
                return v[1]  # (connection)
        raise ValueError("mapper no found")
 ```

 ```python
    MapperRegistry.get_current_mapper(cls.tablename)[1]._drop_all()

 ```
 где **v[0]**, **v[1]** является вероятным местом ошибки(во время рефакторинга или оптимизации)

### Решение
    
    Ввод именнованныйх полей через dict

 ```python
  MapperRegistry.mappers[_tablename] = {"class_type": cls, "mapper": self}
 ```

### Резултат
 
 ```python
 def get_mapper(obj) | None":
        for _, v in MapperRegistry.mappers.items():
            if isinstance(obj, v["class_type"]):
                return v["mapper"]
        raise ValueError("mapper no found")
 ```

 ```python
    MapperRegistry.get_current_mapper(cls.tablename)["mapper"]._drop_all()

 ```

## Spaghetti Code // Спагетти-код
    Синдром самозванца и перфекционизм говорят, что всё что я пишу, является "Spaghetti code"
## Lasagna Code // Лазанья-код
    ---
## Blind faith // Слепая вера
    В питоне принято не проверять данные через if-else, а оборачивать все в try-exect.
    Однако try-exect медленее и нарушает flowchart логику, подобно (goto) 
## Cryptic Code // Шифрокод
    ----
## Hard Code // Жёсткое кодирование
    ----
## Soft Code // Мягкое кодирование
    ----
## Lava flow // Поток лавы
    ----
## Anemic Domain Model // Боязнь размещать логику в объектах предметной области
    ----
## God object (The Blob) // Божественный объект
    В данном проекте существует синглтон "Framework", который является основной точкой входа в фреймворк.
## Poltergeist // Полтергейст
    ---- 
    ~~Не является ли Полтергейст == Builder class~~
## Singletonitis // Сплошное одиночество
    ----
## Privatization // Приватизация
    Осталась привычки использовать private(c/java) для всего, однако это противоречит SOLID(O-Open-Closed)
## Copy — Paste // Программирование методом копирования — вставки
    Чаще печатаю самотоядельно, Copy-Paste использую отдельно от проекта для проверки (фукции\методик)   
## Golden hammer // Золотой молоток
    Не в чём не уверен. Все можно оптимизировать.
## Improbability factor  // Фактор невероятности
    ----
## Premature optimization // Преждевременная оптимизация
    Очень сложный антипаттерн
### Решение
    Написание ТЗ (Usecase -> ClassDiagram -> SequenceDiagram)
    Установка временных рамок
    Написание alpha версии (программы/метода) (с "костылями" =( ) удовлетворяющее ТЗ
    Оптимизация
## Reinventing the wheel // Изобретение велосипеда
## Reinventing the square wheel // Изобретение квадратного колеса
    Данный код является велосипедом(с квадратными колесами), так как сущетвует годовые web-Framework(flask, django)
## Abstract Inversion // Инверсия абстракции
    ----
## Big ball of mud // Большой комок грязи
    ----
## Input kludge // Затычка на ввод
    ----
## Magic button // Волшебная кнопка
    ----
## Mutilation // Членовредительство
    ----
## Stovepipe Enterprise // Дымоход предприятия
    ----
## Stovepipe System // Дымоход системы
    ----
## Jumble // Путаница
    ----

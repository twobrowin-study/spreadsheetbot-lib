# Python библиотека бота с управлением Google таблиц

[Пример таблицы - только на чтение](https://docs.google.com/spreadsheets/d/1dkpFEvOqWvVM_cJAnKvaQ0Ne8MmGPjy33cvPeeSwi-o/edit?usp=sharing)

## Установка библиотеки

`pip install spreadsheetbot`

## Использование библиотеки

Для использования библиотеки потребуется обеспечить следующие параметры:

* `bot_token: str` - Токен подключения бота

* `sheets_secret: str` - JSON строка с ключами доступа к Google Cloud API

* `sheets_link: str` - Ссылка для подключения к Google таблице

* `switch_update_time: int` - Время обновления таблицы `Рубильник` (сек)

* `setting_update_time: int` - Время обновления таблицы `Настройки` (сек)

Далее, следует имортировать класс библиотеки и обеспечить его работу

```python
from spreadsheetbot import SpreadSheetBot

if __name__ == "__main__":
    bot = SpreadSheetBot(BotToken, SheetsSecret, SheetsLink, SwitchUpdateTime, SettingsUpdateTime)
    bot.run_polling()
```

Дополнительно, возможно указать debug настройки вывода библиотеки:

```python
from spreadsheetbot import Log, DEBUG

Log.setLevel(DEBUG)
Log.debug("Starting in debug mode")
```

## Функциональное наполнение - поддерживаемые таблицы

### Рубильник

Эта таблица предназначена для срочного выключения бота, поле `bot_active` выключает бота с исключением `BotShouldBeInactive`.

Поле `user_registration_open` заперщает регистрацию новых пользователей.

### Группы

Бота можно добавлять в группы, однако требуется ручное добавление идентификатора группы для использования ботом.

Идентификатор группы можно получить из таблицы `Логи`.

Группы могут иметь статус `is_admin` Нет, Да и Супер. Обычные группы получают все уведомления из таблицы `Оповещения`, админские группы - оповещения о количестве зарегистрированных пользователей и имею команду `/report` - будет выслано содержимое таблицы `Отчёт`.

Суперадминские группы также получают уведомления об ошибках:

* Общие ошибки

* Ошибки ввода пользователей

### Пользователи

Пользователи (таблица `Пользователи`) могут регистрировать в соответствии с описанием в таблице `Параметры регистрации`.

В таблице `Параметры регистрации` можно указать ссылку для записи данных на диск. В случае если ссылка указана, от пользователя будет ожидаться передача фото или документа. Фото или документ будет сохранён по указанной ссылке с именем файла, соответствующем полю пользоватля, указанному в таблице `Настройки` в поле `user_document_name_field`. Такие поля не предполагаются как основные вопросы поскольку текст из таблицы не форматируется в форме отображения регистрации пользователя. _Директория обязательно должна быть с доступом на записть!_

Также можно указать `state` для того чтобы пользователь ответил на конвретный вопрос - аналогично таблице `Оповещения`.

Пользователи имеют возможность изменить регистрационные данные при помощи таблицы `Клавиатура`

### Оповещения

Оповещения высылаются в установленную дату, возможно выслать картинку и указать поле, в которое таблицу будут сохранены ответы пользователей.

Можно указать как варианты ответов на вопросы в формате перечисленных кнопок или добавить единственную кнопку для начала ввода пользователя. Подробнее правила оформления смотри в описании колонок в тестовой таблице.

Возможно указать ссылку для сохранения фото или документа, далее логика аналогична сохранению фото или документа в таблице `Пользватели`.

Возможно указать столбец - условие для оповещения. В таком случае, оповещение будут получать только пользователи, для которых указано значение `Да` в этом слобце. Для успешного оповещения следует учитывать время синхронизации между таблицами `Пользователи` и `Оповещения`!

### Клавиатура

Клавиатура содержит описание показываемой зарегистрированному пользователю клавиатуры с помощью ввода.

Поддерживается функция (поле `function`) register для изменения регистрационных данных пользователя.

### Настройки, Логи, i18n

Настройки содержат все настройки приложения, в том числе текстовки стандартных сообщений пользователю.

В Логи записываются запуски, остановки приложения, добавления бота в группы, баны пользователей и ошибки ввода пользователя.

Интернационализация i18n содержит стандартные текстовки для переводов текстов.
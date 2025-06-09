# postmanager

Тестовое задание. Web-приложение для работы с a la blog posts и telegram-бот для взаимодействие с ними.

# Установка и запуск
## Web-приложение
```bash
git clone https://github.com/dfwdfq/postmanager.git
cd postmanager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
## Бот
В отдельном терминале
```
cd postmanager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 bot.py #шебанга нет
```

В браузере API будет доступно по адресу ```localhost:5000```.<br>
Бот имеет ник:```@yet_another_postmanager_bot```

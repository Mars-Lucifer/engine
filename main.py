"""
This module handles the main functionality for the Pokemon app.
"""
import os
import time
import json
import threading
from datetime import datetime

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

CODE = "7842"
app = Flask(__name__)

# Путь для сохранения аватаров
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DB_FILE = 'db.json'

# Проверяем, есть ли папка для загрузок, если нет — создаем
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Читаем базу данных или создаем пустую


def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as db_file:
            return json.load(db_file)
    return []

# Сохраняем изменения в базе данных


def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as db_file:
        json.dump(data, db_file, ensure_ascii=False, indent=4)


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/pok')
def pokemons():
    return render_template('/pokemons.html')


@app.route('/create', methods=['GET', 'POST'])
def create_team():
    if request.method == 'POST':
        # Получаем данные формы
        team_name = request.form['team_name']
        verification_code = request.form['verification_code']

        if verification_code == CODE:
            # Загружаем участников
            members = []
            for i in range(1, 5):
                avatar_file = request.files.get(f'avatar{i}')
                participant_name = request.form.get(f'avatar{i}')

                if avatar_file and participant_name:
                    filename = secure_filename(avatar_file.filename)
                    file_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], filename)
                    avatar_file.save(file_path)

                    # Преобразуем обратные слеши в прямые
                    file_path = file_path.replace('\\', '/')

                    members.append({
                        'name': participant_name,
                        'avatar_path': file_path
                    })

            # Загружаем существующие команды из базы данных
            data = load_db()

            # Генерируем уникальный номер команды
            team_id = len(data) + 1

            # Формируем данные команды с новыми полями
            team_data = {
                'id': team_id,
                'team_name': team_name,
                'members': members,
                'points': 0,
                'tasks': [
                    [0, "Проведите мини-фотосессию команды с заданной темой - «Эмоции нашей команды»"],
                    [0, "Создайте забавный мем о вашей команде"],
                    [0, "Выложить 5 историй в социальной сети ВКонтакте с хэштегом #КомандаПервых31"],
                    [0, "Снять рилс «5 плюсов учебы в «название образовательной организации» или «почему я активист движения первых»"],
                    [0, "Командная история, участникам требуется составить увлекательную и небольшую историю, снятую на видео. Где каждый участник по очереди продолжает историю пока все не выскажутся"],
                    [0, "Нарисовать общий рисунок команды на любую социальную тему"],
                    [0, "Придумать гимн/песню для своей команды"],
                    [0, "Сделать фотографию возле флага Движения Первых всей командой"]
                ],
                'pokemons': [0, 0]
            }

            # Добавляем новую команду в базу данных
            data.append(team_data)
            save_db(data)

            # Переадресуем на страницу команды
            return "Команда успешно создана"
        else:
            return "Ошибка, неверный код"
    else:
        return render_template('create_team.html')


@app.route('/command/<int:team_id>')
def team_details(team_id):
    # Загружаем базу данных
    data = load_db()

    # Ищем команду по ID
    team = next((team for team in data if team['id'] == team_id), None)

    if team:
        # Исключаем последнее техническое задание
        return render_template('profile.html', team=team, pokemons=team['pokemons'])
    else:
        return "Команда не найдена", 404


@app.route('/edit/<int:team_id>', methods=['GET', 'POST'])
def edit(team_id):
    # Загружаем базу данных
    data = load_db()

    # Ищем команду по ID
    team = next((team for team in data if team['id'] == team_id), None)

    if team:
        if request.method == 'POST':
            verification_code = request.form['verification_code']

            if verification_code == CODE:
                # Обработка изменения очков
                points_change = request.form.get('points')
                if points_change:
                    try:
                        points_change = int(points_change)
                        if team['pokemons'][0] == 0:
                            team['points'] = int(
                                team['points'] + points_change)
                        else:
                            team['points'] = int(
                                team['points'] + points_change + ((points_change / 100) * 20))
                    except ValueError:
                        pass  # Игнорируем некорректный ввод

                # Обработка изменения статуса заданий
                task_change = request.form.get('task')
                pokemon = team['pokemons']
                if task_change:
                    try:
                        task_id = int(task_change) - 1
                        if team['tasks'][task_id][0] == 0:
                            # Если не выполнено, делаем выполненным
                            team['tasks'][task_id][0] = 1
                            if pokemon[0] == 0:
                                team['points'] += 100  # + 100 без покемона
                            else:
                                # +100 и +20% с покемоном
                                team['points'] = int(
                                    team['points'] + 100 + ((100/100) * 20))
                        else:
                            team['tasks'][task_id][0] = 0
                            if pokemon[0] == 0:
                                team['points'] -= 100  # -100 без покемона
                            else:
                                # -100 и -20% без покемона
                                team['points'] = int(
                                    team['points'] - 100 - ((100/100) * 20))
                    except (ValueError, IndexError):
                        pass  # Игнорируем некорректный ввод или индекс

                # Проверка выполнения заданий и назначение покемонов
                if all(team['tasks'][i][0] == 1 for i in range(3)):  # Задания 1, 2, 3
                    team['pokemons'][0] = 1  # Покемон 1
                else:
                    team['pokemons'][0] = 0
                if all(team['tasks'][i][0] == 1 for i in range(3, 6)):  # Задания 4, 5, 6
                    team['pokemons'][1] = 1  # Покемон 2
                else:
                    team['pokemons'][1] = 0

                # Изменение названия команды
                title = request.form.get('team_name')
                if title != "":
                    team['team_name'] = title
                else:
                    pass

                # Изменение имён участников
                for i in range(4):
                    member_name = request.form.get(f'avatar{i+1}')
                    if member_name != "":
                        team['members'][i]['name'] = member_name
                    else:
                        pass

                # Изменение фотографий участников
                for i in range(1, 5):
                    avatar_file = request.files.get(f'avatar{i}')

                    if avatar_file:
                        filename = secure_filename(avatar_file.filename)
                        file_path = os.path.join(
                            app.config['UPLOAD_FOLDER'], filename)
                        avatar_file.save(file_path)

                        # Преобразуем обратные слеши в прямые
                        file_path = file_path.replace('\\', '/')

                        team['members'][i-1]['avatar_path'] = file_path

                # Сохраняем обновленную команду
                save_db(data)

                return "Успешно изменено"
            else:
                return "Неверный код"
        else:
            # GET-запрос: отрисовываем страницу
            return render_template('edit.html', team=team)
    else:
        return "Команда не найдена", 404


def add_bonus_points():
    data = load_db()

    for team in data:
        if team['pokemons'][1] == 1:
            print(int(team['points'] * 0.25))
            team['points'] += int(team['points'] * 0.25)

    save_db(data)

@app.route('/top', methods=['GET'])
def top():
    # Загружаем базу данных
    data = load_db()

    # Получаем значение из формы поиска
    search_query = request.args.get('search', '').lower()

    # Если есть запрос на поиск, фильтруем команды по названию
    if search_query:
        filtered_teams = [team for team in data if search_query in team['team_name'].lower()]
    else:
        # Если запроса нет, выводим все команды
        filtered_teams = data

    # Сортируем команды по количеству очков (от большего к меньшему)
    sorted_teams = sorted(filtered_teams, key=lambda team: team['points'], reverse=True)

    # Отправляем отсортированные данные в шаблон
    return render_template('top.html', teams=sorted_teams)

@app.route('/talisman')
def talisman():
    return render_template('/talisman.html')


# Расписание задачи на 12 октября в 19:00
def schedule_task():
    # Установим точную дату и время
    target_date = datetime(2024, 10, 13, 19, 0)
    current_time = datetime.now()

    if current_time >= target_date:
        add_bonus_points()
        return False


def run_scheduler():
    while True:
        if schedule_task():
            break
        time.sleep(30 * 60)  # Проверяем каждые 30 минут


# Запуск планировщика в отдельном потоке
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # Поток завершится при завершении основного потока
scheduler_thread.start()

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import in_BD
import parse_news

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    connection = in_BD.db_connection()
    cursor = connection.cursor()
    select = """select * from vacancies order by Дата_публикации desc LIMIT 20"""
    cursor.execute(select)
    vacancies = cursor.fetchall()
    if request.method == "POST":
        in_BD.bd_update_vacancies()
        return render_template('index.html', vacancies=vacancies)
    in_BD.db_conn_close()
    return render_template('index.html', vacancies=vacancies)


@app.route('/archive/', methods=['GET', 'POST'])
def archive():
    connection = in_BD.db_connection()
    cursor = connection.cursor()
    select = """select * from news where Архив = 1 order by Дата_публикации desc"""
    cursor.execute(select)
    archive = cursor.fetchall()
    if request.method == "POST":
        t = request.form.get('name')
        in_BD.delete_from_archive(t)
        return render_template('archive.html', archive=archive)
    in_BD.db_conn_close()
    return render_template('archive.html', archive=archive)


@app.route('/news/', methods=['GET', 'POST'])
def news():
    connection = in_BD.db_connection()
    cursor = connection.cursor()
    select = """select * from news order by Дата_публикации desc LIMIT 20"""
    cursor.execute(select)
    news = cursor.fetchall()
    if request.method == "POST":
        in_BD.bd_update_news()
        return render_template('news.html', news=news)
    in_BD.db_conn_close()
    return render_template('news.html', news=news)


@app.route('/send', methods=['POST'])
def send():
    message = ''
    form = request.form
    if request.method == "POST":
        t = form.get('name')
        in_BD.insert_in_archive(t)
        message = "Добавлен в архив"
    return message


if __name__ == '__main__':
    app.run()

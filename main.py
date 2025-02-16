from flask import Flask, render_template, send_from_directory, make_response
from werkzeug.utils import safe_join
from os.path import exists, abspath, dirname, join
import socket
import logging

school_name = 'Hangzhou Wenli Middle School'
target_host = '0.0.0.0'
target_port = 8080


def get_file(file_name):
    file_path = join(PROJECT_ROOT, file_name)
    if exists(file_path):
        file_file = open(file_path, 'r')
        file_content = file_file.read()
        logging.debug(f"Served file file: {file_name} with status code 200")
        response = make_response(file_content, 200, {'Content-Type': 'text'})
        return response
    logging.debug(f"file file not found: {file_name}")
    return "file file not found", 404


def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


logging.basicConfig(level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().addHandler(logging.FileHandler('app.log'))

PROJECT_ROOT = abspath(dirname(__file__))
app = Flask(__name__, static_folder=None, template_folder=join(PROJECT_ROOT, 'templates'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/static/<path:file_path>')
def static(file_path):
    # 构建安全的文件路径
    file_dir = join(PROJECT_ROOT, 'static')
    safe_file_path = safe_join(file_dir, file_path)

    # 检查文件是否存在
    if not exists(safe_file_path):
        logging.warning(f"File not found: {safe_file_path}")
        return "File not found", 404

    # 记录请求日志
    logging.info(f"Served file: {file_path} with status code 200")

    return send_from_directory(file_dir, file_path)


@app.route('/')
def index():
    return render_template('index.html', school_name=school_name)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/facilities')
def facilities():
    return render_template('facilities.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/log')
def log():
    return get_file('app.log')


@app.route('/sitemap')
def sitemap():
    return get_file('sitemap.txt')


@app.route('/robots.txt')
def robots():
    return get_file('robots.txt')


@app.route('/license')
def show_license():
    return get_file('LICENSE')


if __name__ == '__main__':
    while check_port(target_host, target_port):
        target_port += 1
    app.run(host=target_host, port=target_port)

from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()


@app.route('/')
def home():
    return render_template('home.html', short_codes=session.keys())


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':

        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['short_code'] in urls.keys():
            flash('That Short Name is Already Taken. Please Choose Another Short Name.')

            return redirect(url_for('home'))

        if 'url' in request.form.keys():

            urls[request.form['short_code']] = {'url': request.form['url']}

        else:

            file = request.files['your_file']

            file_full_name = request.form['short_code'] + secure_filename(file.filename)

            file.save('/home/nerdx/Desktop/ShortenerFox/static/user_files/' + file_full_name)

            urls[request.form['short_code']] = {'file': file_full_name}

        with open('urls.json', 'w') as url_file:

            json.dump(urls, url_file)

            session[request.form['short_code']] = True

        return render_template('your-url.html', short_code=request.form['short_code'])

    else:

        return redirect(url_for('home'))


@app.route('/<string:short_code>')
def redirect_to_url(short_code):
    if os.path.exists('urls.json'):

        with open('urls.json') as url_file:

            urls = json.load(url_file)

            if short_code in urls.keys():

                if 'url' in urls[short_code].keys():

                    return redirect(urls[short_code]['url'])

                else:

                    return redirect(url_for('static', filename='user_files/' + urls[short_code]['file']))

    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

#-*- encoding: utf8 -*-
from flask import Flask, render_template, request, abort, send_file
from checktools import check_text, is_py_extension, pep8parser, template_results
from datetime import datetime
from generate import gen_text_file, gen_result_text
from tools import generate_short_name
import pep8
import autopep8
from forms import ContactForm
import os



from bson.objectid import ObjectId

app = Flask(__name__)
app.config['TEMP_PATH'] = '/var/www/FlaskApp/FlaskApp/tmp/'
app.secret_key = 'development key'


def get_datetime():
    """return datetime as string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@app.route("/")
def paste_page():
    """
    Main page with form for paste code
    """
    return render_template("paste_page.html")


@app.route('/123', methods=('POST'))
def my_form_post():
	form = ContactForm()
	aaa = ''
	if request.method == 'POST':
		messa = request.form["message"]
		aaa = check_text(
                messa,
                app.config['TEMP_PATH']
            )
		return render_template('123.html', form=form, aaa = aaa)

	

@app.route("/1231", methods=('POST', ))
def hello():
    back_url = str(request.referrer).replace(request.host_url, '')
    context = {
        'result': '',
        'code_text': '',
        'error': '',
        'back_url': back_url,
    }
    if request.method == "POST":
        code_text = request.form["code"]
        code_file = gen_text_file(code_text)
        try:
            context['code_text'] = request.form["code"]
        except KeyError:
            abort(404)
        if not context['code_text']:
            context['error'] = 'Empty request'
            return render_template("123.html", **context)
        else:
            context['result'] = auto_pep(
                context['code_text'],
                app.config['TEMP_PATH']
            )
           
    return render_template("123.html",**context)

	
@app.route("/about")
def about():
    """About page"""
    return render_template("about.html")


@app.route("/upload")
def upload_page():
    """
    Main page with form for upload file
    """
    return render_template("upload_page.html")


@app.route("/checkresult", methods=('POST', ))
def check_result():
    """
    Show results for checked code
    """

    back_url = str(request.referrer).replace(request.host_url, '')
    context = {
        'result': '',
        'code_text': '',
        'error': '',
        'back_url': back_url,
    }
    if request.method == "POST":
        if str(request.referrer).replace(request.host_url, '') == 'upload':
            code_file = request.files['code_file']
            if not code_file:
                context['error'] = 'Forget file'
                return render_template("check_result.html", **context)
            if not is_py_extension(code_file.filename):
                context['error'] = 'Please upload python file'
                return render_template("check_result.html", **context)
            context['code_text'] = code_file.read()
        else:
            try:
                context['code_text'] = request.form["code"]
            except KeyError:
                abort(404)
        if not context['code_text']:
            context['error'] = 'Empty request'
            return render_template("check_result.html", **context)
        else:

            context['result'] = check_text(
                context['code_text'],
                app.config['TEMP_PATH']
            )
    return render_template("check_result.html", **context)

@app.route("/savecode", methods=['POST', ])
def save_code():
    if request.method == "POST":
        code_text = request.form["orig_code"]
        code_file = gen_text_file(autopep8.fix_code(code_text))
        attachment_filename = ''.join(('code_', get_datetime(), '.py'))
        return send_file(code_file,
                         mimetype="application/x-python",
                         as_attachment=True,
                         attachment_filename=attachment_filename)
    else:
        return ''

if __name__ == '__main__':
    app.run()
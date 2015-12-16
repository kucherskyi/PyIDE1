#-*- encoding: utf8 -*-

import pep8
import autopep8
import os
from bson.objectid import ObjectId
from flask import Flask, render_template, request, abort, send_file
from datetime import datetime

from generate import gen_text_file, gen_result_text
from tools import generate_short_name
from checktools import check_text, is_py_extension, pep8parser, template_results


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
    return render_template("paste.html")


@app.route("/result", methods=('POST', ))
def check_result():
    """
    results for code
    """

    back_url = str(request.referrer).replace(request.host_url, '')
    context = {
        'result': '',
        'code_text': '',
        'error': '',
        'back_url': back_url,
    }
    if request.method == "POST":
        if not context['code_text']:
            context['error'] = 'Empty request'
            return render_template("chec.html", **context)
        else:
            context['result'] = check_text(
                context['code_text'],
                app.config['TEMP_PATH']
            )
    return render_template("check.html", **context)


@app.route("/save", methods=['POST', ])
def save_code():
    if request.method == "POST":
        code_text = request.form["orig_code"]
        code_file = gen_text_file(autopep8.fix_code(code_text))
        attachment_filename = ''.join(('code_', '.py'))
        return send_file(code_file,
                         mimetype="application/x-python",
                         as_attachment=True,
                         attachment_filename=attachment_filename)

if __name__ == '__main__':
    app.run()

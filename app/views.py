from app import app
from flask import render_template, request, redirect, jsonify
import json

@app.route("/")
def index():
    return render_template("test.html")

@app.route("/config-testcases/")
def config_testcases():
    with open('./.config.json', 'r') as f:
        data = json.load(f)
        tests = data['tests']
        for id,t in enumerate(tests):
            t['id']=str(id)
        return render_template("test_urls.html", tests=tests)
    return "Error!"

@app.route("/config-browsers/")
def config_browsers():
    return render_template("test_browsers.html")

@app.route('/update_test_url/<int:id>', methods=["POST"])
def update_test_url(id):
    new_data = request.form['new_url']
    with open('./.config.json', 'r+') as f:
        data = json.load(f)
        data['tests'][id]['url']=new_data
        f.seek(0)
        f.truncate()
        json.dump(data, f)
        resp=jsonify(success=True)
        return resp

@app.route('/delete_test_url/<int:id>', methods=['POST'])
def delete_test_url(id):
    with open('./.config.json', 'r+') as f:
        data = json.load(f)
        data['tests'].pop(id)
        f.seek(0)
        f.truncate()
        json.dump(data, f)
        resp=jsonify(success=True)
        return resp

@app.route('/add_test_url/', methods=['POST'])
def add_test_url():
    new_tc=request.form['new_tc']
    new_lang=request.form['sel-lang']
    with open('./.config.json', 'r+') as f:
        data = json.load(f)
        data['tests'].append({"url": new_tc, "language": new_lang})
        f.seek(0)
        f.truncate()
        json.dump(data, f)
        return redirect('/config-testcases/')


@app.route('/config/', methods=["GET"])
def get_config():
    with open('./.config.json', 'r') as f:
        return jsonify(json.load(f))

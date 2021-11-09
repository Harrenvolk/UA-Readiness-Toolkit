from app import app
from src.browser_interactor.main import test_ua_readiness, generate_screenshot
from flask import render_template, request, redirect, jsonify
import json
from dotenv import load_dotenv

@app.route("/")
def index():
    return render_template("test.html")

@app.route("/config-testcases/")
def config_testcases():
    with open('./.config.json', 'r', encoding="utf-8") as f:
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
    with open('./.config.json', 'r+', encoding="utf-8") as f:
        data = json.load(f)
        data['tests'][id]['url']=new_data
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False)
        resp=jsonify(success=True)
        return resp

@app.route('/delete_test_url/<int:id>', methods=['POST'])
def delete_test_url(id):
    with open('./.config.json', 'r+', encoding="utf-8") as f:
        data = json.load(f)
        data['tests'].pop(id)
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False)
        resp=jsonify(success=True)
        return resp

@app.route('/add_test_url/', methods=['POST'])
def add_test_url():
    new_tc=request.form['new_tc']
    new_lang=request.form['sel-lang']
    with open('./.config.json', 'r+', encoding="utf-8") as f:
        data = json.load(f)
        data['tests'].append({"url": new_tc, "language": new_lang})
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False)
        return redirect('/config-testcases/')


@app.route('/config/', methods=["GET"])
def get_config():
    with open('./.config.json', 'r', encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route('/run_tests/')
def run_tests():
    load_dotenv()
    with open('./.config.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        list_of_domains=[]
        list_of_language_codes=[]
        for test in data['tests']:
            list_of_domains.append(test['url'])
            list_of_language_codes.append(data['languages'][test['language']])
        list_of_image_files = generate_screenshot(list_of_domains, list_of_language_codes, "Chrome")
        test_ua_readiness(list_of_image_files, list_of_language_codes)
        return jsonify(success="True")

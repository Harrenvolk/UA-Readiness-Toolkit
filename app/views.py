from app import app
from src.browser_interactor.main import test_ua_readiness, generate_screenshot
from flask import render_template, request, redirect, jsonify
import json
from dotenv import load_dotenv
from src.dns_sniffer.dns_sniffer import list_active_interfaces, run_powershell, initiate_sniffing
import threading
import idna

@app.route("/")
def index():
    return render_template("test.html", interfaces=list_active_interfaces())


@app.route("/config-testcases/")
def config_testcases():
    with open('./.config.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        tests = data['tests']
        for id, t in enumerate(tests):
            t['id'] = str(id)
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
        data['tests'][id]['url'] = new_data
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False)
        resp = jsonify(success=True)
        return resp


@app.route('/delete_test_url/<int:id>', methods=["POST"])
def delete_test_url(id):
    with open('./.config.json', 'r+', encoding="utf-8") as f:
        data = json.load(f)
        data['tests'].pop(id)
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False)
        resp = jsonify(success=True)
        return resp


@app.route('/add_test_url/', methods=["POST"])
def add_test_url():
    new_tc = request.form['new_tc']
    new_lang = request.form['sel-lang']
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


@app.route('/run_tests/', methods=["POST"])
def run_tests():
    interface = request.form['interface']
    browser = request.form['browser']
    load_dotenv()
    
    # WINDOWS ONLY
    run_powershell("Clear-DnsClientCache")
    sniffer_thread=threading.Thread(target=initiate_sniffing, name="sniffer", args=(interface,))
    sniffer_thread.start()

    with open('./.config.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        list_of_domains = []
        list_of_language_codes = []
        list_of_languages = []
        for test in data['tests']:
            list_of_domains.append(test['url'])
            list_of_language_codes.append(data['languages'][test['language']])
            list_of_languages.append(test['language'])
        list_of_image_files, is_successful = generate_screenshot(
            list_of_domains, list_of_language_codes, browser=browser)
        is_ulabel = test_ua_readiness(list_of_image_files, list_of_language_codes)
        transmitted_as = [idna.encode(domain) for domain in list_of_domains]

        if sniffer_thread.is_alive():
            sniffer_thread.join()

    results = []
    

    for i in range(0, len(list_of_domains)):
        results.append({
            'language': list_of_languages[i] + " - "+ list_of_language_codes[i],
            'domain': list_of_domains[i],
            'is_ulabel': is_ulabel[i],
            'is_successful': is_successful[i],
        })

    dns_results = get_dns_results()
    print(results, dns_results)
    return render_template('results.html', results=results, dns_results=dns_results)   
    # return jsonify(success="True")

def get_dns_results():
    # Read from file
    requests = []
    responses = []
    ids = []
    dns_results = []
    with open('./pkt.txt', "r", encoding='utf-8') as f:
        Lines = f.readlines()
        for line in Lines:
            striped_list = line.split(':')
            if 'Request' in striped_list[0].strip():
                requests.append({
                    'id': striped_list[2].strip(),
                    'query': striped_list[0].strip(),
                    'url': striped_list[1].strip(),
                    'query_response': "",
                    'resp_url': '',
                    'is_punny_code': True if "xn--" in striped_list[1].strip() else False,
                    'success': 0, 
                })
            else:
                responses.append({
                    'id': striped_list[2].strip(),
                    'query': striped_list[0].strip(),
                    'query_response': "",
                    'url': striped_list[1].strip(),
                    'is_punny_code': True if "xn--" in striped_list[1].strip() else False,
                    'success': True,
                })          
    for response in responses:
        for request in requests:
            if response['id'] == request['id']:
                if response['url'] == request['url']:  
                    request['success'] = 2
                else:
                    request['success'] = 1
                request['query_response'] = response['query']
                request['resp_url'] = response['url']

    return requests

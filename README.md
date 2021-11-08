# UA-Readiness-Toolkit

## Steps to run

1.  Install requirements
```bash
pip install -r src/requirements.txt
```

2. Create and fill .env with paths
```bash
cd src/browser_interactor/
cp .sample_env .env
```

3. To get list of detected browsers 
```bash
python main.py -detect_browsers
```

4. Firefox, Chrome, Edge
```bash
python main.py --browser=Firefox
```
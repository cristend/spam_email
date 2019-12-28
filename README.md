# Spam_filter
## Clone repository
```
git clone https://github.com/cristend/spam_email.git
```
## Installation requirements
### Install pipenv
upgrade pip
```sh
python -m pip install --upgrade pip
```
install pipenv
```sh
pip install pipenv
```
start pipenv 
```
pipenv shell
```
install requirements
```
pipenv install --dev --skip-lock
```
## Using guide
Process data
```
pipenv run python crawl_data.py
```
Build model
```
pipenv run python build_model.py
```
Run predict
    Step1: Store data test to app/source_data/test
    Step2:
```
pipenv run python main.py
```
One in all 
```
pipenv run python auto_run.py
```

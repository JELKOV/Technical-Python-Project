import requests

BASE_URL = "https://opentdb.com/api.php"

parameters = {
    "amount": 10,
    "type": "boolean"
}
def fetch_data():
    response = requests.get(BASE_URL, params= parameters)
    response.raise_for_status()

    data = response.json()
    questions = data['results']

    return questions

question_data = fetch_data()
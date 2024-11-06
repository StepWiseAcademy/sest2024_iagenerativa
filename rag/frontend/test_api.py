import requests

if __name__ == '__main__':

    print(requests.post('http://127.0.0.1:5000/top5', json={'query_text':'Olá'}).json())
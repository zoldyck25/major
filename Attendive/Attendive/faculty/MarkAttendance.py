import requests

def markAttendance(id_, subject, section):
    url = f"http://127.0.0.1:5000/faculty/marking_attendance/{id_}/{subject}/{section}/dd85fe3ab7ec25ea4190/"
    resp = requests.get(url)
    if resp != '0':
        return resp
    return False

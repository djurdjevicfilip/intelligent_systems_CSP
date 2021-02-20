import copy
import json

from models.exam import Exam
from models.room import Room
from models.term import Term

test_num = "7"

all_departments = []

with open("tests/rok"+test_num+".json", "rb") as read_file:
    data = json.load(read_file)


with open("tests/sale"+test_num+".json", "rb") as read_file:
    rooms_json = json.load(read_file)


def create_term(data):
    """
    Napravi objekat Term klase na osnovu .json-a
    """

    term = Term(length = data['trajanje_u_danima'])


    for exam_json in data['ispiti']:
        deps = []
        for department in exam_json['odseci']:
            deps.append(department)

        term.addExam(Exam(code=exam_json['sifra'],
                          applied_num=exam_json['prijavljeni'],
                          need_computers=exam_json['racunari'],
                          departments=deps))
        for dep in deps:
            if dep not in all_departments:
                all_departments.append(dep)

    return term

def instantiate_rooms(data, days):
    """
    Instancira sve sobe sa svim mogucim terminima na osnovu json-a
    """
    rooms = []

    for t in range(1, 4*days+1):
        for room in data:
            rooms.append(Room(name=room['naziv'],
                              capacity=room['kapacitet'],
                              has_computers=room['racunari'],
                              on_duty_num=room['dezurni'],
                              on_etf=room['etf'],
                              time=t))
   # rooms.sort()
    return rooms
term = create_term(data)


days = term.length

exams = term.exams

def instantiate_domains(vars, rooms):
    """
    Instancira sve domene na osnovu Ispita i Sala
    """
    domains ={}
    for var in vars:
        domains[var.code] = copy.deepcopy(rooms)
    return domains


rooms = instantiate_rooms(rooms_json, days)
domains = instantiate_domains(exams, rooms)
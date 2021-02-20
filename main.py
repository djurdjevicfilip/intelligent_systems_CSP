import copy
import itertools
from math import floor
from random import random, randrange

import numpy as np

import csv_writer
from setup import domains, rooms, exams, days, all_departments
import time

starting_time = time.time()

def calculate_cost(it):
    """
    Racunanje cene (broja bodova) kombinacije

    Parameters
    ---------
    it : array of integers
        Niz koji sadrzi indekse odabranih sala

    Returns
    ------------------
    cost
        Ukupna cena
    """
    cost = 0
    for index in it:
        cost += 1.2*(1 - rooms[index].on_etf) + rooms[index].on_duty_num;
    return cost

def solution_valid(solution):
    """
    Provera ispravnosti resenja, tj da li je svakoj sobi dodeljena bar 1 sala

    Parameters
    ---------
    solution : dictionary
        Resenja
    Returns
    ------------------
    boolean
        True ako je resenje ispravno po datom kriterijumu, u suprotnom False
    """
    for k,v in solution.items():
        if len(v) == 0:
            return False
    return True

def calculate_capacity(it):
    """
        Racunanje kapaciteta kombinacije

        Parameters
        ---------
        it : array of integers
            Niz koji sadrzi indekse odabranih sala

        Returns
        ------------------
        capacity
            Kapacitet
    """
    capacity = 0
    for index in it:
        capacity += rooms[index].capacity
    return capacity

def is_consistent_assignment(exam, room,exam_solution, department_constraints, department_additional_constraints):
    """
        Provera konzistentnosti dodele Sale Ispitu

        Parameters
        ---------
        exam : Exam
            Ispit kom se dodeljuje sala
        room : Room
            Sala koja se dodeljuje ispitu
        exam_solution : array of Rooms
            Trenutne sale koje su odabrane za dati ispit
        department_constraints : dictionary
            Key -> ime odseka + godina + dan
            Value -> True
            Ogranicenje : u jednom danu se ne mogu rasporediti 2 ili vise ispita sa iste godine za isti odsek
        department_additional_constraints : dictionary
            Key -> ime odseka + godina + termin
            Value -> True
            Ogranicenje : u jednom terminu se ne mogu rasporediti 2 ili vise ispita iz susednih godina za isti odske

        Returns
        ------------------
        boolean
            True ako je dodela moguca, u suprotnom False
    """
    # If room time is equal
    if exam_solution:
        if exam_solution[0].time != room.time:
            return False
    for dep in exam.departments:
        key1 = (dep + exam.year + str(int((room.time-1) / 4)))
        key2 = (dep + exam.year + str(room.time))
        if key1 in department_constraints or key2 in department_additional_constraints:
            return False

    if exam.need_computers and not room.has_computers:
        return False

    return True

def forward_checking(exams, exam, room, domains, department_constraints, department_additional_constraints):
    """
        Izbacivanje

        Parameters
        ---------
        exams : array of Exams
            Niz ispita
        exam : Exam
            Ispit kom je dodeljena soba
        room : Room
            Soba koja je dodeljena ispitu
        domains : dictionary
            Domeni
        department_constraints : dictionary
            Key -> ime odseka + godina + dan
            Value -> True
            Ogranicenje : u jednom danu se ne mogu rasporediti 2 ili vise ispita sa iste godine za isti odsek
        department_additional_constraints : dictionary
            Key -> ime odseka + godina + termin
            Value -> True
            Ogranicenje : u jednom terminu se ne mogu rasporediti 2 ili vise ispita iz susednih godina za isti odske

        Returns
        ------------------
        boolean
            True ako je nijedan domen nije prazan, ako je bar jedan prazan vraca False
    """
    for ex in exams:
        if ex != exam:
            prev_len = len(domains[ex.code])
            domains[ex.code] = [x for x in domains[ex.code] if x.name != room.name or x.time != room.time]

            # Check first dict constraints
            for constraint_key, constraint_value in department_constraints.items():
                department = constraint_key[0:2]
                year = constraint_key[2]
                day = constraint_key[3: len(constraint_key)]
                if department in ex.departments and year == ex.year:
                    domains[ex.code] = [x for x in domains[ex.code] if day != floor((x.time - 1)/4)]

            # Check second dict constraints
            for constraint_key, constraint_value in department_additional_constraints.items():
                department = constraint_key[0:2]
                year = constraint_key[2]
                time = constraint_key[3: len(constraint_key)]
                if department in ex.departments and year == ex.year:
                    domains[ex.code] = [x for x in domains[ex.code] if time != x.time]

            if len(domains[ex.code]) == 0:
                return False


    return True
def make_room_combination_lists(rooms_comb, listNum, listLength):
    """
        Koristi se kad je broj soba veci od 20
    """
    rooms_comb_list = []

    for i in range(listNum):
        l = copy.deepcopy(rooms_comb)
        rooms_comb_list.append(l)
        while len(l) > listLength:
            l.pop(randrange(0, len(l)))
    return rooms_comb_list

#print(room_combination_list)

print("Initializing components...")


def create_combinations(rooms_comb, rooms_cost, rooms_capacity, room_iterables):
    """
        Stvaranje svih mogucih kombinacija svih sala, suma cene i kapaciteta kombinacija


        Parameters
        ----------
        rooms_comb : array of integers
            Indeksi svih soba
        rooms_cost : dictionary
            Cene kombinacija
        rooms_capacity : dictionary
            Kapaciteti kombinacija
        room_iterables : dictionary
            Nizovi indeksa koji predstavljaju kombinaciju

    """
    sum = 0
    for i in range(1,unique_rooms+1):
        for j in itertools.combinations(rooms_comb, i):
            rooms_cost[str(j)] = calculate_cost(j)
            rooms_capacity[str(j)] = calculate_capacity(j)
            room_iterables[str(j)] = j
            sum+=1


def sort_dict(d, reverse = False):
    """
        Sortiraj dictionary po vrednosti

        Parameters
        ----------
        d : dictionary

        Returns
        -------
        dictionary
            Sortirani dict
    """
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))

def print_solution(final_solution):
    """
        Odstampaj resenje i broj bodova

        Parameters
        ----------
        final_solution : dictionary
            Resenje
    """
    score = 0
    for key, val in final_solution.items():
        #print(key + " ")
        for item in val:
            #item.print()
            if item.on_etf == 0:
                score += 1.2
            score += item.on_duty_num
    print("SCORE: "+str(score))

def write_csv(final_solution):
    """
        Ispis .csv fajla

        Parameters
        ----------
        final_solution : dictionary
            Resenje
    """
    #final_solution = sort_solution(final_solution)

    room_arr = []

    for r in rooms:
        if r.name not in room_arr:
            room_arr.append(r.name)

    solution_dict = {}
    for key, val in final_solution.items():
        for room in val:
            solution_dict[room.name+str(room.time)] = key

    csv_writer.write("solution.csv", room_arr, solution_dict, days)

def solution_possible(exams, rooms):
    """
        Proverava da li je moguce doci do resenja na osnovu kapaciteta soba, termina, i broja prijavljenih

        Parameters
        ----------
        exams : array of Exams
        rooms : array of Rooms


        Returns
        -------
        boolean
            True ako je resenje moguce, u suprotnom False
    """
    exam_sum = 0
    room_sum = 0
    for exam in exams:
        exam_sum += exam.applied_num

    for room in rooms:
        room_sum += room.capacity

    return room_sum >= exam_sum

def get_next_room_arr(exam, index, time):
    """
        Uzmi sledeci niz soba za ispit na osnovu vremena
        Uzima niz koji najbolje odgovara trenutnom ispitu po: broju bodova, najmanjoj razlici kapaciteta niza i broja prijavljenih

        Parameters
        ----------
        exam : Exam
            Ispit
        index : integer
            Indeks elementa niza koji je poslednji dodeljen ispitu
        time : integer
            Vreme na osnovu kog se bira sledeci niz

        Returns
        -------
        array of Rooms
            Sobe koje odgovaraju odabranoj kombinaciji

    """
    if index >= len(rooms_cost):
        return None, -1

    i = 0
    for k, v in rooms_cost.items():
        i+=1
        if i < index:
            continue
        if rooms_capacity[k] >= exam.applied_num:
            room_list = []
            for r in room_iterables[k]:
                room_list.append(rooms[r+(int(len(rooms)/(days*4)))*(time-1)])
            return room_list, i+1
    return None, -1

def get_next_time(domain, index):
    """
        Uzmi sledece vreme na osnovu indeksa i domena
        Uzima vreme sa najvise slobodnih mesta

        Parameters
        ----------
        domain : array
            Domen ispita za koji se bira vreme
        index : integer
            Indeks elementa koji je poslednji dodeljen ispitu

        Returns
        -------
        integer
            Vreme
    """
    d = {}
    for r in domain:
        if not r.time in d:
            d[r.time] = 1
        else:
            d[r.time] += 1

    d = sort_dict(d, reverse=True)
    if len(d.values()) <= index or list(d.values())[index] == 0:
        return None

    return list(d.items())[index][0]

def room_in_domain(room,domain):
    """
        Proverava da li se soba nalazi u domenu

        Parameters
        ----------
        room : Room
            Soba koja se proverava
        domain : array
            Domen koji se proverava

        Returns
        -------
        boolean
            True ako se soba nalazi u domenu, u suprotnom false
    """
    for r in domain:
        if r.time == room.time and r.name == room.name:
            return True
    return False

def sort_exams(exams):
    """
        Vrsi podelu ispita na 2 niza (bez i sa racunarima), sortira ta 2 niza i spaja ih u 1 niz tako da se na pocetku nalaze
        ispiti za koje su potrebni racunari

        Parameters
        ----------
        exams : array of Exams
            Niz ispita

        Returns
        -------
        array of Exams
            Sortiran niz ispita
    """
    exams_with_computers = [x for x in exams if x.need_computers == True]
    exams_without_computers = [x for x in exams if x.need_computers == False]

    exams_with_computers.sort()
    exams_without_computers.sort()

    return exams_without_computers + exams_with_computers

# Broj razlicitih soba
unique_rooms = int(len(rooms)/(days*4))

# Dictionary -> broj bodova sala na osnovu kombinacija
rooms_cost = {}
# Dictionary -> kapacitet sala na osnovu kombinacija
rooms_capacity = {}
# Dictionary -> Nizovi indeksa koji predstavljaju kombinaciju
room_iterables = {}

# Lista mogucih indeksa
rooms_comb = list(range(0, unique_rooms))

room_combination_list = make_room_combination_lists(rooms_comb, 1, 15)

# Popunjavanje rooms_cost, rooms_capacity, room_iterables
for comb in room_combination_list:
    create_combinations(comb, rooms_cost, rooms_capacity, room_iterables)

# Ogranicenja za odseke
department_constraints = {}
department_additional_constraints = {}

dep_index = 0
rooms_cost = dict(sorted(rooms_cost.items(), key=lambda kv: rooms_capacity[kv[0]]))

# Sortiraj
rooms_cost = sort_dict(rooms_cost)
rooms_capacity = sort_dict(rooms_capacity)

# Niz linija koraka algoritma

algorithm_steps = []

# Niz vremena
time_arr = ['08:00', '11:30', '15:00', '18:30']

def backtrack_search(exams, domains, final_solution, lvl, department_constraints, department_additional_constraints):
    """
        Rekurzivna pretraga resenja

        Parameters
        ----------
        exams : array of Exams
            Niz ispita
        domains : dictionary
            Domeni svih ispita
        final_solution : dictionary
            Trenutno konacno resenje
        lvl : integer
            Ujedno nivo u stablu i indeks pormenljive
        department_constraints : dictionary
            Key -> ime odseka + godina + dan
            Value -> True
            Ogranicenje : u jednom danu se ne mogu rasporediti 2 ili vise ispita sa iste godine za isti odsek
        department_additional_constraints : dictionary
            Key -> ime odseka + godina + termin
            Value -> True
            Ogranicenje : u jednom terminu se ne mogu rasporediti 2 ili vise ispita iz susednih godina za isti odske

    """

    global cutoff, iterations, final_sol, absolute_min
    if lvl == len(exams):
        return True

    if(len(domains) == 0):
        return False

    exam = exams[lvl]
    found_solution = False

    # Init arr
    if exam.code not in final_solution:
        final_solution[exam.code] = []

    time = 1
    timeIndex = 0
    while time:
        # Uzmi vreme
        time = get_next_time(domains[exam.code], timeIndex)

        if not time:
            break

        timeIndex += 1
        index = 0
        room_arr, index = get_next_room_arr(exam, index, time)
        while room_arr:
            not_in_domain = False
            # Duboke kopije
            new_dom = copy.deepcopy(domains)
            new_dep_constraints = copy.deepcopy(department_constraints)
            new_dep_additional = copy.deepcopy(department_additional_constraints)

            # Add algorithm steps
            step = exam.code + " -> ["
            for room in room_arr:
                step += room.name + "(day: " + str(room.time) + ", time:" + time_arr[(room.time-1)%4]+")" + "| "
            step = step[0:len(step)-2]
            step += "]"
            algorithm_steps.append(step)

            # Za svaku sobu proveri da li je soba u domenu i da li je dodela konzistentna
            for room in room_arr:
                if not room_in_domain(room, domains[exam.code]) or not is_consistent_assignment(exam, room, final_solution[exam.code], new_dep_constraints, new_dep_additional) :
                    not_in_domain = True
                    break
            if not_in_domain :
                room_arr, index = get_next_room_arr(exam, index, time)
                continue
            forward_exit = False
            for room in room_arr:
                # Dodaj sobe kao resenje
                final_solution[exam.code].append(room)

                # Dodaj ogranicenja
                for dep in exam.departments:
                    new_dep_constraints[dep + str(exam.year) + str(int((room.time - 1) / 4))] = True
                    new_dep_additional[dep + str(int(exam.year) - 1) + str(room.time)] = True
                    new_dep_additional[dep + str(int(exam.year) + 1) + str(room.time)] = True

                    # Forward checkig za sobu
                    if not forward_checking(exams, exam, room, new_dom, department_constraints,
                                            department_additional_constraints):
                        forward_exit = True

            # Ako je forward checking prijavio gresku
            if forward_exit:
                room_arr, index = get_next_room_arr(exam, index, time)
                for room in room_arr:
                    final_solution[exam.code].remove(room)
                continue
            new_dom[exam.code] = copy.deepcopy(final_solution[exam.code])

            # Sledeci nivo/premenljiva
            if backtrack_search(exams, new_dom, final_solution, lvl+1, new_dep_constraints, new_dep_additional):
                return True

            for room in room_arr:
                final_solution[exam.code].remove(room)

            room_arr, index = get_next_room_arr(exam, index, time)
    return found_solution

final_solution = {}

# Mandatory
exams = sort_exams(exams)
print("Components initialized!")
print("Component initialization execution time: "+str(time.time() - starting_time))
print("Searching for the solution...")

# Stampaj resenje
if solution_possible(exams,rooms):
    backtrack_search(exams,domains,final_solution,0, department_constraints, department_additional_constraints)
    if solution_valid(final_solution):
        # Ako je pronadjeno resenje
        print("SOLUTION FOUND")
        print_solution(final_solution)
        write_csv(final_solution)
    else:
        print("SOLUTION NOT FOUND")
else:
    print("NOT ENOUGH SPACE")

f = open("algorithm_steps.txt", "w", encoding='utf-8')

iteration = 0
for step in algorithm_steps:
    iteration += 1
    f.write("Step "+str(iteration)+": "+step+"\n")
f.close()


print("Execution time: "+str(time.time() - starting_time))


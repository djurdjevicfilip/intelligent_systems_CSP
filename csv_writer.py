import csv
import numpy as np
def write(file, room_names, solution_dict, days):
    """
    Upisivanje u .csv fajl

    Parametri
    ---------
    file : string
        Ime fajla
    room_names : array of strings
        Niz imena razlicitih sala
    solution_dict : dictionary
        Key -> ime_sale + vreme_sale
        Value -> sifra ispita
    days : integer
        Broj dana
    """

    with open(file, 'w', newline='', encoding='utf-8') as csvfile:
        time_arr = ['08:00', '11:30', '15:00', '18:30']

        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        rows = [[],[],[],[]]
        for day in range(days):
            room_write = ["Day"+str(int(day))]
            for room_name in room_names:
                room_write.append(room_name)
            spamwriter.writerow(room_write)
            rows = [[],[],[],[]]
            for time in range(1, 5):
                rows[time-1] = [time_arr[int(time)-1]]
                for room_name in room_names:
                    key = room_name+str(int(day*4 + time))
                    if key not in solution_dict:
                       rows[time-1].append("X")
                    else:
                       rows[time-1].append(solution_dict[key])
            for row in rows:
                spamwriter.writerow(row)
            spamwriter.writerow([])

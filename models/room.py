class Room:
    """
    Klasa koja predstavlja SALU

    Polja
    -----
    name : string
        Ime sale
    capacity : integer
        Kapacitet sale
    has_computers : integer
       Da li je sala sa racunarima?
    on_duty_num : integer
        Broj dezurnih
    on_etf : integer
        Da li se sala nalazi na etf-u?
    time : integer
        Vreme odrzavanja ispita
        vreme = (dan - 1)*4 + termin, gde je opseg broja termina [1-4]

    Metode
    ------
    print()
        Stampanje sale
    """
    def __init__(self, name, capacity, has_computers, on_duty_num, on_etf, time):
        self.name = name
        self.capacity = capacity
        self.has_computers = has_computers
        self.on_duty_num = on_duty_num
        self.on_etf = on_etf
        self.time = time

    def print(self):
        print(" --- Room --- ")
        print("Name: " + self.name)
        print("Cap: "+str(self.capacity))
        print("Time: "+str(self.time))
        print(" ------------ ")
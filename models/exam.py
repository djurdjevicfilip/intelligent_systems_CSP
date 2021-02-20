class Exam:
    """
    Klasa koja predstavlja ISPIT

    Polja
    -----
    code : string
        Sifra ispita
    applied_num : integer
        Broj prijavljenih studenata
    need_computers : integer
        Da li su za ispit potrebni racunari?
    departments : array of strings
        Niz odseka
    year : integer
        Godina studija u kojoj se ispit odrzava

    Metode
    ------
    __lt__(other)
        Koristi se za sortiranje ispita po broju prijavljenih
    """
    def __init__(self, code, applied_num, need_computers, departments):
        self.code = code
        self.applied_num = applied_num
        self.need_computers = need_computers
        self.departments = departments
        self.year = self.code[5]

    def __lt__(self, other):
        return self.applied_num > other.applied_num


class Term:
    """
    Klasa koja predstavlja ROK

    Polja
    -----
    length : integer
        Duzina trajanja roka
    exams : array of Exams
        Niz ispita

    Metode
    ------
    addExam(exam)
        Dodaj ispit u listu ispita
    """
    def __init__(self, length):
        self.length = length
        self.exams = []

    def addExam(self, exam):
        self.exams.append(exam)
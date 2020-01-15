class Contrat:

    def __init__(self, EOI):

        self.EOI = EOI
        self.element = []
        self.bain = []


    def add_element(self, element):

        self.element.append(element)

    def add_bain(self, bain):

        self.bain.append(bain)


class Contrat_retour:

    def __init__(self, EOI):

        self.EOI = EOI
        self.element = []
        self.bain = []


    def add_element(self, element):

        self.element.append(element)

    def add_bain(self, bain):

        self.bain.append(bain)

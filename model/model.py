import copy

from database.DAO import DAO

class Model:
    def __init__(self):
        self._soluzione = [] #ricorsione
        self._personeSoluzione = 0
        self._listaEventiCondizione = None #non sarebbe servito ma ho voluto aggiungerlo io
        self._listNerc = None
        self._listEvents = None

        self.loadNerc()



    def worstCase(self,maxY, maxH):
        #azzeriamo sempre i record prima di partire
        self._soluzione = []
        self._personeSoluzione = 0
        #inizializzo la ricorsione, passando lista vuota (il parziale che si riempie ogni volta);
        #la lista completa sulla quale faccia ricorsione; i nostri parametri x e y; la posizione / indice per capire a che punto siamo
        self.ricorsione([], self._listaEventiCondizione, maxY, maxH, 0)
        ore_totali = sum(self._calcolaOreEvento(evento) for evento in self._soluzione) #per comodità utilizzo direttamente il mio metodo
        #di prima per calcolare le ore dato un evento, fa solo datafin - datainiz in secondi e poi return secondi / 3600 = ore!
        return self._soluzione, self._personeSoluzione, ore_totali



    def ricorsione(self, parziale, eventi_validi, maxY, maxH, pos):
        #ogni volta che entro qui la parziale si è riempita un po e quindi ha qualche evento al suo interno

        #calcolo clienti in questo parziale
        personeAttuali = sum(evento._customers_affected for evento in parziale) #è un ciclo for su una riga con somma

        #salvo la corrente ricorsione parziale se e solo se i danni / numeri sono maggiori del mio record storico
        if personeAttuali > self._personeSoluzione:
            self._personeSoluzione = personeAttuali
            self._soluzione = copy.deepcopy(parziale) #creo una copia della lista, importantissimo!
            #deepcopy è molto piu lento di list() siccome clona tutto, chiedere a merda Averta

         #caso base ricorsione, controllato tutti sono a fondo lista:
        if pos == len(self._listaEventiCondizione):
                return

        #sennò passo alle due scelte della ricorsione
         #scelta 1, ignoro il corrente e passo alla prossima scelta, pos + 1, posizione successiva
        self.ricorsione(parziale, eventi_validi, maxY, maxH, pos + 1)
        #scelta 2, lo includo
        nuovoEvento = self._listaEventiCondizione[pos]

        #prima di includerlo verifico condizioni di isvalid e (pos + 1) + backtracking
        if self._isValid(parziale, nuovoEvento, maxY, maxH):
            parziale.append(nuovoEvento)
            self.ricorsione(parziale, eventi_validi, maxY, maxH, pos + 1)
            parziale.pop()

    def _isValid(self, parziale, nuovoEvento, maxY, maxH):
        ore_attuali = sum(self._calcolaOreEvento(evento) for evento in parziale)
        ore_nuovo_evento = self._calcolaOreEvento(nuovoEvento)

        #verifica ore < ore massime
        if ore_nuovo_evento + ore_attuali > maxH:
            return False
        #verifica due date piu lontante sia minori del numero anni richiesto dall'utente, differenza di date
        if len(parziale) > 0:
            tutteDate = [evento._date_event_began for evento in parziale]
            #aggiungo l'ultima, la new entry
            tutteDate.append(nuovoEvento._date_event_began)
            #ora faccio differenza in giorni fra data piu recente e quella piu vecchia min e max
            differenza_giorni = (max(tutteDate) - min(tutteDate)).days
            #controllo se rispetta la condizione
            if differenza_giorni > maxY*365:
                return False
        return True

    def _calcolaOreEvento(self, evento):
        differenza_secondi = (evento._date_event_finished - evento._date_event_began).total_seconds()
        return differenza_secondi / 3600

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    def EventiCondizione(self, nerc, ore):
        self._listaEventiCondizione = DAO.getEventiCondizione(nerc, ore)


    @property
    def listNerc(self):
        return self._listNerc


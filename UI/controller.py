import flet as ft
from time import time

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # 1. Recupero i valori crudi (stringhe)
        anni_str = self._view._txtYears.value
        ore_str = self._view._txtHours.value
        nerc_str = self._view._ddNerc.value  # Aggiunto l'underscore corretto

        # 2. Controllo campi vuoti corretto
        if not nerc_str or not anni_str or not ore_str:
            self._view._txtOut.controls.clear()
            self._view._txtOut.controls.append(ft.Text("Attenzione: Compilare tutti i campi!", size=20, color="Red"))
            self._view.update_page()
            return

        # 3. Trasformo anni e ore in NUMERI
        try:
            anni = int(anni_str)
            ore = int(ore_str)
        except ValueError:
            self._view._txtOut.controls.clear()
            self._view._txtOut.controls.append(
                ft.Text("Errore: Anni e Ore devono essere numeri!", size=20, color="Red"))
            self._view.update_page()
            return

        # 4. Estraggo l'oggetto NERC dalla mappa
        nerc = self._idMap[nerc_str]

        self._view._txtOut.controls.clear()
        self._view._txtOut.controls.append(
            ft.Text(f"Selezionato WorstCase per Nerc: {nerc.value} | anni: {anni} | ore: {ore}", size=20,
                    color="Green"))
        self._view.update_page()

        # 5. Chiamo il Model per caricare gli eventi
        # NOTA: Uso il metodo EventiCondizione che hai nel Model per fargli caricare i dati
        self._model.EventiCondizione(nerc, ore)

        # Recupero la lista appena creata per vedere quanti sono
        listaCondizioni = self._model._listaEventiCondizione

        if not listaCondizioni or len(listaCondizioni) == 0:
            self._view._txtOut.controls.append(
                ft.Text("Nessun evento trovato con questi filtri!", size=20, color="Red"))
            self._view.update_page()
            return

        self._view._txtOut.controls.append(
            ft.Text(f"Trovati {len(listaCondizioni)} eventi. Calcolo ricorsione in corso... attendere.",
                    italic=True))
        for ev in listaCondizioni: #stampo la lista che soddisfa solo il campo nerc
            # e durata y ore, nella ricorsione implemento anche condizione anni X, è un po una lista pre ricorsione
            self._view._txtOut.controls.append(ft.Text(f"ID evento : {ev.id} | Clienti afflitti : {ev.customers_affected}")
            )
        self._view.update_page()

        # 6. LANCIO LA RICORSIONE (che ora mi restituisce soluzione e numero clienti)
        inizio = time()
        soluzione, max_clienti, ore_totali_blackout = self._model.worstCase(anni, ore) #l'esercizio chiede sia lista eventi compatibili che somma morti
        fine = time()
        tempo_ricorsione = fine-inizio
        # 7. STAMPO I RISULTATI FINALI
        self._view._txtOut.controls.append(
            ft.Text(f"Calcolo ricorsione terminato in {tempo_ricorsione:.4f} secondi!\n-Clienti massimi coinvolti: {max_clienti}\n"
                    f"-Numero eventi selezionati / compatibili con i filtri: {len(soluzione)}\n"
                    f"-Somma ore totali blackout: {ore_totali_blackout:.2f}", color="green", weight="bold"))

        for ev in soluzione:
            # Sostituisci ev.id con gli attributi reali del tuo oggetto evento
            self._view._txtOut.controls.append(ft.Text(f"ID evento : {ev.id} | Clienti afflitti : {ev.customers_affected} | Data inizio evento: {ev._date_event_began}"
                                                       f"| Data fine evento : {ev._date_event_finished}"))

        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc
        for n in nercList:
            # FONDAMENTALE: Uso n.value (la stringa) come chiave, non l'oggetto intero!
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.value, text=n.value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
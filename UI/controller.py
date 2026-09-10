import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._ratingValue1 = None
        self._ratingValue2 = None

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()  # raccolgo i dati dal database tramite model
        ratingsDDOptions1 = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceRating1),
                                     ratings))  # differenza tra data e key?
        ratingsDDOptions2 = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceRating2), ratings))
        self._view._ddrating1.options = ratingsDDOptions1
        self._view._ddrating2.options = ratingsDDOptions2

    def _choiceRating1(self, e):  # metodo per salvare il valore selezionato dall'utente
        self._ratingValue1 = e.control.data
        print("selezionato rating di partenza " + str(self._ratingValue1))  # per debug

    def _choiceRating2(self, e):
        self._ratingValue2 = e.control.data
        print("selezionato rating di chiusura " + str(self._ratingValue2))

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        if self._ratingValue1 is None or self._ratingValue2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare rating di inizio e di chiusura del range!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._ratingValue1, self._ratingValue2)
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))

        topEdges = self._model.getArchiMaggiori()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))  # in questo caso era top 5
        for u, v, data in topEdges:
            self._view.txt_result.controls.append(ft.Text(f"{u.name} -> {v.name} : {data['weight']}"))

        components, largest = self._model.getConnectedComponents()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(components)} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(largest)}:"))
        for u in largest:
            self._view.txt_result.controls.append(ft.Text(f"{u.name}"))

        self._view.update_page()

    def handleCammino(self, e):
        pass
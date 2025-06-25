import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def fillDDStore(self):
        for i in self._model.getAllStores():
            self._view._ddStore.options.append(ft.dropdown.Option(data=i, text=i.store_name, on_click=self.readStore))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        bool, Nnodes, Nedges = self._model.creaGrafo(self._selectedStore.store_id, self._view._txtIntK.value)
        if bool is True:
            self._view.txt_result.controls.append(ft.Text(f"Creazione grafo eseguita con successo\nNumero nodi: {Nnodes}\nNumero archi: {Nedges}"))
        for i in self._model.getAllNodes(self._selectedStore.store_id):
            self._view._ddNode.options.append(ft.dropdown.Option(data=i, text=i.order_id, on_click=self.readOrder))
        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        cammino, peso = self._model.getCamminoLungo(self._selectedOrder)
        self._view.txt_result.controls.append(ft.Text(f"Trovato cammino di peso {peso}"))
        for i,item in enumerate(cammino, start=1):
            self._view.txt_result.controls.append(ft.Text(f"{i}. {item}"))
        self._view.update_page()


    def handleRicorsione(self, e):
        self._view.txt_result.controls.clear()
        sequenza, costo = self._model.getSequenzaOttima(self._selectedOrder)
        self._view.txt_result.controls.append(ft.Text(f"Ricorsione conclusa con successo\nCosto: {costo}"))
        for i, item in enumerate(sequenza, start=1):
            self._view.txt_result.controls.append(ft.Text(f"{i}. {item}"))
        self._view.update_page()


    def readStore(self, e):
        self._selectedStore = e.control.data

    def readOrder(self, e):
        self._selectedOrder = e.control.data

import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile", width=300)

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento
    input_tipo = ft.TextField(label="Tipo", width=200)
    input_marca = ft.TextField(label="Marca", width=200)
    input_anno = ft.TextField(label="Anno di acquisto", width=150)

    # Contatore valore in euro
    valore_corrente = 100.0
    txt_valore = ft.Text(value=f"{valore_corrente:.1f}", size=16, width=60, text_align=ft.TextAlign.CENTER)

    def decrementa_valore(e):
        nonlocal valore_corrente
        if valore_corrente >= 10.0:
            valore_corrente -= 10.0
            txt_valore.value = f"{valore_corrente:.1f}"
            page.update()

    def incrementa_valore(e):
        nonlocal valore_corrente
        valore_corrente += 10.0
        txt_valore.value = f"{valore_corrente:.1f}"
        page.update()

    btn_meno = ft.Button("-", on_click=decrementa_valore)
    btn_piu = ft.Button("+", on_click=incrementa_valore)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    def aggiungi_strumento(e):
        nonlocal valore_corrente
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno_str = input_anno.value.strip()

        if not tipo or not marca or not anno_str:
            alert.show_alert("Compilare tutti i campi per aggiungere il nuovo strumento.")
            return

        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("Il campo anno di acquisto deve essere un numero intero valido.")
            return

        valore = float(valore_corrente)

        try:
            deposito.aggiungi_strumento(tipo, marca, anno, valore)
        except Exception as ex:
            alert.show_alert(str(ex))
            return

        # Svuota i campi e resetta il valore
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        valore_corrente = 100.0
        txt_valore.value = f"{valore_corrente:.1f}"

        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)
    pulsante_aggiungi = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=20,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(spacing=20,
               controls=[input_tipo, input_marca, input_anno],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=10,
               controls=[ft.Text("Valore (€):"), btn_meno, txt_valore, btn_piu, pulsante_aggiungi],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        ft.Container(content=lista_strumenti, height=250, expand=True),
    )
    aggiorna_lista_strumenti()

ft.run(main)
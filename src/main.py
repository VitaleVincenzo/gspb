#!/usr/bin/env python3
# =============================================================================
# PROGETTO FINALE DI PROGRAMMAZIONE - SISTEMA GESTIONE SPESE E BUDGET
# Autore: Vincenzo Vitale
# File: src/main.py
# Descrizione: Applicazione console per la gestione di spese personali,
#              categorie e budget mensile con persistenza su database SQLite.
# =============================================================================

import os
import sqlite3
from datetime import datetime

# Percorso del file database SQLite
DB_NAME = "spese.db"


def connetti_db():
    """
    Stabilisce la connessione con il database SQLite e abilita
    il supporto per i vincoli di chiave esterna (FOREIGN KEY).
    """
    if not os.path.exists(DB_NAME):
        print(f"Attenzione: il file database '{DB_NAME}' non esiste.")
        print("Esegui prima da terminale: sqlite3 spese.db < sql/database.sql\n")
        return

    conn = sqlite3.connect(DB_NAME)
    # Attiva il vincolo FOREIGN KEY in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def modulo_gestione_categorie(conn):
    """
    Consente all'utente di inserire una nuova categoria di spesa.
    Effettua la verifica che il nome non sia vuoto e che non esista gia'.
    """
    print("\n--- GESTIONE CATEGORIE ---")
    nome_categoria = input("Inserisci il nome della categoria: ").strip()

    # 1. Verifica che il nome non sia vuoto
    if not nome_categoria:
        print("Errore: Il nome della categoria non puo' essere vuoto.")
        return

    cursor = conn.cursor()

    # 2. Controllo dell'esistenza della categoria (SQL SELECT)
    cursor.execute("SELECT id FROM categorie WHERE LOWER(nome) = LOWER(?);", (nome_categoria,))
    risultato = cursor.fetchone()

    if risultato is not None:
        # Se trovata, segnalo l'errore
        print("Errore: La categoria esiste già.")
        return

    # 3. Inserimento della nuova categoria (SQL INSERT)
    try:
        cursor.execute("INSERT INTO categorie (nome) VALUES (?);", (nome_categoria,))
        conn.commit()
        print("Categoria inserita correttamente.")
    except sqlite3.Error as e:
        print(f"Errore durante l'inserimento: {e}")


def modulo_inserisci_spesa(conn):
    """
    Consente la registrazione di una spesa con data, importo, categoria
    ed eventuale descrizione facoltativa.
    """
    print("\n--- INSERISCI SPESA ---")

    # 1. Acquisizione della data
    data_str = input("Inserisci la data (YYYY-MM-DD): ").strip()
    try:
        # Validazione formale della data
        datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        print("Errore: Formato data non valido. Usare il formato YYYY-MM-DD (es. 2025-01-15).")
        return

    # 2. Acquisizione e validazione dell'importo
    importo_str = input("Inserisci l'importo: ").strip()
    try:
        importo = float(importo_str.replace(",", "."))
    except ValueError:
        print("Errore: Inserire un valore numerico valido per l'importo.")
        return

    if importo <= 0:
        print("Errore: l’importo deve essere maggiore di zero.")
        return

    # 3. Acquisizione e verifica dell'esistenza della categoria
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categorie WHERE LOWER(nome) = LOWER(?);", (nome_categoria,))
    riga = cursor.fetchone()

    if riga is None:
        print("Errore: la categoria non esiste.")
        return

    categoria_id = riga[0]

    # 4. Descrizione facoltativa
    descrizione = input("Inserisci una descrizione (facoltativa): ").strip()
    if not descrizione:
        descrizione = None

    # 5. Inserimento della spesa nel database (SQL INSERT con chiave esterna)
    try:
        cursor.execute("""
            INSERT INTO spese (data, importo, categoria_id, descrizione)
            VALUES (?, ?, ?, ?);
        """, (data_str, importo, categoria_id, descrizione))
        conn.commit()
        print("Spesa inserita correttamente.")
    except sqlite3.Error as e:
        print(f"Errore database: {e}")

def modulo_definisci_budget(conn):
    """
    Imposta o aggiorna il limite di spesa per una categoria in un determinato mese.
    """
    print("\n--- DEFINISCI BUDGET MENSILE ---")

    # 1. Acquisizione e controllo mese
    mese_str = input("Inserisci il mese (YYYY-MM): ").strip()
    try:
        datetime.strptime(mese_str, "%Y-%m")
    except ValueError:
        print("Errore: Formato mese non valido. Usare il formato YYYY-MM (es. 2025-01).")
        return

    # 2. Acquisizione e verifica esistenza categoria
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categorie WHERE LOWER(nome) = LOWER(?);", (nome_categoria,))
    riga = cursor.fetchone()

    if riga is None:
        print("Errore: la categoria non esiste.")
        return

    categoria_id = riga[0]

    # 3. Acquisizione e verifica che il budget sia maggiore di zero
    budget_str = input("Inserisci l'importo del budget: ").strip()
    try:
        importo_budget = float(budget_str.replace(",", "."))
    except ValueError:
        print("Errore: Inserire un valore numerico valido per il budget.")
        return

    if importo_budget <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return

    # 4. Inserimento o aggiornamento del record di budget
    cursor.execute("""
        SELECT id FROM budget WHERE mese = ? AND categoria_id = ?;
    """, (mese_str, categoria_id))
    budget_esistente = cursor.fetchone()

    try:
        if budget_esistente:
            # Aggiornamento se gia' presente per questo mese
            cursor.execute("""
                UPDATE budget SET importo = ? WHERE id = ?;
            """, (importo_budget, budget_esistente[0]))
        else:
            # Nuovo inserimento
            cursor.execute("""
                INSERT INTO budget (mese, categoria_id, importo)
                VALUES (?, ?, ?);
            """, (mese_str, categoria_id, importo_budget))

        conn.commit()
        print("Budget mensile salvato correttamente.")
    except sqlite3.Error as e:
        print(f"Errore database: {e}")

def report_totale_per_categoria(conn):
    """
    REPORT 1: Calcola e mostra la somma totale delle spese per ogni categoria.
    """
    print("\n--- REPORT 1: Totale delle Spese per Categoria ---")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.nome, SUM(s.importo) AS totale
        FROM categorie c
        JOIN spese s ON c.id = s.categoria_id
        GROUP BY c.id, c.nome
        ORDER BY c.nome;
    """)
    righe = cursor.fetchall()

    if not righe:
        print("Nessuna spesa registrata nel sistema.")
        return

    print(f"{'Categoria':<20} Totale Speso")
    print("-" * 35)
    for nome, totale in righe:
        # Formattazione puntata simile all'esempio della traccia
        punti = "." * max(1, 20 - len(nome))
        print(f"{nome}{punti}{totale:.2f}")


def report_spese_vs_budget(conn):
    """
    REPORT 2: Confronta le spese effettive di un mese e categoria con il budget.
    Stampa se il budget e' stato superato o rispettato tramite if/else.
    """
    print("\n--- REPORT 2: Spese Mensili vs Budget ---")
    mese = input("Inserisci il mese da verificare (YYYY-MM): ").strip()
    categoria_nome = input("Inserisci la categoria: ").strip()

    cursor = conn.cursor()

    # Recupero l'ID della categoria
    cursor.execute("SELECT id, nome FROM categorie WHERE LOWER(nome) = LOWER(?);", (categoria_nome,))
    cat = cursor.fetchone()
    if cat is None:
        print("Errore: la categoria non esiste.")
        return

    categoria_id, nome_ufficiale = cat[0], cat[1]

    # Recupero il budget per il mese e la categoria selezionata
    cursor.execute("""
        SELECT importo FROM budget
        WHERE mese = ? AND categoria_id = ?;
    """, (mese, categoria_id))
    riga_budget = cursor.fetchone()

    if riga_budget is None:
        print(f"Nessun budget impostato per la categoria '{nome_ufficiale}' nel mese {mese}.")
        return

    budget_val = riga_budget[0]

    # Calcolo del totale speso per mese e categoria (SQL)
    cursor.execute("""
        SELECT COALESCE(SUM(importo), 0.0)
        FROM spese
        WHERE categoria_id = ? AND strftime('%Y-%m', data) = ?;
    """, (categoria_id, mese))
    totale_speso = cursor.fetchone()[0]

    # Confronto con il budget tramite if / else
    if totale_speso > budget_val:
        stato = "SUPERAMENTO BUDGET"
    else:
        stato = "NEL BUDGET"

    # Visualizzazione dei risultati esattamente come nell'esempio della traccia
    print(f"\nMese: {mese}")
    print(f"Categoria: {nome_ufficiale}")
    print(f"Budget: {budget_val:.2f}")
    print(f"Speso: {totale_speso:.2f}")
    print(f"Stato: {stato}")


def report_elenco_completo_spese(conn):
    """
    REPORT 3: Mostra l'elenco cronologico di tutte le spese registrate.
    """
    print("\n--- REPORT 3: Elenco Completo delle Spese ---")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '')
        FROM spese s
        JOIN categorie c ON s.categoria_id = c.id
        ORDER BY s.data ASC, s.id ASC;
    """)
    righe = cursor.fetchall()

    if not righe:
        print("Nessuna spesa presente nel database.")
        return

    print("Data        Categoria            Importo   Descrizione")
    print("-" * 62)
    for data, cat, importo, desc in righe:
        print(f"{data:<11} {cat:<20} {importo:<9.2f} {desc}")


def modulo_visualizza_report(conn):
    """
    Gestisce il sottomenu dei report richiesto dalla traccia.
    """
    while True:
        print("\nMenu dei Report")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")

        scelta = input("Inserisci la tua scelta: ").strip()

        # Selezione del caso tramite switch (match / case)
        match scelta:
            case "1":
                report_totale_per_categoria(conn)
            case "2":
                report_spese_vs_budget(conn)
            case "3":
                report_elenco_completo_spese(conn)
            case "4":
                # Ritorna al menu principale
                break
            case _:
                print("Scelta non valida. Riprovare.")


def main():
    """
    Funzione principale del programma.
    Gestisce l'avvio, il ciclo del menu e la chiusura della connessione.
    """
    # 1. Messaggio di benvenuto all'avvio
    print("=========================================")
    print(" Benvenuto nel Sistema di Gestione Spese ")
    print("=========================================")

    # Connessione al database SQLite
    conn = connetti_db()
    if not conn:
        return

    # 2. Ciclo iterativo per ripetere il menu fino all'uscita (scelta 5)
    while True:
        print("\n-------------------------")
        print("SISTEMA SPESE PERSONALI")
        print("-------------------------")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("-------------------------")

        scelta = input("Inserisci la tua scelta: ").strip()

        # Logica del menu tramite selezione con switch (match / case)
        match scelta:
            case "1":
                modulo_gestione_categorie(conn)
            case "2":
                modulo_inserisci_spesa(conn)
            case "3":
                modulo_definisci_budget(conn)
            case "4":
                modulo_visualizza_report(conn)
            case "5":
                print("\nChiusura dell'applicazione. Arrivederci!")
                break
            case _:
                # Messaggio obbligatorio da specifiche del professore
                print("Scelta non valida. Riprovare.")

    # Chiusura corretta della connessione
    conn.close()


if __name__ == "__main__":
    main()

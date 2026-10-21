# Sistema di Gestione delle Spese Personali e del Budget

Progetto finale per il corso di **Programmazione / Fondamenti di Informatica**  
Corso di Laurea in Ingegneria Informatica.

---

## 1. Descrizione del Progetto

L'applicazione è un sistema basato su console (interfaccia a riga di comando) per la gestione finanziaria personale di un singolo utente. Il programma permette di:
- Gestire le categorie di spesa (es. Alimentari, Trasporti, Salute, Svago).
- Registrare le spese giornaliere specificando data, importo, categoria e descrizione facoltativa.
- Impostare limiti di spesa mensili (budget) per ciascuna categoria.
- Visualizzare report riepilogativi generati tramite query SQL relazionali (totale spesa per categoria, confronto spese vs budget con alert di superamento, ed elenco cronologico completo).

La persistenza dei dati è gestita tramite un database relazionale **SQLite**, con vincoli di integrità referenziale (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`, `NOT NULL`) attivi e verificati.

---

## 2. Requisiti per l'Esecuzione

- **Interprete**: **Python 3.10 o versione successiva** (requisito minimo obbligatorio per il supporto al costrutto nativo `match / case` introdotto con PEP 634 per la selezione dei menu tramite switch).
- **Librerie esterne**: *Nessuna libreria esterna richiesta.*  
  Il progetto fa uso esclusivo delle seguenti librerie standard di Python:
  - `sqlite3`: per la gestione della connessione e l'esecuzione di query SQL relazionali.
  - `datetime`: per la validazione dei formati data (`YYYY-MM-DD`) e mese (`YYYY-MM`).
  - `os`: per la gestione dei percorsi dei file in modo indipendente dal sistema operativo.

---

## 3. Istruzioni per l'Esecuzione

### a) Clonazione del Repository
Clonare il repository sul proprio computer e accedere alla cartella del progetto:
```bash
git clone https://github.com/nomeutente/PersonalExpenseSystem.git
cd PersonalExpenseSystem
```

### b) Istruzioni di Compilazione
Trattandosi di un programma scritto in linguaggio interpretato (Python), **non è richiesta alcuna fase di compilazione preventiva**.

### c) Creazione del Database
Prima di avviare l'applicazione per la prima volta, generare e popolare il database SQLite eseguendo da terminale:
```bash
sqlite3 spese.db < sql/database.sql
```
Questo comando crea il file `spese.db` con tutte le tabelle, i vincoli di integrità e i dati di esempio.

### d) Istruzioni di Avvio del Programma
Per avviare l'applicazione, eseguire il seguente **comando esatto da terminale**:

```bash
python3 src/main.py
```

*(Su ambienti Windows in cui il comando `python3` non è configurato, utilizzare `python src/main.py`).*

---

## 4. Struttura del Repository

In conformità con le specifiche di consegna:

```text
PersonalExpenseSystem/
├── src/
│   └── main.py          # Codice sorgente dell'applicazione console
├── sql/
│   └── database.sql     # Script SQL con DDL (CREATE TABLE con vincoli) e DML (INSERT)
├── demo/
│   └── demo_video.mp4   # Video dimostrativo del funzionamento
└── README.md            # Documentazione con requisiti e istruzioni di esecuzione
```

---

## 5. Dati di Esempio e Casi di Test

Il file `sql/database.sql` include dati di test per verificare immediatamente il comportamento dei report:
- **Alimentari (Ottobre 2026)**: Budget = 300.00 €, Speso = 320.00 € $\rightarrow$ **SUPERAMENTO BUDGET**
- **Trasporti (Ottobre 2026)**: Budget = 150.00 €, Speso = 120.00 € $\rightarrow$ **NEL BUDGET**

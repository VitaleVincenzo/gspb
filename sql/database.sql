-- =====================================================================
-- ELABORATO FINALE DI PROGRAMMAZIONE (Fondamenti di Informatica)
-- Progetto: Sistema di Gestione delle Spese Personali e del Budget
-- Autore: Vincenzo Vitale
-- File: sql/database.sql
-- =====================================================================

-- Abilitazione del controllo delle chiavi esterne per SQLite
PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- 1. TABELLA: categorie
-- Contiene le categorie di spesa (es. Alimentari, Trasporti).
-- Vincoli espliciti:
-- - PRIMARY KEY (id)
-- - NOT NULL e UNIQUE sul nome della categoria
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

-- ---------------------------------------------------------------------
-- 2. TABELLA: spese
-- Registra le singole spese sostenute dall'utente.
-- Vincoli espliciti:
-- - PRIMARY KEY (id)
-- - NOT NULL su data, importo e categoria_id
-- - CHECK sull'importo (deve essere strettamente positivo)
-- - FOREIGN KEY verso la tabella categorie
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    categoria_id INTEGER NOT NULL,
    descrizione TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- ---------------------------------------------------------------------
-- 3. TABELLA: budget
-- Definisce il limite di spesa mensile per ciascuna categoria.
-- Vincoli espliciti:
-- - PRIMARY KEY (id)
-- - NOT NULL su mese, categoria_id e importo
-- - CHECK sull'importo del budget (deve essere maggiore di zero)
-- - FOREIGN KEY verso la tabella categorie
-- - UNIQUE su (mese, categoria_id) per evitare definizioni duplicate
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    UNIQUE (mese, categoria_id),
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- Inserimento Categorie iniziali
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Svago');
INSERT INTO categorie (nome) VALUES ('Bollette');

-- Inserimento Budget per il mese 2026-10
INSERT INTO budget (mese, categoria_id, importo) VALUES ('2026-10', 1, 300.00);
INSERT INTO budget (mese, categoria_id, importo) VALUES ('2026-10', 2, 150.00);

-- Inserimento Spese di esempio (anno-mese 2026-10)
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-10-05', 120.00, 1, 'Spesa settimanale supermercato');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-10-12', 175.00, 1, 'Spesa macelleria e mercato');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-10-15', 25.00, 1, 'Pranzo');

INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-10-10', 50.00, 2, 'Rifornimento carburante');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-10-17', 70.00, 2, 'Abbonamento mezzi pubblici');

INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-10-16', 35.50, 3, 'Cinema e pizza');

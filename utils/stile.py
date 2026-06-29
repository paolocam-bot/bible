# utils/stile.py
import customtkinter as ctk

class Stile:
    # ==========================================
    # 1. GEOMETRIE E FONT UNIFICATI
    # ==========================================
    CORNER_RADIUS_INPUT = 6   # Per Entry, ComboBox, Pulsanti piccoli
    CORNER_RADIUS_CARD = 8    # Per schede statistiche, riquadri interni
    CORNER_RADIUS_BADGE = 12  # Per i badge degli stati (effetto pillola)
    
    FONT_TITOLO = ("Segoe UI", 22, "bold")
    FONT_SUBTITLE = ("Segoe UI", 14, "bold")
    FONT_NORMALE = ("Segoe UI", 12, "normal")
    FONT_BADGE = ("Segoe UI", 11, "bold")

    # ==========================================
    # 2. COLORI DI BACKGROUND E TESTO
    # ==========================================
    BG_PRINCIPALE = ("#f8fafc", "#0f172a") # Sfondo finestre vuote
    BG_CARD = ("#ffffff", "#1e293b")       # Sfondo schede e form
    
    TEXT_MAIN = ("#1e293b", "#f8fafc")     # Scritte principali
    TEXT_MUTED = ("#64748b", "#94a3b8")    # Scritte secondarie / Placeholder

    # ==========================================
    # 3. STILE DEI PULSANTI (ELEMENTI ATTIVI)
    # ==========================================
    # Pulsante Primario (Es. Inserisci, Salva, Conferma)
    BTN_PRIMARY_BG = ("#3b82f6", "#2563eb")
    BTN_PRIMARY_HOVER = ("#2563eb", "#1d4ed8")
    BTN_PRIMARY_TEXT = ("#ffffff", "#ffffff")

    # Pulsante Secondario / Annulla
    BTN_SECONDARY_BG = ("#e2e8f0", "#334155")
    BTN_SECONDARY_HOVER = ("#cbd5e1", "#475569")
    BTN_SECONDARY_TEXT = ("#1e293b", "#f8fafc")

    # ==========================================
    # 4. STATI SEMANTICI (SFONDO, TESTO)
    # ==========================================
    # Ritorna una tupla: (Colore Sfondo, Colore Testo)
    @classmethod
    def ottieni_stile_stato(cls, stato):
        stato_str = str(stato).lower()
        if "risolto" in stato_str or "completato" in stato_str:
            return ("#d1e7dd", "#064e3b"), ("#0f5132", "#34d399")
        elif "da finire" in stato_str or "in attesa" in stato_str:
            return ("#ffe5d0", "#7c2d12"), ("#a04000", "#fb923c")
        elif "eliminato" in stato_str or "pericolo" in stato_str:
            return ("#f8d7da", "#7f1d1d"), ("#842029", "#fca5a5")
        else:
            return ("#e2e8f0", "#334155"), ("#1e293b", "#f8fafc")
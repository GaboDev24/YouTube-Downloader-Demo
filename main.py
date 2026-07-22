import math
import os
import re
import sys
import threading
import subprocess
import tkinter as tk
from io import BytesIO
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
import requests
import yt_dlp
from PIL import Image

# ── Appearance ────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ──────────────────────────────────────────────────────────────────────────────
#  Sistema Táctico — Paleta de colores (DESIGN.md)
# ──────────────────────────────────────────────────────────────────────────────
RED        = "#A30000"
RED_DARK   = "#6B0000"
RED_MED    = "#c40000"
BLACK      = "#000000"
OFF_WHITE  = "#F5F5F5"
GRAY_DARK  = "#121212"
STEEL      = "#2A2A2A"
STEEL_MID  = "#1A1A1A"
BORDER     = "#330000"          # rgba(163,0,0,0.2) aproximado
BORDER_MID = "#1a0000"

GREEN_OK   = "#22c55e"
YELLOW_W   = "#f59e0b"
BLUE_INFO  = "#38bdf8"

# ── YouTube URL regex ─────────────────────────────────────────────────────────
YOUTUBE_RE = re.compile(
    r'(https?://)?(www\.)?'
    r'(youtube\.com/(watch|shorts|embed|v)/|youtu\.be/)'
    r'[\w\-]{1,20}'
    r'([?&]\S*)?'
)


def get_downloads_dir() -> str:
    """Returns a reliable downloads folder regardless of run location."""
    base = Path.home() / "Downloads" / "YT-Downloader"
    base.mkdir(parents=True, exist_ok=True)
    return str(base)


# ──────────────────────────────────────────────────────────────────────────────
#  Título animado — pulso rojo táctico
# ──────────────────────────────────────────────────────────────────────────────
class AnimatedTitle(ctk.CTkCanvas):
    """
    Canvas that draws an animated pulsing red title.
    Mimics the tactical system glow effect.
    """
    def __init__(self, master, text="YT DOWNLOADER", **kwargs):
        super().__init__(master, bg=BLACK, highlightthickness=0, height=62, **kwargs)
        self._text = text
        self._step = 0
        self._draw()

    def _draw(self):
        self.delete("all")
        self._step = (self._step + 2) % 360
        t = (math.sin(math.radians(self._step)) + 1) / 2   # 0 → 1

        # Pulse between RED and RED_DARK
        r1, g1, b1 = 0xA3, 0x00, 0x00
        r2, g2, b2 = 0xC4, 0x00, 0x00
        r = int(r1 + (r2 - r1) * t)
        color = f"#{r:02x}0000"

        w = self.winfo_width() or 520
        cx = w // 2

        # Glow shadow layers
        self.create_text(cx + 2, 34, text=self._text,
                         font=("Courier New", 18, "bold"),
                         fill="#300000", anchor="center")
        self.create_text(cx + 1, 33, text=self._text,
                         font=("Courier New", 18, "bold"),
                         fill="#500000", anchor="center")
        # Main text
        self.create_text(cx, 32, text=self._text,
                         font=("Courier New", 18, "bold"),
                         fill=color, anchor="center")

        # Subtitle eyebrow — monospace tag
        sub_color = f"#{int(0x33 + t * 0x22):02x}0000"
        self.create_text(cx, 54, text="// VIDEO DOWNLOADER  ·  GABODEV",
                         font=("Courier New", 8),
                         fill=sub_color, anchor="center")

        self.after(35, self._draw)


# ──────────────────────────────────────────────────────────────────────────────
#  Scanlines overlay — efecto CRT táctico
# ──────────────────────────────────────────────────────────────────────────────
class ScanlinesOverlay(tk.Canvas):
    """Transparent canvas overlay that draws horizontal CRT scanlines."""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="", highlightthickness=0,
                         bd=0, **kwargs)
        self.bind("<Configure>", self._redraw)

    def _redraw(self, event=None):
        self.delete("all")
        h = self.winfo_height()
        w = self.winfo_width()
        for y in range(0, h, 4):
            self.create_line(0, y, w, y, fill="#050000", width=1)


# ──────────────────────────────────────────────────────────────────────────────
#  Punto de pulso — indicador de estado
# ──────────────────────────────────────────────────────────────────────────────
class PulseDot(tk.Canvas):
    def __init__(self, master, color=RED, bg=STEEL_MID, **kwargs):
        super().__init__(master, bg=bg, highlightthickness=0,
                         width=10, height=10, **kwargs)
        self._color  = color
        self._bg_hex = bg
        self._step   = 0
        self._draw()

    def set_color(self, color: str, bg: str = None):
        self._color = color
        if bg:
            self._bg_hex = bg
            self.configure(bg=bg)

    def _hex_to_rgb(self, h: str):
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    def _draw(self):
        self.delete("all")
        self._step = (self._step + 3) % 360
        t = (math.sin(math.radians(self._step)) + 1) / 2
        # Blend dot color with bg for pulse effect
        cr, cg, cb = self._hex_to_rgb(self._color)
        br, bg_, bb = self._hex_to_rgb(self._bg_hex)
        alpha = 0.45 + t * 0.55
        r = int(br + (cr - br) * alpha)
        g = int(bg_ + (cg - bg_) * alpha)
        b = int(bb + (cb - bb) * alpha)
        blended = f"#{r:02x}{g:02x}{b:02x}"
        self.create_oval(1, 1, 9, 9, fill=blended, outline="")
        self.after(40, self._draw)


# ──────────────────────────────────────────────────────────────────────────────
#  Card táctica — bordes rojos, esquinas rectas, bg oscuro
# ──────────────────────────────────────────────────────────────────────────────
class TacticalCard(ctk.CTkFrame):
    """Card styled after the tactical system: sharp corners, red border."""
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color",      STEEL_MID)
        kwargs.setdefault("corner_radius", 0)
        kwargs.setdefault("border_color",  BORDER)
        kwargs.setdefault("border_width",  1)
        super().__init__(master, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
#  Cabecera de card — estilo terminal con dots macOS
# ──────────────────────────────────────────────────────────────────────────────
class CardHeader(ctk.CTkFrame):
    def __init__(self, master, label: str = "", **kwargs):
        super().__init__(master, fg_color="#0a0000",
                         corner_radius=0, **kwargs)
        # macOS-style dots
        dots_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        dots_frame.pack(side="left", padx=(10, 8), pady=8)
        for color in ("#ff5f57", "#febc2e", "#28c840"):
            dot = tk.Canvas(dots_frame, width=9, height=9, bg="#0a0000",
                            highlightthickness=0)
            dot.create_oval(0, 0, 8, 8, fill=color, outline="")
            dot.pack(side="left", padx=2)
        if label:
            ctk.CTkLabel(
                self, text=label,
                text_color="#330000",
                font=("Courier New", 9),
            ).pack(side="left", padx=4)


# ──────────────────────────────────────────────────────────────────────────────
#  Badge de estado táctico
# ──────────────────────────────────────────────────────────────────────────────
class StatusBadge(ctk.CTkFrame):
    """
    Pill-shaped tactical status indicator.
    States: idle, loading, ready, downloading, done, error
    """
    _STATES = {
        "idle":        (RED,      "STANDBY"),
        "loading":     (YELLOW_W, "CARGANDO"),
        "ready":       (GREEN_OK, "LISTO"),
        "downloading": (BLUE_INFO,"DESCARGANDO"),
        "done":        (GREEN_OK, "COMPLETADO"),
        "error":       (RED,      "ERROR"),
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=STEEL_MID,
                         corner_radius=0, **kwargs)
        # Left red accent bar
        ctk.CTkFrame(self, width=3, fg_color=RED,
                     corner_radius=0).pack(side="left", fill="y")

        self._dot = PulseDot(self, color=RED, bg=STEEL_MID)
        self._dot.pack(side="left", padx=(8, 4), pady=8)

        self._lbl = ctk.CTkLabel(
            self, text="STANDBY",
            text_color=RED,
            font=("Courier New", 10, "bold"),
        )
        self._lbl.pack(side="left", padx=(0, 14), pady=8)
        self.set("idle")

    def set(self, key: str, msg: str = ""):
        color, default_text = self._STATES.get(key, (RED, key.upper()))
        display = msg.upper() if msg else default_text
        self._dot.set_color(color, STEEL_MID)
        self._lbl.configure(text=display, text_color=color)


# ──────────────────────────────────────────────────────────────────────────────
#  Label táctica
# ──────────────────────────────────────────────────────────────────────────────
def tac_label(parent, text: str, **kwargs) -> ctk.CTkLabel:
    """Monospace uppercase label matching the tactical system."""
    kwargs.setdefault("text_color", RED)
    kwargs.setdefault("font", ("Courier New", 9))
    return ctk.CTkLabel(parent, text=text.upper(), **kwargs)


def body_label(parent, text: str, **kwargs) -> ctk.CTkLabel:
    """Body text label."""
    kwargs.setdefault("text_color", "#888888")
    kwargs.setdefault("font", ("Courier New", 10))
    return ctk.CTkLabel(parent, text=text, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
#  Separador táctico
# ──────────────────────────────────────────────────────────────────────────────
class TacSeparator(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("height", 1)
        kwargs.setdefault("fg_color", BORDER)
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
#  Botón táctico — rojo primario con glow / ghost secundario
# ──────────────────────────────────────────────────────────────────────────────
def tac_button_primary(parent, text: str, command, width=180, height=42, **kwargs):
    return ctk.CTkButton(
        parent, text=text.upper(), command=command,
        width=width, height=height,
        fg_color=RED,
        hover_color=RED_MED,
        text_color=OFF_WHITE,
        font=("Courier New", 11, "bold"),
        corner_radius=0,
        border_width=0,
        **kwargs,
    )


def tac_button_ghost(parent, text: str, command, width=180, height=42, **kwargs):
    return ctk.CTkButton(
        parent, text=text.upper(), command=command,
        width=width, height=height,
        fg_color="transparent",
        hover_color=STEEL,
        border_color=BORDER,
        border_width=1,
        text_color="#555555",
        font=("Courier New", 11, "bold"),
        corner_radius=0,
        **kwargs,
    )


# ──────────────────────────────────────────────────────────────────────────────
#  Campo de entrada táctico
# ──────────────────────────────────────────────────────────────────────────────
def tac_entry(parent, placeholder: str = "", **kwargs):
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        placeholder_text_color="#330000",
        fg_color=GRAY_DARK,
        border_color=BORDER,
        border_width=1,
        text_color=OFF_WHITE,
        font=("Courier New", 11),
        corner_radius=0,
        **kwargs,
    )


# ──────────────────────────────────────────────────────────────────────────────
#  Aplicación principal
# ──────────────────────────────────────────────────────────────────────────────
class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YT DOWNLOADER  //  GABODEV")
        self.geometry("560x820")
        self.minsize(480, 580)
        self.configure(fg_color=BLACK)
        self.resizable(True, True)

        self.video_info      = None
        self.download_dir    = get_downloads_dir()
        self._is_downloading = False
        self._open_btn_shown = False

        self._setup_ui()

    # ── UI Construction ───────────────────────────────────────────────────────
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Scrollable container ──────────────────────────────────────────────
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=BLACK,
            corner_radius=0,
            scrollbar_button_color=STEEL,
            scrollbar_button_hover_color=RED,
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure(0, weight=1)
        sf = self._scroll   # shorthand

        # ── HUD top bar ───────────────────────────────────────────────────────
        hud_bar = ctk.CTkFrame(sf, fg_color=STEEL_MID, corner_radius=0, height=28)
        hud_bar.grid(row=0, column=0, sticky="ew")
        hud_bar.grid_propagate(False)
        hud_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            hud_bar, text="◀  SISTEMA DE DESCARGA",
            text_color=RED,
            font=("Courier New", 8),
        ).grid(row=0, column=0, padx=12, pady=6, sticky="w")

        ctk.CTkLabel(
            hud_bar, text="GABODEV  //  v2.0",
            text_color="#2a0000",
            font=("Courier New", 8),
        ).grid(row=0, column=2, padx=12, pady=6, sticky="e")

        # ── Animated header ───────────────────────────────────────────────────
        self.animated_title = AnimatedTitle(sf, text="YT DOWNLOADER")
        self.animated_title.grid(row=1, column=0, sticky="ew",
                                 padx=0, pady=(0, 0))

        # ── Status badge ──────────────────────────────────────────────────────
        status_row = ctk.CTkFrame(sf, fg_color=BLACK, corner_radius=0)
        status_row.grid(row=2, column=0, sticky="ew", padx=20, pady=(8, 4))
        status_row.grid_columnconfigure(1, weight=1)

        self.status_badge = StatusBadge(status_row)
        self.status_badge.grid(row=0, column=0, sticky="w")

        # Decorative right-side line
        ctk.CTkFrame(status_row, height=1, fg_color=BORDER,
                     corner_radius=0).grid(
            row=0, column=1, sticky="ew", padx=(12, 0), pady=14)

        # ── URL Card ──────────────────────────────────────────────────────────
        url_card = TacticalCard(sf)
        url_card.grid(row=3, column=0, padx=20, pady=(4, 6), sticky="ew")
        url_card.grid_columnconfigure(0, weight=1)

        CardHeader(url_card, label="INPUT.URL").grid(
            row=0, column=0, sticky="ew")

        tac_label(url_card, "// Enlace del video").grid(
            row=1, column=0, padx=14, pady=(10, 4), sticky="w")

        url_inner = ctk.CTkFrame(url_card, fg_color="transparent",
                                 corner_radius=0)
        url_inner.grid(row=2, column=0, padx=10, pady=(0, 6), sticky="ew")
        url_inner.grid_columnconfigure(0, weight=1)

        self.url_entry = tac_entry(
            url_inner,
            placeholder="https://www.youtube.com/watch?v=...",
            height=42,
        )
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.url_entry.bind("<Return>", lambda _: self.load_video_info())

        self.load_btn = tac_button_primary(
            url_inner, "CARGAR",
            command=self.load_video_info,
            width=88, height=42,
        )
        self.load_btn.grid(row=0, column=1)

        body_label(url_card, "  Admite: youtube.com/watch  ·  youtu.be  ·  /shorts").grid(
            row=3, column=0, padx=14, pady=(0, 12), sticky="w")

        # ── Destination Card ──────────────────────────────────────────────────
        dest_card = TacticalCard(sf)
        dest_card.grid(row=4, column=0, padx=20, pady=6, sticky="ew")
        dest_card.grid_columnconfigure(1, weight=1)

        CardHeader(dest_card, label="OUTPUT.PATH").grid(
            row=0, column=0, columnspan=3, sticky="ew")

        tac_label(dest_card, "// Carpeta de destino").grid(
            row=1, column=0, columnspan=3, padx=14, pady=(10, 4), sticky="w")

        self.dest_label = ctk.CTkLabel(
            dest_card,
            text=self._truncate_path(self.download_dir),
            text_color="#555555",
            font=("Courier New", 10),
            anchor="w",
        )
        self.dest_label.grid(row=2, column=0, columnspan=2,
                             padx=14, pady=(0, 12), sticky="ew")

        tac_button_ghost(
            dest_card, "CAMBIAR",
            command=self._choose_dir,
            width=78, height=34,
        ).grid(row=2, column=2, padx=(0, 12), pady=(0, 12))

        # ── Video Info Card (hidden initially) ────────────────────────────────
        self.info_card = TacticalCard(sf)
        self.info_card.grid_columnconfigure(0, weight=1)
        # Not placed until info loads

        CardHeader(self.info_card, label="VIDEO.INFO").grid(
            row=0, column=0, sticky="ew")

        # Thumbnail
        self.thumbnail_lbl = ctk.CTkLabel(self.info_card, text="",
                                          corner_radius=0)
        self.thumbnail_lbl.grid(row=1, column=0, padx=14, pady=(14, 8))

        # Red accent separator under thumbnail
        TacSeparator(self.info_card).grid(
            row=2, column=0, sticky="ew", padx=0)

        # Title
        self.title_lbl = ctk.CTkLabel(
            self.info_card, text="",
            wraplength=480,
            font=("Segoe UI", 13, "bold"),
            text_color=OFF_WHITE,
            justify="center",
            corner_radius=0,
        )
        self.title_lbl.grid(row=3, column=0, padx=14, pady=(10, 4))

        # Channel / duration
        meta_row = ctk.CTkFrame(self.info_card, fg_color="transparent",
                                corner_radius=0)
        meta_row.grid(row=4, column=0, padx=14, pady=(0, 12))

        self.channel_lbl = ctk.CTkLabel(
            meta_row, text="",
            text_color="#555555",
            font=("Courier New", 10),
        )
        self.channel_lbl.grid(row=0, column=0, padx=(0, 16))

        self.duration_lbl = ctk.CTkLabel(
            meta_row, text="",
            text_color="#555555",
            font=("Courier New", 10),
        )
        self.duration_lbl.grid(row=0, column=1)

        TacSeparator(self.info_card).grid(
            row=5, column=0, sticky="ew", padx=14, pady=4)

        # ── Quality selectors grid ─────────────────────────────────────────
        selectors_row = ctk.CTkFrame(self.info_card, fg_color="transparent",
                                     corner_radius=0)
        selectors_row.grid(row=6, column=0, padx=14, pady=(6, 0), sticky="ew")
        selectors_row.grid_columnconfigure((0, 1), weight=1)

        # Video quality column
        video_q_col = ctk.CTkFrame(selectors_row, fg_color="transparent",
                                   corner_radius=0)
        video_q_col.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        video_q_col.grid_columnconfigure(0, weight=1)

        tac_label(video_q_col, "// Calidad de video").grid(
            row=0, column=0, pady=(0, 4), sticky="w")

        self.quality_var  = ctk.StringVar(value="Mejor disponible")
        self.quality_menu = ctk.CTkOptionMenu(
            video_q_col,
            variable=self.quality_var,
            values=["Mejor disponible"],
            height=38,
            fg_color=GRAY_DARK,
            button_color=RED,
            button_hover_color=RED_MED,
            text_color=OFF_WHITE,
            font=("Courier New", 11),
            corner_radius=0,
            dynamic_resizing=False,
        )
        self.quality_menu.grid(row=1, column=0, sticky="ew")

        # Audio quality column
        audio_q_col = ctk.CTkFrame(selectors_row, fg_color="transparent",
                                   corner_radius=0)
        audio_q_col.grid(row=0, column=1, padx=(6, 0), sticky="ew")
        audio_q_col.grid_columnconfigure(0, weight=1)

        tac_label(audio_q_col, "// Calidad de audio").grid(
            row=0, column=0, pady=(0, 4), sticky="w")

        self.audio_quality_var  = ctk.StringVar(value="192k  —  ESTÁNDAR")
        self.audio_quality_menu = ctk.CTkOptionMenu(
            audio_q_col,
            variable=self.audio_quality_var,
            values=[
                "64k   —  BAJO",
                "128k  —  BUENO",
                "192k  —  ESTÁNDAR",
                "256k  —  ALTO",
                "320k  —  MÁXIMO",
            ],
            height=38,
            fg_color=GRAY_DARK,
            button_color=STEEL,
            button_hover_color=RED,
            text_color=OFF_WHITE,
            font=("Courier New", 11),
            corner_radius=0,
            dynamic_resizing=False,
        )
        self.audio_quality_menu.grid(row=1, column=0, sticky="ew")

        # Download buttons
        btn_row = ctk.CTkFrame(self.info_card, fg_color="transparent",
                               corner_radius=0)
        btn_row.grid(row=8, column=0, padx=14, pady=(12, 18))
        btn_row.grid_columnconfigure((0, 1), weight=1)

        self.dl_video_btn = tac_button_primary(
            btn_row, "⬇  DESCARGAR VIDEO",
            command=lambda: self._start_download(audio_only=False),
            height=46,
        )
        self.dl_video_btn.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.dl_audio_btn = ctk.CTkButton(
            btn_row,
            text="🎵  DESCARGAR AUDIO",
            height=46,
            fg_color="transparent",
            hover_color=STEEL,
            border_color=RED,
            border_width=1,
            text_color=RED,
            font=("Courier New", 11, "bold"),
            corner_radius=0,
            command=lambda: self._start_download(audio_only=True),
        )
        self.dl_audio_btn.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        # ── Progress Card ─────────────────────────────────────────────────────
        self.prog_card = TacticalCard(sf)
        self.prog_card.grid_columnconfigure(0, weight=1)
        # Not placed until download starts

        CardHeader(self.prog_card, label="TRANSFERENCIA").grid(
            row=0, column=0, sticky="ew")

        self.prog_title = ctk.CTkLabel(
            self.prog_card,
            text="DESCARGANDO...",
            font=("Courier New", 11, "bold"),
            text_color=OFF_WHITE,
        )
        self.prog_title.grid(row=1, column=0, padx=14, pady=(14, 8), sticky="w")

        self.prog_bar = ctk.CTkProgressBar(
            self.prog_card,
            height=8,
            progress_color=RED,
            fg_color=GRAY_DARK,
            corner_radius=0,
        )
        self.prog_bar.set(0)
        self.prog_bar.grid(row=2, column=0, padx=14, pady=(0, 8), sticky="ew")

        detail_row = ctk.CTkFrame(self.prog_card, fg_color="transparent",
                                  corner_radius=0)
        detail_row.grid(row=3, column=0, padx=14, pady=(0, 6), sticky="ew")
        detail_row.grid_columnconfigure(1, weight=1)

        self.pct_lbl = ctk.CTkLabel(
            detail_row,
            text="0 %",
            font=("Courier New", 13, "bold"),
            text_color=RED,
        )
        self.pct_lbl.grid(row=0, column=0, padx=(0, 14))

        self.eta_lbl = ctk.CTkLabel(
            detail_row,
            text="",
            text_color="#555555",
            font=("Courier New", 10),
            anchor="w",
        )
        self.eta_lbl.grid(row=0, column=1, sticky="ew")

        self.open_folder_btn = ctk.CTkButton(
            self.prog_card,
            text="📂  ABRIR CARPETA",
            height=38,
            fg_color="transparent",
            hover_color=STEEL,
            border_color=BORDER,
            border_width=1,
            text_color="#555555",
            font=("Courier New", 10),
            corner_radius=0,
            command=self._open_downloads_folder,
        )
        # Placed only after download completes

        # ── Footer táctico ────────────────────────────────────────────────────
        TacSeparator(sf).grid(row=99, column=0, sticky="ew",
                              padx=0, pady=(12, 0))
        footer = ctk.CTkFrame(sf, fg_color=STEEL_MID, corner_radius=0)
        footer.grid(row=100, column=0, sticky="ew")
        footer.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            footer, text="// GABODEV  ·  POWERED BY YT-DLP",
            text_color="#2a0000",
            font=("Courier New", 8),
        ).grid(row=0, column=0, padx=14, pady=8, sticky="w")

        # Status pulse dot in footer
        pulse_footer = ctk.CTkFrame(footer, fg_color="transparent",
                                    corner_radius=0)
        pulse_footer.grid(row=0, column=2, padx=12, pady=4, sticky="e")
        PulseDot(pulse_footer, color=GREEN_OK, bg=STEEL_MID).pack(
            side="left", padx=(0, 4))
        ctk.CTkLabel(
            pulse_footer, text="ONLINE",
            text_color=GREEN_OK,
            font=("Courier New", 8),
        ).pack(side="left")

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _truncate_path(path: str, max_len: int = 52) -> str:
        return path if len(path) <= max_len else "..." + path[-(max_len - 3):]

    def _choose_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.download_dir)
        if chosen:
            self.download_dir = chosen
            self.dest_label.configure(text=self._truncate_path(chosen))

    def _open_downloads_folder(self):
        try:
            if sys.platform == "win32":
                os.startfile(self.download_dir)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.download_dir])
            else:
                subprocess.Popen(["xdg-open", self.download_dir])
        except Exception as exc:
            print(f"Cannot open folder: {exc}")

    def _set_action_buttons(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.dl_video_btn.configure(state=state)
        self.dl_audio_btn.configure(state=state)
        self.load_btn.configure(state=state)
        self.quality_menu.configure(state=state)
        self.audio_quality_menu.configure(state=state)

    @staticmethod
    def _format_duration(seconds) -> str:
        if not seconds:
            return ""
        seconds = int(seconds)
        h, rem = divmod(seconds, 3600)
        m, s   = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    # ── Load video info ───────────────────────────────────────────────────────
    def load_video_info(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_badge.set("error", "INGRESA UN ENLACE")
            return
        if not YOUTUBE_RE.search(url):
            messagebox.showwarning(
                "ENLACE INVÁLIDO",
                "Ingresa una URL válida de YouTube.\n\n"
                "Formatos admitidos:\n"
                "  · https://www.youtube.com/watch?v=...\n"
                "  · https://youtu.be/...\n"
                "  · https://www.youtube.com/shorts/..."
            )
            return

        self.load_btn.configure(state="disabled", text="CARGANDO...")
        self.status_badge.set("loading")
        self.info_card.grid_remove()
        threading.Thread(target=self._fetch_info,
                         args=(url,), daemon=True).start()

    def _fetch_info(self, url: str):
        try:
            ydl_opts = {
                "quiet":         True,
                "no_warnings":   True,
                "skip_download": True,
                "http_headers": {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/125.0.0.0 Safari/537.36"
                    ),
                    "Accept-Language": "en-US,en;q=0.9",
                },
                "extractor_args": {
                    "youtube": {"player_client": ["web", "android"]}
                },
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            self.video_info = info

            # Thumbnail
            ctk_img   = None
            thumb_url = info.get("thumbnail") or ""
            if thumb_url:
                try:
                    resp    = requests.get(thumb_url, timeout=10)
                    resp.raise_for_status()
                    img     = Image.open(BytesIO(resp.content))
                    img     = img.resize((390, 219), Image.Resampling.LANCZOS)
                    ctk_img = ctk.CTkImage(img, size=(390, 219))
                except Exception as te:
                    print(f"Thumbnail error: {te}")

            # Quality options — all standard resolutions the video can deliver
            # Standard ladder: 144p → 240p → 360p → 480p → 720p → 1080p → 1440p → 2160p
            STANDARD_HEIGHTS = [144, 240, 360, 480, 720, 1080, 1440, 2160]
            formats   = info.get("formats", [])
            available = {
                f.get("height") for f in formats
                if f.get("height") and f.get("vcodec") not in (None, "none")
            }
            max_h = max(available) if available else 0

            # Include every standard step up to the max available height
            filtered = [h for h in STANDARD_HEIGHTS if h <= max_h]
            # Also include any non-standard height reported by yt-dlp
            extra = sorted(available - set(STANDARD_HEIGHTS))
            all_heights = sorted(set(filtered) | set(extra))

            q_opts = [f"{h}p" for h in all_heights]
            # Always offer a "best available" option at the end
            q_opts.append("Mejor disponible")

            channel  = info.get("channel") or info.get("uploader") or ""
            duration = self._format_duration(info.get("duration"))

            self.after(0, lambda: self._show_info(
                info["title"], ctk_img, q_opts, channel, duration))

        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.after(0, lambda: self._on_fetch_error(str(exc)))

    def _show_info(self, title: str, ctk_img, q_opts: list,
                   channel: str, duration: str):
        self.title_lbl.configure(text=title)
        if ctk_img:
            self.thumbnail_lbl.configure(image=ctk_img)
        self.channel_lbl.configure(text=f"▶  {channel}" if channel else "")
        self.duration_lbl.configure(
            text=f"⏱  {duration}" if duration else "")
        self.quality_menu.configure(values=q_opts)
        # Default to highest video quality (second-to-last before "Mejor disponible")
        if len(q_opts) >= 2:
            self.quality_var.set(q_opts[-2])   # highest named resolution
        else:
            self.quality_var.set(q_opts[-1])
        self.load_btn.configure(state="normal", text="CARGAR")
        self.status_badge.set("ready")
        self.info_card.grid(row=5, column=0, padx=20,
                            pady=6, sticky="ew")

    def _on_fetch_error(self, msg: str):
        self.load_btn.configure(state="normal", text="CARGAR")
        self.status_badge.set("error")
        messagebox.showerror(
            "ERROR DE CARGA",
            "Asegúrate de que el enlace sea correcto y tengas conexión.\n\n"
            f"Detalle: {msg[:300]}"
        )

    # ── Download ──────────────────────────────────────────────────────────────
    def _start_download(self, audio_only: bool):
        if not self.video_info or self._is_downloading:
            return

        self._is_downloading = True
        self._set_action_buttons(False)

        self.prog_bar.set(0)
        self.pct_lbl.configure(text="0 %", text_color=RED)
        self.eta_lbl.configure(text="")
        self.prog_title.configure(
            text="DESCARGANDO AUDIO (MP3)..." if audio_only
            else "DESCARGANDO VIDEO (MP4)..."
        )
        if self._open_btn_shown:
            self.open_folder_btn.grid_remove()
            self._open_btn_shown = False

        self.prog_card.grid(row=6, column=0, padx=20,
                            pady=6, sticky="ew")
        self.status_badge.set("downloading")

        url     = self.url_entry.get().strip()
        quality = self.quality_var.get()
        threading.Thread(
            target=self._download_thread,
            args=(url, quality, audio_only),
            daemon=True,
        ).start()

    def _progress_hook(self, d: dict):
        status = d.get("status", "")

        if status == "downloading":
            downloaded = d.get("downloaded_bytes") or 0
            total      = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            if total > 0:
                progress = downloaded / total
            else:
                raw = re.sub(r"[^\d.]", "", d.get("_percent_str", "0"))
                try:
                    progress = float(raw) / 100
                except ValueError:
                    progress = 0.0

            progress  = max(0.0, min(1.0, progress))
            pct_text  = f"{progress * 100:.1f} %"
            speed     = d.get("_speed_str", "—")
            eta       = d.get("_eta_str",   "—")
            eta_text  = f"VEL: {speed}  ·  RESTANTE: {eta}"

            self.after(0, lambda p=progress: self.prog_bar.set(p))
            self.after(0, lambda t=pct_text:  self.pct_lbl.configure(text=t))
            self.after(0, lambda t=eta_text:  self.eta_lbl.configure(text=t))

        elif status == "finished":
            self.after(0, lambda: self.prog_bar.set(1.0))
            self.after(0, lambda: self.pct_lbl.configure(
                text="100 %", text_color=GREEN_OK))
            self.after(0, lambda: self.eta_lbl.configure(
                text="PROCESANDO ARCHIVO FINAL..."))

    def _download_thread(self, url: str, quality: str, audio_only: bool):
        # Parse selected audio bitrate (e.g. "192k  —  ESTÁNDAR" → "192")
        raw_audio_q = self.audio_quality_var.get().split("k")[0].strip()
        audio_bitrate = raw_audio_q if raw_audio_q.isdigit() else "192"

        if audio_only:
            fmt = "bestaudio/best"
        elif quality == "Mejor disponible":
            fmt = "bestvideo+bestaudio/best"
        elif quality.endswith("p") and quality[:-1].isdigit():
            h   = quality[:-1]
            fmt = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]/best[height<={h}]"
        else:
            fmt = "bestvideo+bestaudio/best"

        outtmpl = os.path.join(self.download_dir, "%(title)s.%(ext)s")

        http_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
        }

        ydl_opts = {
            "format":              fmt,
            "outtmpl":             outtmpl,
            "progress_hooks":      [self._progress_hook],
            "merge_output_format": "mp4",
            "quiet":               True,
            "no_warnings":         True,
            "http_headers":        http_headers,
            "extractor_args":      {
                "youtube": {"player_client": ["web", "android"]}
            },
            "nocheckcertificate":  False,
            "socket_timeout":      30,
        }

        if audio_only:
            ydl_opts["postprocessors"] = [{
                "key":              "FFmpegExtractAudio",
                "preferredcodec":   "mp3",
                "preferredquality": audio_bitrate,
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, self._on_download_complete)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.after(0, lambda e=exc: self._on_download_error(str(e)))

    def _on_download_complete(self):
        self._is_downloading = False
        self._set_action_buttons(True)
        self.status_badge.set("done")
        self.prog_title.configure(text="✓  DESCARGA COMPLETADA")
        self.pct_lbl.configure(text="100 %", text_color=GREEN_OK)
        self.eta_lbl.configure(
            text=f"GUARDADO EN: {self._truncate_path(self.download_dir)}")
        if not self._open_btn_shown:
            self.open_folder_btn.grid(
                row=4, column=0, padx=14, pady=(4, 16), sticky="ew")
            self._open_btn_shown = True

    def _on_download_error(self, msg: str):
        self._is_downloading = False
        self._set_action_buttons(True)
        self.status_badge.set("error")
        self.prog_title.configure(text="✗  ERROR EN LA DESCARGA")
        self.pct_lbl.configure(text_color=RED)
        messagebox.showerror(
            "ERROR DE DESCARGA",
            "No se pudo descargar el archivo.\n\n"
            f"Detalle: {msg[:400]}"
        )


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()

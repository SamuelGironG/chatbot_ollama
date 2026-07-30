"""Interfaz Tkinter moderna del cliente de chat."""

import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

from app.llm_client import OllamaClient, OllamaClientError


MODELS = ("gemma2:2b", "llama3.2:3b", "llama3.1:8b")
BACKGROUND = "#101827"
SURFACE = "#182235"
SURFACE_ALT = "#222e43"
TEXT = "#edf2f7"
MUTED = "#9aa9bf"
ACCENT = "#6c8cff"
USER_BUBBLE = "#243b70"
ASSISTANT_BUBBLE = "#1b2b3f"
ERROR = "#ff8d9a"


class ChatApplication:
    """Coordina la interfaz y las peticiones a Ollama en segundo plano."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._client = OllamaClient()
        self._conversation: list[tuple[str, str]] = []
        self._is_generating = False

        self._configure_window()
        self._create_header()
        self._create_history()
        self._create_input()

    def _configure_window(self) -> None:
        self._root.title("Ollama Chat")
        self._root.geometry("820x650")
        self._root.minsize(650, 500)
        self._root.configure(background=BACKGROUND)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(1, weight=1)

        style = ttk.Style(self._root)
        style.theme_use("clam")
        style.configure("App.TFrame", background=BACKGROUND)
        style.configure("Surface.TFrame", background=SURFACE)
        style.configure("Title.TLabel", background=SURFACE, foreground=TEXT, font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background=SURFACE, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Label.TLabel", background=SURFACE, foreground=MUTED, font=("Segoe UI", 9, "bold"))
        style.configure("Status.TLabel", background=BACKGROUND, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("TCombobox", fieldbackground=SURFACE_ALT, background=SURFACE_ALT, foreground=TEXT, padding=7)
        style.map("TCombobox", fieldbackground=[("readonly", SURFACE_ALT)], foreground=[("readonly", TEXT)])
        style.configure("Send.TButton", background=ACCENT, foreground="#ffffff", borderwidth=0, padding=(18, 9), font=("Segoe UI", 9, "bold"))
        style.map("Send.TButton", background=[("active", "#809bff"), ("disabled", "#46577a")])
        style.configure("Clear.TButton", background=SURFACE_ALT, foreground=TEXT, borderwidth=0, padding=(12, 8))
        style.map("Clear.TButton", background=[("active", "#30405b")])

    def _create_header(self) -> None:
        header = ttk.Frame(self._root, style="Surface.TFrame", padding=(20, 16))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        badge = tk.Label(header, text="◉", background=SURFACE, foreground=ACCENT, font=("Segoe UI", 20))
        badge.grid(row=0, column=0, rowspan=2, padx=(0, 10))
        ttk.Label(header, text="Ollama Chat", style="Title.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(header, text="Asistente local · privado · sin conexión a la nube", style="Subtitle.TLabel").grid(row=1, column=1, sticky="w")

        controls = ttk.Frame(header, style="Surface.TFrame")
        controls.grid(row=0, column=2, rowspan=2, sticky="e")
        ttk.Label(controls, text="MODELO", style="Label.TLabel").grid(row=0, column=0, sticky="w")
        self._model = tk.StringVar(value=MODELS[0])
        self._selector = ttk.Combobox(controls, textvariable=self._model, values=MODELS, state="readonly", width=16)
        self._selector.grid(row=1, column=0, pady=(3, 0))

    def _create_history(self) -> None:
        container = ttk.Frame(self._root, style="App.TFrame", padding=(20, 18, 20, 8))
        container.grid(row=1, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self._history = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            background=BACKGROUND,
            foreground=TEXT,
            insertbackground=TEXT,
            selectbackground=ACCENT,
            relief=tk.FLAT,
            borderwidth=0,
            padx=10,
            pady=10,
            font=("Segoe UI", 10),
        )
        self._history.grid(row=0, column=0, sticky="nsew")
        self._history.tag_configure("user_name", foreground="#b9c7ff", font=("Segoe UI", 9, "bold"))
        self._history.tag_configure("assistant_name", foreground="#8fe3c4", font=("Segoe UI", 9, "bold"))
        self._history.tag_configure("user", background=USER_BUBBLE, foreground=TEXT, lmargin1=18, lmargin2=18, rmargin=45, spacing1=3, spacing3=14)
        self._history.tag_configure("assistant", background=ASSISTANT_BUBBLE, foreground=TEXT, lmargin1=18, lmargin2=18, rmargin=45, spacing1=3, spacing3=5)
        self._history.tag_configure("meta", foreground=MUTED, font=("Segoe UI", 8, "italic"), lmargin1=18, spacing3=16)
        self._history.tag_configure("error", foreground=ERROR, lmargin1=18, spacing3=14)
        self._write("¡Hola! Soy tu asistente local. ¿En qué puedo ayudarte?\n\n", "meta")

    def _create_input(self) -> None:
        area = ttk.Frame(self._root, style="Surface.TFrame", padding=(20, 12, 20, 16))
        area.grid(row=2, column=0, sticky="ew")
        area.columnconfigure(0, weight=1)
        self._message = tk.StringVar()
        self._entry = tk.Entry(
            area, textvariable=self._message, background=SURFACE_ALT, foreground=TEXT,
            insertbackground=TEXT, relief=tk.FLAT, font=("Segoe UI", 10),
            highlightthickness=1, highlightbackground="#33445f", highlightcolor=ACCENT,
        )
        self._entry.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0, 10))
        self._entry.bind("<Return>", self._on_enter)
        self._send = ttk.Button(area, text="Enviar  ➜", style="Send.TButton", command=self._send_message)
        self._send.grid(row=0, column=1, sticky="e")
        self._status = ttk.Label(area, text="Listo para conversar", style="Status.TLabel")
        self._status.grid(row=1, column=0, sticky="w", pady=(9, 0))
        self._clear = ttk.Button(area, text="Limpiar", style="Clear.TButton", command=self._clear_history)
        self._clear.grid(row=1, column=1, sticky="e", pady=(6, 0))
        self._entry.focus_set()

    def _on_enter(self, _event: tk.Event) -> str:
        self._send_message()
        return "break"

    def _send_message(self) -> None:
        message = self._message.get().strip()
        if not message or self._is_generating:
            return
        self._message.set("")
        self._write("TÚ\n", "user_name")
        self._write(f"{message}\n\n", "user")
        self._conversation.append(("Usuario", message))
        self._set_busy(True)
        threading.Thread(target=self._generate, args=(self._model.get(), self._build_prompt()), daemon=True).start()

    def _build_prompt(self) -> str:
        turns = (f"{role}: {message}" for role, message in self._conversation)
        return "Eres un asistente útil. Responde en español.\n\n" + "\n\n".join(turns) + "\n\nAsistente:"

    def _generate(self, model: str, prompt: str) -> None:
        try:
            result = self._client.generate(model, prompt)
        except OllamaClientError as error:
            self._root.after(0, self._show_error, str(error))
        else:
            self._root.after(0, self._show_response, result.text, result.elapsed_seconds)

    def _show_response(self, text: str, elapsed_seconds: float) -> None:
        answer = text or "(sin contenido)"
        self._write("OLLAMA\n", "assistant_name")
        self._write(f"{answer}\n", "assistant")
        self._write(f"Tiempo de respuesta · {elapsed_seconds:.2f} s\n\n", "meta")
        self._conversation.append(("Asistente", answer))
        self._set_busy(False)

    def _show_error(self, message: str) -> None:
        self._write(f"No se pudo obtener una respuesta: {message}\n\n", "error")
        self._set_busy(False)

    def _write(self, text: str, tag: str | None = None) -> None:
        self._history.configure(state=tk.NORMAL)
        self._history.insert(tk.END, text, tag)
        self._history.configure(state=tk.DISABLED)
        self._history.see(tk.END)

    def _clear_history(self) -> None:
        if self._is_generating:
            return
        self._history.configure(state=tk.NORMAL)
        self._history.delete("1.0", tk.END)
        self._history.configure(state=tk.DISABLED)
        self._conversation.clear()
        self._status.configure(text="Historial limpiado")

    def _set_busy(self, busy: bool) -> None:
        self._is_generating = busy
        self._send.configure(state=tk.DISABLED if busy else tk.NORMAL)
        self._entry.configure(state=tk.DISABLED if busy else tk.NORMAL)
        self._selector.configure(state=tk.DISABLED if busy else "readonly")
        self._clear.configure(state=tk.DISABLED if busy else tk.NORMAL)
        self._status.configure(text="Generando respuesta…" if busy else "Listo para conversar")

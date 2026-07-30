"""Punto de entrada del cliente de chat para Ollama."""

import tkinter as tk

from app.ui import ChatApplication


def main() -> None:
    root = tk.Tk()
    ChatApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

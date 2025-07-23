import tkinter as tk
from src.ui.main_window import JournalApp

def main() -> None:
    root = tk.Tk()
    root.title("Journal Tool")
    JournalApp(root)
    root.minsize(900, 600)
    root.mainloop()

if __name__ == "__main__":
    main()
import ttkbootstrap as ttk

from gui.app import ImageApp


def main() -> None:
    app = ttk.Window(themename="flatly")
    ImageApp(app)
    app.mainloop()


if __name__ == "__main__":
    main()

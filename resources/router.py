import tkinter as tk

class Router(tk.Frame):
    def __init__(self, master, pages: dict, start_page: str):
        super().__init__(master)
        self.master = master
        self.pages = pages   # dict: {"login": LoginPage, "home": HomePage, ...}
        self.frames = {}     # cache instance halaman
        self.current_page = None

        # langsung tampilkan halaman awal
        self.navigate(start_page)

    def navigate(self, page_name: str):
        # sembunyikan halaman aktif
        if self.current_page:
            self.frames[self.current_page].pack_forget()

        # buat instance baru jika belum ada
        if page_name not in self.frames:
            page_class = self.pages[page_name]
            frame = page_class(self, controller=self)
            self.frames[page_name] = frame

        # tampilkan halaman baru
        self.frames[page_name].pack(fill="both", expand=True)
        self.current_page = page_name

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from core.api import Compiler

class CompilerWindow:
    def __init__(self, root):
        self.root, self.result = root, None
        root.title("Lexical analysis")
        root.geometry("1160x740")
        root.minsize(980, 600)
        root.configure(bg="#242424")
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure(".", background="#242424", foreground="#ffffff", font=("Segoe UI", 10))
        for widget in ("TButton", "Treeview.Heading", "Vertical.TScrollbar"):
            style.configure(widget, background="#383838", arrowcolor="#ffffff", padding=6)
            style.map(widget, background=[("active", "#454545")])
        style.configure("Accent.TButton", background="#3584e4", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#62a0ea")])
        style.configure("Treeview", background="#303030", fieldbackground="#303030", rowheight=28)
        style.map("Treeview", background=[("selected", "#3584e4")], foreground=[("selected", "#ffffff")])
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)
        bar = ttk.Frame(frame)
        bar.pack(fill="x", pady=(0, 14))
        ttk.Button(bar, text="Open source", command=self.open_source).pack(side="left")
        ttk.Button(bar, text="Analyze", style="Accent.TButton", command=self.analyze).pack(side="right")
        panes = ttk.Panedwindow(frame, orient="horizontal")
        panes.pack(fill="both", expand=True)
        source_panel = ttk.Labelframe(panes, text="Source", padding=8)
        self.editor = ScrolledText(source_panel, width=38, wrap="char", undo=True, font=("Consolas", 12),
                                   bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", selectbackground="#3584e4")
        self.editor.vbar.configure(bg="#383838", troughcolor="#242424", activebackground="#454545")
        self.editor.tag_configure("error", background="#652832", foreground="#ffffff")
        self.editor.bind("<<Modified>>", self.source_modified)
        self.editor.pack(fill="both", expand=True)
        panes.add(source_panel, weight=2)
        results = ttk.Panedwindow(panes, orient="vertical")
        self.tokens = self.make_table(results, "Tokens", ("Type", "Lexeme", "Line", "Column", "Offset"))
        self.diagnostics = self.make_table(results, "Diagnostics", ("Code", "Message", "Line", "Column", "Length"))
        self.diagnostics.bind("<<TreeviewSelect>>", self.select_diagnostic)
        panes.add(results, weight=3)
        self.status = tk.StringVar(value="Open a file or enter source, then click Analyze.")
        ttk.Label(frame, textvariable=self.status, wraplength=1050).pack(anchor="w", pady=(14, 0))
        self.editor.insert("1.0", "int total = (12 + 30)\nfunc sum(total)\n")
        self.editor.edit_modified(False)

    def make_table(self, parent, label, columns):
        panel = ttk.Labelframe(parent, text=label, padding=8)
        table = ttk.Treeview(panel, columns=columns, show="headings", selectmode="browse")
        for column, width in zip(columns, (110, 200, 50, 55, 55)):
            table.heading(column, text=column)
            table.column(column, width=width, minwidth=40)
        scrollbar = ttk.Scrollbar(panel, command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        table.pack(fill="both", expand=True)
        parent.add(panel, weight=2 if label == "Tokens" else 1)
        return table

    def clear_result(self):
        self.result = None
        for table in (self.tokens, self.diagnostics):
            table.delete(*table.get_children())
        self.editor.tag_remove("error", "1.0", "end")
        self.status.set("Click Analyze to refresh the result.")

    def source_modified(self, _event=None):
        if self.editor.edit_modified():
            self.clear_result()
            self.editor.edit_modified(False)

    def set_source(self, path):
        try:
            source = Path(path).read_text(encoding="utf-8-sig")
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", source)
            self.clear_result()
            self.editor.edit_modified(False)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Cannot open source", str(exc))

    def open_source(self):
        if path := filedialog.askopenfilename(filetypes=[("NovaScript", "*.ns"), ("All files", "*")]):
            self.set_source(path)

    def analyze(self):
        self.clear_result()
        self.editor.edit_modified(False)
        try:
            compiler = Compiler()
            self.result = compiler.analyze_lexically(self.editor.get("1.0", "end-1c"))
        except (OSError, ValueError) as exc:
            messagebox.showerror("DFA configuration error", str(exc))
            return
        for t in self.result.tokens:
            self.tokens.insert("", "end", values=(t.type.value, t.lexeme, t.pos.line, t.pos.column, t.pos.offset))
        for i, d in enumerate(self.result.diagnostics):
            self.diagnostics.insert("", "end", iid=str(i), values=(d.code, d.msg, d.line, d.column, d.length))
            self.editor.tag_add("error", f"1.0 + {d.offset} chars", f"1.0 + {d.offset + d.length} chars")
        self.status.set(f"{len(self.result.tokens)} tokens  /  {len(self.result.diagnostics)} errors. Select an error to locate it.")

    def select_diagnostic(self, _event=None):
        if self.result is not None and (selected := self.diagnostics.selection()):
            diagnostic = self.result.diagnostics[int(selected[0])]
            self.editor.see(f"1.0 + {diagnostic.offset} chars")
            self.status.set(diagnostic.msg)

def main():
    root = tk.Tk()
    CompilerWindow(root)
    root.mainloop()
    return 0

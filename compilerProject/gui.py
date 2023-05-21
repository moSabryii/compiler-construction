import tkinter as tk
from tokenizer import Tokenizer
from myparser import Parser


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.code_label = tk.Label(self, text="Enter code:")
        self.code_label.pack()
        self.code_entry = tk.Entry(self, width=50)
        self.code_entry.pack()
        self.token_button = tk.Button(self, text="Tokenize", command=self.tokenize)
        self.token_button.pack()
        self.tree_button = tk.Button(self, text="Generate Tree", command=self.generate_tree)
        self.tree_button.pack()
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def tokenize(self):
        code = self.code_entry.get()
        tokenizer = Tokenizer(code)
        tokens = []
        while True:
            token = tokenizer.get_next_token()
            if token.type == "EOF":
                break
            tokens.append(token)
        result = "\n".join(str(token) for token in tokens)
        self.result_label.config(text=result)

    def generate_tree(self):
        code = self.code_entry.get()
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        ast = parser.parse()
        self.result_label.config(text=repr(ast))


root = tk.Tk()
app = Application(master=root)
app.mainloop()

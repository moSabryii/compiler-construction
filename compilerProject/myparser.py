class ASTNode:
    def __init__(self, type_, children):
        self.type = type_
        self.children = children

    def __repr__(self):
        return f"{self.type}({', '.join(repr(child) for child in self.children)})"

# Parser class that takes a Tokenizer object as input and generates an abstract syntax tree (AST) from the tokens.
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, type_):
        if self.current_token.type == type_:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return ASTNode("Number", [token.value])
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return ASTNode("Variable", [token.value])
        elif token.type == "STRING":
            self.eat("STRING")
            return ASTNode("String", [token.value])
        elif token.type == "OPERATOR" and token.value == "(":
            self.eat("OPERATOR")
            node = self.expr()
            self.eat("OPERATOR")
            return node
        else:
            self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type == "OPERATOR" and self.current_token.value in ["*", "/", "%"]:
            op = self.current_token
            self.eat("OPERATOR")
            node = ASTNode("BinaryOperation", [node, op.value, self.factor()])

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type == "OPERATOR" and self.current_token.value in ["+", "-"]:
            op = self.current_token
            self.eat("OPERATOR")
            node = ASTNode("BinaryOperation", [node, op.value, self.term()])

        return node

    def assignment_statement(self):
        var = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("OPERATOR")  # skip equals sign
        expr = self.expr()
        return ASTNode("Assignment", [var, expr])

    def statement(self):
        if self.current_token.type == "IDENTIFIER":
            return self.assignment_statement()
        else:
            self.error()

    def program(self):
        statements = []
        while self.current_token.type != "EOF":
            statements.append(self.statement())
        return ASTNode("Program", statements)

    def parse(self):
        ast = self.program()
        if self.current_token.type != "EOF":
            self.error()
        return ast

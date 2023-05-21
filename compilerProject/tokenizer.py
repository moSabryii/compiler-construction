class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


#takes a string of code and return it as tokens
class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
#returns the next tokens untill reaches the end of the string
    def get_next_token(self):
        #The get_next_token() method uses a series of if-else statements
        #to determine the type of the current character and returns the corresponding token.
        if self.pos >= len(self.text):
            return Token("EOF", None)

        char = self.text[self.pos]

        if char.isdigit():
            return self.number()
        elif char.isalpha():
            return self.identifier()
        elif char == '"':
            return self.string()
        elif char in "+-*/%()":
            self.pos += 1
            return Token("OPERATOR", char)
        elif char.isspace():
            self.pos += 1
            return self.get_next_token()
        else:
            raise Exception(f"Invalid character: {char}")

    def number(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
        return Token("NUMBER", int(self.text[start:self.pos]))

    def identifier(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isalnum():
            self.pos += 1
        return Token("IDENTIFIER", self.text[start:self.pos])

    def string(self):
        start = self.pos + 1
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            self.pos += 1
        value = self.text[start:self.pos]
        self.pos += 1
        return Token("STRING", value)

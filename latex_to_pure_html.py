from typing import List, Union
from enum import Enum, auto

class TOKEN(Enum):
    LEFT_CURLY_BRACE = auto()
    RIGHT_CURLY_BRACE = auto()
    INTEGRAL = auto()
    LE = auto()
    BE = auto()
    NE = auto()
    FRAC = auto()
    CDOT = auto()
    VARX = auto()
    SUB = auto()
    SUP = auto()
    VEC = auto()
    EQUIV = auto()
    PLUSMINUS = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_STRAIGHT_BRACE = auto()
    RIGHT_STRAIGHT_BRACE = auto()

class LatexToken:
    def __init__(self, t : TOKEN) -> None:
        self.token : TOKEN = t
        return

    def __eq__(self, o) -> bool:
        return ((type(o) == LatexToken) and (self.token is o.token))

    def latex_form(self) -> str:
        if (self.token is TOKEN.LEFT_CURLY_BRACE):
            return r"\{"
        if (self.token is TOKEN.RIGHT_CURLY_BRACE):
            return r"\}"
        if (self.token is TOKEN.INTEGRAL):
            return r"\int"
        if (self.token is TOKEN.LE):
            return r"\le"
        if (self.token is TOKEN.BE):
            return r"\ge"
        if (self.token is TOKEN.NE):
            return r"\ne"
        if (self.token is TOKEN.FRAC):
            return r"\frac"
        if (self.token is TOKEN.CDOT):
            return r"\cdot"
        if (self.token is TOKEN.VARX):
            return r"\x"
        if (self.token is TOKEN.SUB):
            return r"_"
        if (self.token is TOKEN.SUP):
            return r"^"
        if (self.token is TOKEN.VEC):
            return r"\vec"
        if (self.token is TOKEN.EQUIV):
            return r"\equiv"
        if (self.token is TOKEN.PLUSMINUS):
            return r"\pm"
        if (self.token is TOKEN.LEFT_BRACE):
            return r"\left("
        if (self.token is TOKEN.RIGHT_BRACE):
            return r"\right)"
        if (self.token is TOKEN.LEFT_STRAIGHT_BRACE):
            return r"\left|"
        if (self.token is TOKEN.RIGHT_STRAIGHT_BRACE):
            return r"\right|"
        raise Exception()

    def html_form(self) -> str:
        if (self.token is TOKEN.LEFT_CURLY_BRACE):
            return r"{"
        if (self.token is TOKEN.RIGHT_CURLY_BRACE):
            return r"}"
        if (self.token is TOKEN.INTEGRAL):
            return r"&int;"
        if (self.token is TOKEN.LE):
            return r"&le;"
        if (self.token is TOKEN.BE):
            return r"&ge;"
        if (self.token is TOKEN.NE):
            return r"&ne;"
        if (self.token is TOKEN.FRAC):
            return r"&frasl;"
        if (self.token is TOKEN.CDOT):
            return r"&middot;"
        if (self.token is TOKEN.VARX):
            return r"x"
        if (self.token is TOKEN.SUB):
            return r"_"
        if (self.token is TOKEN.SUP):
            return r"^"
        if (self.token is TOKEN.EQUIV):
            return r"&equiv;"
        if (self.token is TOKEN.PLUSMINUS):
            return r"&#177;"
        if (self.token is TOKEN.LEFT_BRACE):
            return r"("
        if (self.token is TOKEN.RIGHT_BRACE):
            return r")"
        if (self.token is TOKEN.LEFT_STRAIGHT_BRACE):
            return r"|"
        if (self.token is TOKEN.RIGHT_STRAIGHT_BRACE):
            return r"|"
        raise Exception()

    def to_html(self) -> str:
        return self.html_form()

    def __repr__(self) -> str:
        return f"T[{self.token}]"

    def __str__(self) -> str:
        return f"T[{self.token}]"

class LatexBlock:
    def __init__(self, st : str = "", cont : List[Union[str, LatexToken, "LatexBlock"]] = []):
        self.content : List[Union[str, LatexToken, LatexBlock]] = cont
        if (len(self.content) == 0):
            self.parse(st)
        return

    def __repr__(self) -> str:
        return f"B{self.content}"

    def __str__(self) -> str:
        return f"B{self.content}"

    def to_html(self) -> str:
        res = ""
        for elt in self.content:
            if (type(elt) == str):
                res += elt
            else:
                res += elt.to_html()
        return res

    def parse(self, s : str) -> None:
        self.content = self.parse_tokens(s)
        self.atomize_strings()
        block_found = True
        while (block_found):
            block_found = False
            brace_right = 0
            while ((brace_right < len(self.content)) and (self.content[brace_right] != "}")):
                brace_right = brace_right + 1
            if (brace_right >= len(self.content)):
                continue
            brace_left = brace_right
            while ((brace_left >= 0) and (self.content[brace_left] != "{")):
                brace_left = brace_left - 1
            if (brace_left < 0):
                continue
            block_found = True
            new_content : List[Union[str, LatexToken, LatexBlock]] = []
            new_content.extend(self.content[0:brace_left])
            new_content.append(LatexBlock(cont = self.content[brace_left+1:brace_right]))
            new_content.extend(self.content[brace_right+1:len(self.content)])
            self.content = new_content
        for elt in self.content:
            if (type(elt) == LatexBlock):
                elt.parse_expressions()
        self.parse_expressions()
        return

    def atomize_strings(self) -> None:
        res : List[Union[str, LatexToken, LatexBlock]] = []
        for elt in self.content:
            if (type(elt) == str):
                for c in elt:
                    res.append(c)
            else:
                res.append(elt)
        self.content = res
        return

    def parse_token(self, t : LatexToken, c : List[Union[str, LatexToken]]) -> List[Union[str, LatexToken]]:
        res : List[Union[str, LatexToken]] = []
        for s in c:
            if (type(s) == str):
                cur_pos = 0
                t_b = s.find(t.latex_form(), cur_pos)
                while (t_b != -1):
                    res.append(s[cur_pos:t_b])
                    res.append(t)
                    cur_pos = t_b + len(t.latex_form())
                    t_b = s.find(t.latex_form(), cur_pos)
                res.append(s[cur_pos:len(s)])
            else:
                res.append(s)
        return res

    def parse_tokens(self, s : str) -> List[Union[str, LatexToken]]:
        res : List[Union[str, LatexToken]] = [s]
        for token in TOKEN:
            res = self.parse_token(LatexToken(token), res)
        return res

    def parse_expressions(self) -> None:
        self.parse_expression_prefix(TOKEN.FRAC, 2)
        self.parse_expression_infix(TOKEN.SUB)
        self.parse_expression_infix(TOKEN.SUP)
        self.parse_expression_prefix(TOKEN.VEC, 1)
        return

    def parse_expression_prefix(self, token : TOKEN, parameters_count : int):
        expression_found = True
        while (expression_found):
            cur_pos = 0
            expression_found = False
            while ((cur_pos < len(self.content)) and (not (self.content[cur_pos] == LatexToken(token)))):
                cur_pos = cur_pos + 1
            if (cur_pos >= len(self.content)):
                continue
            expression_found = True
            res : List[Union[str, LatexToken, LatexBlock]] = []
            res.extend(self.content[0:cur_pos])
            p = []
            for i in range(parameters_count):
                p.append(self.content[cur_pos+1+i])
            res.append(LatexExpression(LatexToken(token), p))
            res.extend(self.content[cur_pos+1+parameters_count:len(self.content)])
            self.content = res
        return

    def parse_expression_infix(self, token : TOKEN):
        expression_found = True
        while (expression_found):
            cur_pos = 0
            expression_found = False
            while ((cur_pos < len(self.content)) and (not (self.content[cur_pos] == LatexToken(token)))):
                cur_pos = cur_pos + 1
            if (cur_pos >= len(self.content)):
                continue
            expression_found = True
            res : List[Union[str, LatexToken, LatexBlock]] = []
            res.extend(self.content[0:cur_pos-1])
            res.append(LatexExpression(LatexToken(token), [self.content[cur_pos-1], self.content[cur_pos+1]]))
            res.extend(self.content[cur_pos+2:len(self.content)])
            self.content = res
        return

class LatexExpression:
    def __init__(self, t : LatexToken, p : List[LatexBlock]):
        self.token = t
        self.parameters = p
        return

    def __repr__(self) -> str:
        return f"E[{self.token}{self.parameters}]"

    def __str__(self) -> str:
        return f"E[{self.token}{self.parameters}]"

    def to_html(self) -> str:
        if (self.token.token is TOKEN.FRAC):
            left_part = self.parameters[0] if type(self.parameters[0]) == str else self.parameters[0].to_html()
            right_part = self.parameters[1] if type(self.parameters[1]) == str else self.parameters[1].to_html()
            res = f'<table style="display:inline-table;" border="1" frame="void" rules="all">\n<tr>\n<td>{left_part}</td>\n</tr>\n<tr>\n<td>{right_part}</td>\n</tr>\n</table>'
            return res
        if (self.token.token is TOKEN.SUB):
            left_part = self.parameters[0] if type(self.parameters[0]) == str else self.parameters[0].to_html()
            right_part = self.parameters[1] if type(self.parameters[1]) == str else self.parameters[1].to_html()
            return f"{left_part}<sub>{right_part}</sub>"
        if (self.token.token is TOKEN.SUP):
            left_part = self.parameters[0] if type(self.parameters[0]) == str else self.parameters[0].to_html()
            right_part = self.parameters[1] if type(self.parameters[1]) == str else self.parameters[1].to_html()
            return f"{left_part}<sup>{right_part}</sup>"
        if (self.token.token is TOKEN.VEC):
            right_part = self.parameters[0] if type(self.parameters[0]) == str else self.parameters[0].to_html()
            return f'<b style="text-decoration-line:overline">{right_part}</b>'
        raise Exception()

class LatexFormula:
    def __init__(self, s : str) -> None:
        self.content : List[Union[str, LatexBlock]] = []
        self.parse(s)
        return

    def __str__(self) -> str:
        return f"F{self.content}"

    def to_html(self) -> str:
        res = ""
        for elt in self.content:
            if (type(elt) == str):
                res += elt
            else:
                res += elt.to_html()
        return f"<i>{res}</i>"

    def parse(self, s : str) -> None:
        block = LatexBlock(st = s)
        self.content = block.content
        return

class LatexText:
    def __init__(self, s : str) -> None:
        self.content : List[Union[str, LatexFormula]] = []
        self.parse(s)
        return

    def parse(self, s : str) -> None:
        res : List[Union[str, LatexFormula]] = []
        cur_position = 0
        while (cur_position != -1) and (cur_position < len(s)):
            dl_start = s.find("$", cur_position)
            if (dl_start != -1):
                dl_end = s.find("$", dl_start+1)
                if (dl_end != -1):
                    res.append(s[cur_position:dl_start])
                    formula = LatexFormula(s[dl_start+1:dl_end])
                    res.append(formula)
                    cur_position = dl_end + 1
                else:
                    res.append(s[cur_position:])
                    cur_position = len(s)
            else:
                res.append(s[cur_position:])
                cur_position = dl_start
        self.content = res
        return

    def to_html(self) -> str:
        res = ""
        for elt in self.content:
            if (type(elt) == str):
                res += elt
            else:
                res += elt.to_html()
        res = f'<p style="display:inline-table;">\n{res}\n</p>'
        return res

import argparse

def main() -> None:
    parser = argparse.ArgumentParser(description='Convert LaTeX string to pure HTML code.')
    parser.add_argument('--latex-string', dest='latex_string', metavar='LATEX_STRING', type=str, default="", help='LaTeX string for convert')
    parser.add_argument('--latex-file', dest='latex_file', metavar='LATEX_FILE', type=str, default="", help='file with LaTeX string for convert')
    parser.add_argument('--html-file', dest='html_file', metavar='HTML_FILE', type=str, default="", help='file with LaTeX string for convert')

    args = parser.parse_args()
    latex_str : str = ""
    if (args.latex_file != ""):
        with open(args.latex_file, 'r') as fp:
            latex_str = fp.read()
    else:
        latex_str = args.latex_string
    
    text = LatexText(latex_str)
    html_str = text.to_html()
    if (args.html_file != ""):
        with open(args.html_file, 'w') as fp:
            fp.write(html_str)
    else:
        print(html_str)
    return

if __name__ == "__main__":
    main()
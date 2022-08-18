from typing import List, Union, Any, Optional
from enum import Enum, auto

T_AST = List[Union[str, "LatexToken", "LatexBlock"]]

class LatexTokenMetaclass(type): 

    def __new__(cls, name, bases, dct):
        new_latex_token_class = super(LatexTokenMetaclass, cls).__new__(cls, name, bases, dct)
        if (name != "LatexToken"):
            new_latex_token_class._latex_token_classes.append(new_latex_token_class)
        return new_latex_token_class

class LatexToken(metaclass = LatexTokenMetaclass):
    _latex_token_classes : List[Any] = []
    _latex_signature_prefix : int = 0
    _latex_signature_postfix : int = 0
    __prefix_parameters : List[Any] = []
    __postfix_parameters : List[Any] = []
    __latex_form : List[str] = []
    __html_form : str = ""
    latex_to_html : Optional[List[Any]] = None

    def __init__(self) -> None:
        if (not (self.latex_to_html is None)):
            if (type(self.latex_to_html[0]) == list):
                self.__latex_form = self.latex_to_html[0]
            else:
                self.__latex_form = [self.latex_to_html[0]]
            self.__html_form = self.latex_to_html[1]
            if (len(self.latex_to_html) > 2):
                self._latex_signature_prefix = self.latex_to_html[2]
            if (len(self.latex_to_html) > 3):
                self._latex_signature_postfix = self.latex_to_html[3]
        return

    def pref_p(self, i : int) -> str:
        return self._parameter_to_html(self.__prefix_parameters[i])

    def post_p(self, i : int) -> str:
        return self._parameter_to_html(self.__postfix_parameters[i])

    @staticmethod
    def _parameter_to_html(parameter) -> str:
        res : str = parameter if (type(parameter) == str) else parameter.to_html()
        return res

    def set_parameters(self, pre_par, post_par) -> None:
        self.__prefix_parameters  = pre_par
        self.__postfix_parameters = post_par
        return

    @staticmethod
    def parse_tokens(res : T_AST) -> T_AST:
        for token_class in LatexToken._latex_token_classes:
            token = token_class()
            res = token.parse(res)
        return res

    def parse(self, c : T_AST) -> T_AST:
        for t_latex in self.__latex_form:
            res : T_AST = []
            for s in c:
                if (type(s) == str):
                    cur_pos = 0
                    t_b = self.find_token_latex(s, t_latex, cur_pos)
                    while (t_b != -1):
                        res.append(s[cur_pos:t_b])
                        res.append(self)
                        cur_pos = t_b + len(t_latex)
                        t_b = self.find_token_latex(s, t_latex, cur_pos)
                    res.append(s[cur_pos:len(s)])
                else:
                    res.append(s)
            c = res
        return res

    def find_token_latex(self, s : str, t_latex : str, cur_pos : int) -> int:
        pos = s.find(t_latex, cur_pos)
        last_pos = pos + len(t_latex)
        if ((pos == -1) or (last_pos >= len(s))):
            return pos
        if ((t_latex[-1].isalnum()) and (s[last_pos].isalnum())):
            return -1
        return pos
    
    def to_html(self) -> str:
        return self.__html_form

class LatexTokenSTRAIGHT_BRACE(LatexToken):
    latex_to_html = [r"\|", r"|"]
    
class LatexTokenLEFT_BRACE(LatexToken):
    latex_to_html = [r"\(", r"("]

class LatexTokenRIGHT_BRACE(LatexToken):
    latex_to_html = [r"\)", r")"]

class LatexTokenLEFT_CURLY_BRACE(LatexToken):
    latex_to_html = [r"\{", r"{"]

class LatexTokenRIGHT_CURLY_BRACE(LatexToken):
    latex_to_html = [r"\}", r"}"]

class LatexTokenPLUSMINUS(LatexToken):
    latex_to_html = [r"\pm", r"&#177;"]

class LatexTokenEQUIV(LatexToken):
    latex_to_html = [r"\equiv", r"&equiv;"]

class LatexTokenCDOT(LatexToken):
    latex_to_html = [r"\cdot", r"&middot;"]

class LatexTokenNE(LatexToken):
    latex_to_html = [r"\ne", r"&ne;"]

class LatexTokenLE(LatexToken):
    latex_to_html = [[r"\le", r"\leq"], r"&le;"]

class LatexTokenGE(LatexToken):
    latex_to_html = [[r"\ge", r"\geq"], r"&ge;"]
    
class LatexTokenINTEGRAL(LatexToken):
    latex_to_html = [r"\int", r"&int;"]
    
class LatexTokenFRAC(LatexToken):
    latex_to_html = [r"\frac", r"&frasl;", 0, 2]
    
    def to_html(self) -> str:
        res = f'<table style="display:inline-table;" border="1" frame="void" rules="all">\n<tr>\n<td>{self.post_p(0)}</td>\n</tr>\n<tr>\n<td>{self.post_p(1)}</td>\n</tr>\n</table>'
        return res
    
class LatexTokenVEC(LatexToken):
    latex_to_html = [r"\vec", None, 0, 1]
    
    def to_html(self) -> str:
        res = f'<b style="text-decoration-line:overline">{self.post_p(0)}</b>'
        return res
    
class LatexTokenSUB(LatexToken):
    latex_to_html = [r"_", None, 1, 1]
    
    def to_html(self) -> str:
        res = f"{self.pref_p(0)}<sub>{self.post_p(0)}</sub>"
        return res
    
class LatexTokenSUP(LatexToken):
    latex_to_html = [r"^", None, 1, 1]

    def to_html(self) -> str:
        res = f"{self.pref_p(0)}<sup>{self.post_p(0)}</sup>"
        return res
    
class LatexTokenPMOD(LatexToken):
    latex_to_html = [r"\pmod", None, 0, 1]
    
    def to_html(self) -> str:
        res = f'(mod {self.post_p(0)})'
        return res
    
class LatexBlock:
    def __init__(self, st : str = "", cont : T_AST = []) -> None:
        self._content : T_AST = cont
        if (len(self._content) == 0):
            self.__parse(st)
        return

    def __repr__(self) -> str:
        return f"B{self._content}"

    def __str__(self) -> str:
        return f"B{self._content}"

    def to_html(self) -> str:
        res : str = ""
        for elt in self._content:
            if (isinstance(elt, str)):
                res += elt
            else:
                res += elt.to_html()
        return res

    def __parse(self, s : str) -> None:
        self._content = self.__parse_tokens(s)
        self.__atomize_strings()
        self.__parse_blocks()
        self.__parse_class_expressions()
        return

    def __parse_blocks(self) -> None:
        block_found = True
        while (block_found):
            block_found = False
            brace_right = 0
            while ((brace_right < len(self._content)) and (self._content[brace_right] != "}")):
                brace_right = brace_right + 1
            if (brace_right >= len(self._content)):
                continue
            brace_left = brace_right
            while ((brace_left >= 0) and (self._content[brace_left] != "{")):
                brace_left = brace_left - 1
            if (brace_left < 0):
                continue
            block_found = True
            new_content : T_AST = []
            new_content.extend(self._content[0:brace_left])
            new_content.append(LatexBlock(cont = self._content[brace_left+1:brace_right]))
            new_content.extend(self._content[brace_right+1:len(self._content)])
            self._content = new_content
        return

    def __atomize_strings(self) -> None:
        res : T_AST = []
        for elt in self._content:
            if (type(elt) == str):
                for c in elt:
                    res.append(c)
            else:
                res.append(elt)
        self._content = res
        return

    def __parse_tokens(self, s : str) -> T_AST:
        res : T_AST = [s]
        res = LatexToken.parse_tokens(res)
        return res

    def __parse_class_expressions(self) -> None:
        expression_found : bool = True
        cur_pos : int = 0
        while (expression_found):
            expression_found = False
            while ((cur_pos < len(self._content)) and (not (isinstance(self._content[cur_pos], LatexToken)))):
                cur_pos = cur_pos + 1
            if (cur_pos >= len(self._content)):
                continue
            token = self._content[cur_pos]
            assert isinstance(token, LatexToken)
            pre_count : int = token._latex_signature_prefix
            post_count : int = token._latex_signature_postfix
            expression_found = True
            res : List[Union[str, LatexToken, LatexBlock]] = []
            res.extend(self._content[0:cur_pos-pre_count])
            p_pre = []
            for i in range(pre_count):
                p_pre.append(self._content[cur_pos-1-i])
            p_post = []
            for i in range(post_count):
                p_post.append(self._content[cur_pos+1+i])
            token.set_parameters(p_pre, p_post)
            res.append(token)
            new_cur_pos = len(res)
            res.extend(self._content[cur_pos+post_count+1:len(self._content)])
            self._content = res
            cur_pos = new_cur_pos
        return

class LatexFormula(LatexBlock):
    def __init__(self, s : str) -> None:
        LatexBlock.__init__(self, s)
        return

    def __str__(self) -> str:
        return f"F{self._content}"

    def to_html(self) -> str:
        res = LatexBlock.to_html(self)
        return f"<i>{res}</i>"

class LatexText:
    def __init__(self, s : str) -> None:
        self.__content : List[Union[str, LatexFormula]] = []
        self.__parse(s)
        return

    def __parse(self, s : str) -> None:
        res : List[Union[str, LatexFormula]] = []
        cur_position : int = 0
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
        self.__content = res
        return

    def to_html(self) -> str:
        res = ""
        for elt in self.__content:
            if (isinstance(elt, str)):
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
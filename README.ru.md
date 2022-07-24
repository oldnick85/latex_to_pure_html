# latex_to_pure_html

## Описание

Программа для конвертации текста и формул в формате LaTeX в чистый HTML без использования изображений, внешних ресурсов, MathML и т.п.

## Использование

Скрипт можно использовать из командной строки

    python3 latex_to_pure_html.py --latex-string "for \$x\$ we have \$x^y=\\frac{x}{y}\$"

    python3 latex_to_pure_html.py --latex-file file.tex --html-file file.html

либо импортировать из другой программы python и использовать внутренние классы и функции

    text = LatexText(latex_str)
    html_str = text.to_html()
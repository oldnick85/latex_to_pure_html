# latex_to_pure_html

## Description

A program for converting text and formulas in LaTeX format into pure HTML without the use of images, external resources, MathML, etc.

## Usage

The script can be used from the command line 

    python3 latex_to_pure_html.py --latex-string "for \$x\$ we have \$x^y=\\frac{x}{y}\$"

    python3 latex_to_pure_html.py --latex-file file.tex --html-file file.html

or imported from another python program and use internal classes and functions

    text = LatexText(latex_str)
    html_str = text.to_html()
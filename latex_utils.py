from pylatex.utils import NoEscape

def label(labelname):
    s = '\\label{{{labelname}}}'.format(labelname=labelname)
    return NoEscape(s)


def link(labelname, text):
    s = '\\hyperref[{labelname}]{{{text}}}'.format(
        labelname=labelname, text=text
    )
    return NoEscape(s)


def newline():
    return NoEscape(r'\newline')


def newpage():
    return NoEscape(r'\newpage')

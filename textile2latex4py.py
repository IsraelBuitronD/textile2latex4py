#!/usr/bin/env python

import sys
from optparse import OptionParser
sys.path.insert(0,"../..")

import ply.lex as lex
import ply.yacc as yacc
import os

class InitParser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self,lines):
        for line in lines:
            yacc.parse(line)

    
class Textile2LaTeXParser(InitParser):

    tokens = (
        'ALPHANUMTEXT','ALPHATEXT',
        'UNDERSCORE','ASTERISK','CARET','TILDE','NUMBERSIGN',
        'DBLQUOTE',
        'H1','H2','H3','H4','H5',
        'BQ','FN','LCODE','RCODE',
        'TRADEMARK','REGISTERED','COPYRIGHT',
        'newline',
        )

    # Tokens

    t_ignore = " \t"
       
    def t_TRADEMARK(self, t):
        r'\([T|t][M|m]\)'
        return t
       
    def t_COPYRIGHT(self, t):
        r'\([C|c]\)'
        return t
      
    def t_REGISTERED(self, t):
        r'\([R|r]]\)'
        return t
       
    def t_H1(self, t):
        r'h1\. '
        return t
       
    def t_H2(self, t):
        r'h2\. '
        return t
       
    def t_H3(self, t):
        r'h3\. '
        return t
       
    def t_H4(self, t):
        r'h4\. '
        return t
       
    def t_H5(self, t):
        r'h5\. '
        return t
       
    def t_BQ(self, t):
        r'bq\. '
        return t

    def t_FN(self, t):
        r'fn[0-9]+\. '
        return t

    def t_LCODE(self, t):
        r'<code>'
        return t

    def t_RCODE(self, t):
        r'</code>'
        return t
 
    def t_DBLQUOTE(self, t):
        r'\"'
        return t
 
    def t_UNDERSCORE(self, t):
        r'_'
        return t
 
    def t_NUMBERSIGN(self, t):
        r'\#+ '
        return t
 
    def t_ASTERISK(self, t):
        r'\*'
        return t
 
    def t_CARET(self, t):
        r'\^'
        return t

    def t_TILDE(self, t):
        r'~'
        return t
 
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
        print("Illegal character => '%s'" % t.value[0])
        t.lexer.skip(1)
        
    def t_ALPHANUMTEXT(self, t):
        r'[a-zA-Z0-9 ]+'
        return t
        
    def t_ALPHATEXT(self, t):
        r'[a-zA-Z0-9 ]+'
        return t

    # Parsing rules

    def p_textile_content(self,p):
        '''
        textile_content : textile_headers
                        | textile_phrase_modified
                        | dbl_quoted_text
                        | trademark_text
                        | registered_text
                        | copyright_text
                        | blockquote
                        | footnote
                        | superscript_text
                        | subscript_text
                        | list_text
                        | code_text
                        | empty
        '''
        p[0] = p[1]
        print p[0]


    def p_textile_headers(self,p):
        '''
        textile_headers : header1
                        | header2
                        | header3
                        | header4
                        | header5
        '''
        p[0] = p[1]

    def p_header1(self,p):
        '''
        header1 : H1 text
        '''
        p[0] = "\\section{"+p[2]+"}"

    def p_header2(self,p):
        '''
        header2 : H2 text
        '''
        p[0] = "\\subsection{"+p[2]+"}"

    def p_header3(self,p):
        '''
        header3 : H3 text
        '''
        p[0] = "\\subsubsection{" + p[2] + "}"

    def p_header4(self,p):
        '''
        header4 : H4 text 
        '''
        p[0] = "\\paragraph{" + p[2] + "}"

    def p_header5(self,p):
        '''
        header5 : H5 text 
        '''
        p[0] = "\\subparagraph{" + p[2] + "}"

    def p_blockquote(self,p):
        '''
        blockquote : BQ text 
        '''
        p[0] = "\\begin{quote}\n" + p[2] + "\n\\end{quote}"

    def p_code_text(self,p):
        '''
        code_text : LCODE text RCODE
        '''
        p[0] = "\\begin{verbatim}\n" + p[2] + "\n\\end{verbatim}"

    def p_footnote(self,p):
        '''
        footnote : FN text 
        '''
        p[0] = '\\footnote{' + p[2] + '}'

    def p_textile_phrase_modified(self,p):
        '''
        textile_phrase_modified : stronged_text
                                | underlined_text
        '''
        p[0] = p[1]

    def p_superscript_text(self,p):
        '''
        superscript_text : CARET text CARET
                         | CARET textile_phrase_modified CARET
        '''
        p[0] = "\\textsuperscript{" + p[2] + "}"

    def p_subscript_text(self,p):
        '''
        subscript_text : TILDE text TILDE
                       | TILDE textile_phrase_modified TILDE
        '''
        p[0] = "\\textsubscript{" + p[2] + "}"

    def p_stronged_text(self,p):
        '''
        stronged_text : ASTERISK text ASTERISK
                      | ASTERISK textile_phrase_modified ASTERISK
        '''
        p[0] = "\\textbf{" + p[2] + "}"

    def p_underlined_text(self,p):
        '''
        underlined_text : UNDERSCORE text UNDERSCORE
                        | UNDERSCORE textile_phrase_modified UNDERSCORE
        '''
        p[0] = "\\emph{" + p[2] + "}"

    def p_list_text(self,p):
        '''
        list_text : list_item_text list_text
                  | list_item_text
        '''
        if len(p)==2:
            p[0] = "\\begin{enumerate}\n" + p[1] + "\n\\end{enumerate}"
        elif len(p)==3:
            p[0] = "\\begin{enumerate}\n" + p[1] + "\n" + p[2] + "\n\\end{enumerate}"

    def p_list_item_text(self,p):
        '''
        list_item_text : NUMBERSIGN text
                       | NUMBERSIGN textile_phrase_modified
        '''
        p[0] = "\\item " + p[2]

    def p_dbl_quoted_text(self,p):
        '''
        dbl_quoted_text : DBLQUOTE text DBLQUOTE
        '''
        p[0] = "``" + p[2] + "''"

    def p_trademark_text(self,p):
        'trademark_text : TRADEMARK'
        p[0] = '\\texttrademark '

    def p_registered_text(self,p):
        'registered_text : text REGISTERED'
    
    def p_text(self,p):
        '''
        text : ALPHANUMTEXT
             | ALPHATEXT
        '''
        p[0] = p[1]

    def p_copyright_text(self,p):
        'copyright_text : text COPYRIGHT'
        p[0] = p[1] + '\\textcopyright '

    def p_empty(self, p):
        'empty :'
        pass
    
    def p_error(self, p):
        if p:
            print("Syntax error at => '" + p.value + 
                  "' type => '" + p.type + "'")
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    parser = OptionParser(version="%prog 0.1")

    parser.add_option("-f", "--file",
                      action="store", 
                      type="string", 
                      dest="filename",
                      help="read input from a specific file")

    (options, args) = parser.parse_args()

    if options.filename:
        textile_parser = Textile2LaTeXParser()

        file = open(options.filename)
        lines = file.readlines()
        file.close
        textile_parser.run(lines)
    else:
        parser.print_help()


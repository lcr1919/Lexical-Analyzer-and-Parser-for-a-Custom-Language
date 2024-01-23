#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
from audioop import add
from itertools import combinations
from pickle import ADDITEMS, EMPTY_SET
from random import expovariate
import re
from sre_parse import parse_template
from termios import PARENB
from this import d
from urllib.response import addinfourl
from syntax import *


# I *Logan Risner* have written all of this project myself, without any
# unauthorized assistance, and have followed the academic honor code.

    # TODO: scan input string and return a list of its tokens

    # takes a string

    # returns a list of strings (sequence of logical tokens)
def lex(s):

    toks = [] # grab whole string with group 0, just our token with group 2
    while True:

        # removing white space
        m = re.match(r"^(\t|\n|\r| )*", s)
        s = s[len(m.group(0)):]

        # skipping comments
        m = re.match(r"^(/\*[\s\S]*?\*/)", s)

        if m != None:

            s = s[len(m.group(0)):]
            continue

        m = re.match(r"^(//[^\n\r]*)", s)

        if m!= None:

            s = s[len(m.group(0)):]
            continue

        m = re.match(r"^(([a-zA-Z_][a-zA-Z_0-9]*)|([0-9]*\.?[0-9]+)|\^|\(|\)|\;|\{|\}|\=|\*|\-|\:|\,|\+|\/|\<|\>)" ,s)

        if m == None:

            return toks

        else:

            s = s[len(m.group(0)):]
            toks.append(m.group(0))


# TODO: parse and return an AST node or ErrorMsg object

    # takes a list of strings (tokens)

    # returns an AST node from syntax.py

def parse(toks):

    def errorFunc(errorstr):
        print(errorstr)

        raise ValueError(errorstr)

    def isID(s):

        return s not in ["print", "else", "if", "proc", "while", "ret"] and re.match(r"^[_A-Za-z][_A-Za-z0-9]*", s) != None


    def peek(n):
        nonlocal toks
        if len(toks) > n:
            return toks[n]
        else:
            return ""

    def expect(s):
        nonlocal toks
        if s == peek(0):
            toks = toks[1:]
        else:
            errorFunc("Error: expected '%s', but observed '%s'" % (s, peek(0)))


    def parseP(): # return ast
        s = parseS()
        while peek(0) == ";":
            expect(";")
            s = SeqStmt(s, parseS())
        
    def parseS():

        if peek(0) == "proc":
            expect("proc")
        
            if not isID(peek(0)):
                errorFunc("Error: expected name of defined function, but observed '%s'" % (peek(0)))

            x = Var(peek(0))
            expect(peek(0))
            expect("(")

            p = []

            if peek(0) != ")":

                p = [Var(peek(0))]
                expect(peek(0))

                while peek(0) == ",":
                    expect(",")

                    if not isID(peek(0)):
                        errorFunc("Error: expected variable in parameter list, but observed '%s'" % (peek(0)))

                    p.append(Var(peek(0)))
                    expect(peek(0))

            expect(")")
            expect("{") 

            body = parseP()
            expect("}")

            return ProcStmt(x, p, body)

        elif peek(0) == "if":

            expect("if")
            ge = parseC()
            expect("{")
            tbody = parseP() # true body
            expect("}")
            expect("else")
            expect("{")
            fbody = parseP() # false body 
            expect("}")  

            return IfStmt(ge, tbody, fbody) 

        elif peek(0) == "while":

            expect("while")
            ge = parseC()
            expect("{")
            bbody = parseP() 
            expect("}")  
            
            return WhileStmt(ge, bbody)

        elif peek(0) == "print":

            expect("print")

            return PrintStmt(parseC())
        
        else:

            return parseC()
        



    def parseC():

        a = parseE()

        if peek(0) == "<":
            expect("<")

            return LessThan(a, parseE())
        
        elif peek(0) == "=":
            expect("=")

            return Equal(a, parseE())

        else:

            return a



    def parseE():  

        a = parseT()

        if peek(0) == "+":
            expect("+")

            return Plus(a, parseT)

        elif peek(0) == "-":
            expect("-")

            return Minus(a, parseT)

        else:

            return a


    def parseT():

        a = parseF()

        if peek(0) == "*":
            expect("*")

            return Mult(a, parseF)

        elif peek(0) == "/":
            expect("/")

            return Div(a, parseF)

        else:

            return a

    def parseF():

        s = parseA()

        if peek(0) == "^":
            expect("^")
            s = Expo(s, parseA())
        

    def parseA():

        a = parseP()
        # lbody = parseP()
        if peek(0) == "(":
            expect("(")
            if peek(0) == ")":
                expect(")")
                
                return a
            
        elif peek(0) == ":":
            expect(":")
                
            return SeqStmt(a, parseP())
            # return parseP()

        else:

            return parseP()


    try:
        return parseP()

    except ValueError as error:

        return ErrorMsg(error.args[0])

  



            

                
                



    

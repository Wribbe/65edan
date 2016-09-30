package lang.ast; // The generated scanner will belong to the package lang.ast

import lang.ast.LangParser.Terminals; // The terminals are implicitly defined in the parser
import lang.ast.LangParser.SyntaxError;

%%

// define the signature for the generated scanner
%public
%final
%class LangScanner
%extends beaver.Scanner

// the interface between the scanner and the parser is the nextToken() method
%type beaver.Symbol
%function nextToken

// store line and column information in the tokens
%line
%column

// this code will be inlined in the body of the generated scanner class
%{
  private beaver.Symbol sym(short id) {
    return new beaver.Symbol(id, yyline + 1, yycolumn + 1, yylength(), yytext());
  }
%}

// macros
WhiteSpace = [ ] | \t | \f | \n | \r | \s*\/\/.*
ID = [a-zA-Z][a-zA-Z1-9]*
NUMERAL = [1-9]+

%%

// discard whitespace information
{WhiteSpace}  { }

// token definitions
"return"      { return sym(Terminals.RETURN); }
"while"       { return sym(Terminals.WHILE); }
"else"        { return sym(Terminals.ELSE); }
"int"         { return sym(Terminals.INT); }
"if"          { return sym(Terminals.IF); }
"!="          { return sym(Terminals.NOEQ); }
"=="          { return sym(Terminals.EQ); }
"<="          { return sym(Terminals.LTEQ); }
">="          { return sym(Terminals.GTEQ); }
"<"           { return sym(Terminals.LT); }
">"           { return sym(Terminals.GT); }
","           { return sym(Terminals.COMMA); }
"="           { return sym(Terminals.ASSIGN); }
";"           { return sym(Terminals.SEMI); }
"}"           { return sym(Terminals.RBRA); }
"{"           { return sym(Terminals.LBRA); }
")"           { return sym(Terminals.RPAR); }
"("           { return sym(Terminals.LPAR); }
"%"           { return sym(Terminals.REM); }
"/"           { return sym(Terminals.DIV); }
"*"           { return sym(Terminals.MUL); }
"-"           { return sym(Terminals.MINUS); }
"+"           { return sym(Terminals.PLUS); }
{NUMERAL}     { return sym(Terminals.NUMERAL); }
{ID}          { return sym(Terminals.ID); }
<<EOF>>       { return sym(Terminals.EOF); }

/* error fallback */
[^]           { throw new SyntaxError("Illegal character <"+yytext()+">"); }

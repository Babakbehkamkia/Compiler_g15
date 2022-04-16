grammar urlGrammar;

start
   : url EOF
   ;

url
   :  (('http' | 'https') '://') ? 'www.'? (Domain)+ ('/' (Domain)+)*
   ;

Domain
    : [a-zA-Z0-9]+ ('.')* (Symbol)*
    ;

Symbol
    : '%' | '+' | '=' | '-' | '?' | '#'
    ;
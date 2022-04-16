grammar connectionString;

start :
    (left '=' right ';')* EOF
    ;

left :
    (Alphabet | ' ' | '_')+
    ;

right :
    (Alphabet | NonAlphabet)+
    ;

NonAlphabet :
    [(){}.0-9]
   ;

Alphabet :
    [a-zA-Z]
    ;


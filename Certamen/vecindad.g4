grammar vecindad;

prog: instruccion ;

instruccion: configuration ;

configuration: 'CONFIG' '(' 'infectados' '=' infectados ',' 'capas' '=' capas ',' 'tamano' '=' tamano ',' 'propagacion' '=' propagacion ')' ;

infectados: INT;
capas: INT;
tamano: INT;
propagacion: BOOL;


BOOL: 'True' | 'False';
INT: [0-9]+;
WS: [ \t\r\n]+ -> skip;
function stripw(var) {
    gsub(/^[ \t]+/,"",var);
    gsub(/[ \t]+$/,"",var);
    return var
}

/^[[:digit:]]/ {
                 folio = stripw(folio); name=stripw(name); units=stripw(units); date=stripw(date);
                 value = stripw(value); registrar=stripw(registrar); nav = stripw(nav);
                 printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n",folio,name,units,date,nav,value,registrar ;
                 folio = $1 ; name = $2 ; units = $3 ; date  = $4 ; nav = $5 ; value = $6 ; registrar = $7 ; next }
1 { folio=folio $1 ; name=stripw(name) " " stripw($2) ; units=units $3 ; date=date $4 ; nav=nav $5 ; value=value $6 ; registrar=registrar $7}
END {
                 folio = stripw(folio); name=stripw(name); units=stripw(units); date=stripw(date);
                 value = stripw(value); registrar=stripw(registrar); nav = stripw(nav);
                 printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n",folio,name,units,date,nav,value,registrar ; }


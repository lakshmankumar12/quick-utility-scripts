function stripw(var) {
    gsub(/^[ \t]+/,"",var);
    gsub(/[ \t]+$/,"",var);
    gsub(/[ ]{2,}+$/," ",var);
    return var
}
function finish_line() {
    folio = stripw(folio); isin=stripw(isin); name=stripw(name); units=stripw(units); date=stripw(date);
    value = stripw(value); registrar=stripw(registrar); nav = stripw(nav);
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",folio,isin,name,units,date,nav,value,registrar ;
}
BEGIN {
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n","folio","isin","name","units","date","nav","value","registrar";

}
/^[[:digit:]]/ {
    finish_line()
    folio = $1 ; isin = $2 ; name = $3 ; units = $5 ; date  = $6 ; nav = $7 ; value = $8 ; registrar = $9 ; next }
1 {
    folio=folio $1 ;
    isin = isin $2 ;
    name=stripw(name) " " stripw($3) ;
    units=units $5 ;
    date=date $6 ;
    nav=nav $7 ;
    value=value $8 ;
    registrar=registrar $9
}
END {
    finish_line()
}


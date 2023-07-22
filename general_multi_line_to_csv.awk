function stripw(var) {
    gsub(/^[ \t]+/,"",var);
    gsub(/[ \t]+$/,"",var);
    return var
}
function windup (vals, maxcol) {
    for(i=1; i<=maxcol; i++) {
        printf("%s,",stripw(vals[i]));
    }
    printf ("\n")
}
/-------/ {
    windup(vals, maxcol)
    for(i=1; i<=maxcol; i++) {
        vals[i]="";
    }
    next
}
1 {
    if (NF > maxcol) {
        maxcol=NF
    }
    for (i=1;i<=NF;i++) {
        vals[i]=vals[i] " " stripw($i)
    }
}

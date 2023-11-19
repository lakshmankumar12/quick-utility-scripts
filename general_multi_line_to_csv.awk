### process a file like this:
###
###   line1col1  line1col2     line1col3  line1col4
###              line2col2ctd             line2col4ctd
###   ---------
###
###  into:
###
###   line1col1,line1col2 line2col2ctd,line1col3,line1col4 line2col4ctd
###
###  Useful in the mutual-funds consolidated processing where
###  the fund names are split across lines.
###  Manually add the --------- between funds and run this.
###  Add the --------- in the end to process **THE LAST LINE**
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

###  you typeically invoke this as:
###  git lsm | sort | awk -f ..../prepare_make_op_from_git_ls.awk -v tgt_prefix="/path/to/add/in/tgt/" -F/
1 {
    dir = "";
    for (i = 1; i < NF; i++) dir = dir $i "/";  # Build full directory path
    ## special case for files on top-dir
    if (NF == 1) { dir = "./" }
    file = $NF;  # Last field is the filename

    if (dir != prev_dir) {
        if (NR > 1) print "---";
        print dir;                 # Directory header
        print tgt_prefix "/" dir;  # Prefix line
        prev_dir = dir;
        endp = 1;
    }
    print file;
}
END {
    if (endp == 1) print "---"
}

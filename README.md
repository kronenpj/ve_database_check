A utility to compare an ARRL VE Exam Maker database with the NCVEC published
amateur radio question pools to find discrepancies.

The ARRL VE Exam Maker application and database is (C) American Radio Relay League.
The NCVEC question pools are public domain.

```
usage: compare_db [-h] -d DATABASE [-l LEV] [infile [infile ...]]

Compares provided files to the provided database.

positional arguments:
  infile

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
  -l LEV, --lev LEV     Levenshtein distance, default=1
```

The required `database` option specifies the database to which each `infile` is
compared.

the optional `lev` option specifies the Levenshtein distance to use in the
comparisons.

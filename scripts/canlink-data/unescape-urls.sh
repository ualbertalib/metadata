#!/bin/bash

#unescape IRIs
sed 's%\%20%_%g' escapes.txt | sed 's%\%25%_percent_%g' | sed 's$\%C3\%A[12]$a$g' | sed 's$\%C3\%A7$c$g' | sed 's$\%C8\%9B$t$g' > fixed.txt

sed 's$\[1\]$_1_$g' ~/Downloads/escapes.txt > ~/Downloads/nocarets.txt
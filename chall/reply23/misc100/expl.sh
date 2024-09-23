chr() {
    printf "\\$(printf '%o' "$i") "
}

for (( i0 = 32; i0 <= 126; i0++ )); do
    [ $i0 -eq 42 ] && continue
    c0=$(chr $i0)
    echo $c
    for (( i1 = 32; i1 <= 126; i1++ )); do
        [ $i1 -eq 42 ] && continue
        c1=$(chr $i1)
        for (( i2 = 32; i2 <= 126; i2++ )); do
            [ $i2 -eq 42 ] && continue
            c2=$(chr $i2)
            echo -e "${c0}${c1}${c2}"
        done
    done
done

# rm flag.txt
# for c in {g..z} {A..Z} {0..9}; do
#     echo $c
#     for c1 in {a..z} {A..Z} {0..9}; do
#         echo i: $c1
#         for c2 in {a..z} {A..Z} {0..9}; do
#             PWD="900802jfeng@veryrealmail.com$c$c1${c2}R3ply!"
#             OUT="$(7z x -p"$PWD" important_dental_information.zip 2>&1)"
#             if [ -z "$(echo "$OUT" | grep -E "(ERROR: Wrong password|ERROR: CRC Failed in encrypted file)")" ]
#             then
#                 echo pwd $PWD
#                 echo out $OUT
#                 exit 0
#             fi
#             rm flag.txt
#         done
#     done
# done

# echo sticazzi
# exit 1

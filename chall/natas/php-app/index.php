<?php

function xor_encrypt($in, $key) {
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

$cookie = 'MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY%3D';

// $my = "0l;$$98-8=?#9*jvi 'ngl*+(!$#9lrnh(.*-(.n67";
$my = base64_decode($cookie);

$jenc = json_encode(
    array( "showpassword"=>"no", "bgcolor"=>"#ffffff")
);

$hack = json_encode(
    array( "showpassword"=>"yes", "bgcolor"=>"#ffffff")
);

$key = $my ^ $jenc;

echo 'key: ', substr($key, 0, 4), "\n";
echo 'hack: ', base64_encode(xor_encrypt($hack, substr($key, 0, 4))), "\n";

?>

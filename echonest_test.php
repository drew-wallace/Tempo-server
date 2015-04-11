<?php

function debug_to_console($data) {
    if(is_array($data) || is_object($data))
	{
		echo("<script>console.log('".json_encode($data)."');</script>");
	} else {
		echo("<script>console.log('".$data."');</script>");
	}
}

$url = "http://developer.echonest.com/api/v4/song/search?api_key=NHSTSBEENVYUFRLY5&title=thunderstruck&artist=ac/dc&bucket=audio_summary";
//  Initiate curl
$ch = curl_init();
// Disable SSL verification
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
// Will return the response, if false it print the response
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// Set the url
curl_setopt($ch, CURLOPT_URL,$url);
// Execute
$result=curl_exec($ch);
// Closing
curl_close($ch);

//debug_to_console($result);
echo "<pre>";
print_r(json_decode($result, true)['response']['songs'][0]['audio_summary']);
echo "</pre>";
?>

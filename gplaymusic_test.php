<html>
<head>
	<meta charset="UTF-8"> 
</head>
<body>

<pre>
<?php 
	ob_start();
	passthru('python /home/drew/tempo_scripts/gplaymusic.py');
	$data = ob_get_clean();
?>
</pre>

<script>
	var tracks = <?php echo $data; ?>;
	console.log(tracks);
	document.write(tracks[0].artist + " - " + tracks[0].title + "\n");
	document.write("<pre>" + JSON.stringify(tracks[0], null, 2) + "</pre>");
</script>

<?php
$artist = json_decode($data, true)[0]["artist"];
$title = json_decode($data, true)[0]["title"];
//echo $artist . " - " . $title . "\n";

$url = "http://developer.echonest.com/api/v4/song/search?api_key=NHSTSBEENVYUFRLY5&title=".urlencode($title)."&artist=".urlencode($artist)."&bucket=audio_summary&bucket=artist_discovery&bucket=artist_familiarity&bucket=artist_hotttnesss&bucket=artist_location&bucket=song_currency&bucket=song_discovery&bucket=song_hotttnesss&bucket=song_type";

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
echo "<pre>";
print_r(json_decode($result, true)['response']['songs'][0]);//['audio_summary']);
echo "</pre>";

?>

</body>
</html>

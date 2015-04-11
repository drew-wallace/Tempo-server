<?php 
	ob_start();
	passthru('python /home/drew/tempo_scripts/5songs.py');
	$data = ob_get_clean();
	echo $data;
?>

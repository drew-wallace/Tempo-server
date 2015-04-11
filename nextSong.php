<?php 
	if(isset($_GET['pid']) && isset($_GET['bpm']) && isset($_GET['cluster'])) {
		ob_start();
		passthru('python /home/drew/tempo_scripts/nextSong.py '.$_GET['pid'].' '.$_GET['bpm'].' '.$_GET['cluster']);
		$data = ob_get_clean();
		echo $data;
	}
?>

<?php 
	if(isset($_GET['sid'])) {
		ob_start();
		if(isset($_GET['action'])) {
			passthru('python /home/drew/tempo_scripts/streamURL.py '.$_GET['sid'].' '.$_GET['action']);
		} else {
			passthru('python /home/drew/tempo_scripts/streamURL.py '.$_GET['sid']);
		}
		$data = ob_get_clean();
		echo $data;
	}
?>

<?php 
	if(isset($_GET['pid'])) {
		ob_start();
		passthru('python /home/drew/tempo_scripts/viewplaylists.py '.$_GET['pid']);
		$data = ob_get_clean();
		echo $data;
	}
?>

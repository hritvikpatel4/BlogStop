<?php
	//get the movie part that was sent by the client
	extract($_GET);

	$xml = simplexml_load_file("feed.xml");
	$names = array();
	
    foreach($xml->post as $post) {
               array_push($names, (string)$post->user);     
	}

	$myfile = fopen("newfile.txt", "w");
	$res = array_unique($names);

	foreach($res as $value){
		fwrite($myfile, $value.PHP_EOL);
	}

	$file=fopen("newfile.txt","r");
	$moviearray=array();
	
	while ($line=fgets($file)) {
		$movie=trim($line);
			if(strncasecmp($moviepart, $movie, strlen($moviepart))==0){
				$moviearray[]=$movie;
		}
	}
	echo json_encode($moviearray);

?>
<?php
    
    $id = $_GET['id'];
    $xml = simplexml_load_file("feed.xml");
    
    // Create a child in the first topic node
    foreach($xml->post as $post) {
        if ($post['id'] == $id){
            $var = (int)$post->likes+1;
            echo $var."\n";
            $post->likes = $var;
        }    
    }
    


$xml->asXML("feed.xml");

?>
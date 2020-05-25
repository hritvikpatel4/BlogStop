<?php
    
    $id = $_GET['id'];
    $cmt = $_GET['comment'];
    $xml = simplexml_load_file("feed.xml");
    
    // Create a child in the first topic node
    foreach($xml->post as $post) {
        if ($post['id'] == $id){
            $child = $post->addChild("comments");
            $child[0] = $cmt;
        }    
    }
    


$xml->asXML("feed.xml");

?>
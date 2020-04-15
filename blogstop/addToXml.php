<?php
    
    $id = $_POST['id'];
    $content = $_POST['content'];
    $title  = $_POST['title'];
    $tags = $_POST['tags'];
    $xml = simplexml_load_file("feed.xml");
    $user = $_COOKIE['username'];
    // Create a child in the first topic node
    $child = $xml->addChild("post");
   
    $child->addAttribute("id", "$id");
    $child->addChild("title")[0] = $title;
    $child->addChild("user")[0] = $user;
    $child->addChild("date")[0] = date("d-m-Y");
    $child->addChild("tags")[0] = $tags;
    $child->addChild("likes")[0] = 0;
    $child->addChild("content")[0]=$content;

$xml->asXML("feed.xml");

?>
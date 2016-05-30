<?php
   // connect to mongodb
   $m = new MongoClient();
   echo "Connection to database successfully";
	
   // select a database
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";

   $cursor = $collection->find();
   // iterate cursor to display title of documents
	$start = microtime(true);
	for($i = 0; $i < 10; $i++){
		$document = array( 
		  "title" => "MongoDB", 
		  "description" => "database", 
		  "likerinos" => 100,
		  "created_on"=> microtime(true)
	   );
	   $collection->insert($document);
	}
	echo microtime(true)-$start."secs\n";
	
   foreach ($cursor as $document) {
      //echo $document["_id"] . "\n";
   }
?>

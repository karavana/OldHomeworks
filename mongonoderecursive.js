//This code requires mongoose node module
var mongoose = require('mongodb').MongoClient;

//connecting local mongodb database named test
var minDate = new Date(2016, 0, 1, 0, 0, 0, 0);
var maxDate = new Date(2017, 0, 1, 0, 0, 0, 0);
var delta = maxDate.getTime() - minDate.getTime();
 
var start = new Date();
var count = 0;


//testing connectivity
mongoose.connect("mongodb://localhost:27017/test",function(err, db) {
  if(err) { return console.dir(err); }
	var go = function(){
		var date = new Date(minDate.getTime() + Math.random() * delta);
		var value = Math.random();
		var document = {        
			created_on : date,
			value : value
		};
		var collection = db.collection('testerino');
		collection.insert(document, function(err, res){		
			count++;
			if (count === 50000) {
			  var end = new Date();
			  console.log(count + ' in ' + (new Date() - start)/1000.0 + 's');
			  db.close();
			}
			else{
				go();
			}
		});
	}
	go(); //start the process	
});



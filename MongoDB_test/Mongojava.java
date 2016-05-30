import com.mongodb.MongoClient;
import com.mongodb.MongoException;
import com.mongodb.WriteConcern;

import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import com.mongodb.DBCursor;

import com.mongodb.ServerAddress;
import java.util.Arrays;

public class Mongojava {

   public static void main( String args[] ) {
	
      try{
				  
		final long start = System.nanoTime();
		
         // To connect to mongodb server
        MongoClient mongoClient = new MongoClient( "localhost" , 27017 );
			
        // Now connect to your databases
        DB db = mongoClient.getDB( "test" );
        System.out.println("Connect to database successfully");
        //boolean auth = db.authenticate(myUserName, myPassword);
        //System.out.println("Authentication: "+auth);
		DBCollection coll = db.getCollection("testCollection");
		mongoClient.setWriteConcern(WriteConcern.JOURNALED);
		for(int i = 0; i < 10000; i++){
			
			BasicDBObject doc = new BasicDBObject("name", "MongoDB")
				.append("type", "database")
				.append("count", 1)
				.append("created_on", System.nanoTime());
			coll.insert(doc);
			if(i%500 == 0)
				System.out.println(i);
		}

		final long end = System.nanoTime();

		System.out.println("Took: " + ((end - start) / 1000000) + "ms");
			
      }catch(Exception e){
        System.err.println( e.getClass().getName() + ": " + e.getMessage() );
      }
   }
}



//BasicDBObject doc = new BasicDBObject("name", "MongoDB")
//        .append("type", "database")
//        .append("count", 1)
//        .append("info", new BasicDBObject("x", 203).append("y", 102));
//coll.insert(doc);


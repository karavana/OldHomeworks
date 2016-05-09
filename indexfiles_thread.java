package com.lucene;


import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.core.LowerCaseFilter;
import org.apache.lucene.analysis.ngram.NGramTokenizer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.LongField;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.DocsEnum;
import org.apache.lucene.index.Fields;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.search.DocIdSetIterator;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.AttributeFactory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.analysis.core.StopFilter;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

/** Index all text files under a directory.
 * <p>
 * This is a command-line application demonstrating simple Lucene indexing.
 * Run it with no command-line arguments for usage information.
 */
public class IndexFiles {
  
  private static IndexWriter writer;
  private static HashMap<String, Float> termFrequencies;
  private static HashMap<String, Float> invertedDocumentFrequencies;
  private IndexFiles() {}

  /** Index all text files under a directory. */
  public static void main(String[] args) {
    String usage = "java org.apache.lucene.demo.IndexFiles"
                 + " [-index INDEX_PATH] [-docs DOCS_PATH] [-update]\n\n"
                 + "This indexes the documents in DOCS_PATH, creating a Lucene index"
                 + "in INDEX_PATH that can be searched with SearchFiles";
    String indexPath = "index";
    String docsPath = null;
    boolean create = true;
    for(int i=0;i<args.length;i++) {
      if ("-index".equals(args[i])) {
        indexPath = args[i+1];
        i++;
      } else if ("-docs".equals(args[i])) {
        docsPath = args[i+1];
        i++;
      } else if ("-update".equals(args[i])) {
        create = false;
      }
    }
    /*******************************************************************************************************************/
    /*******************************************KGramGenerationDemonstration********************************************/
    /*AttributeFactory factory = AttributeFactory.DEFAULT_ATTRIBUTE_FACTORY;
	 //  Lucene 5.x
	 NGramTokenizer tokenizer = new NGramTokenizer(factory,3,10);
	 tokenizer.setReader(new StringReader("now we'r heading up highh, where no harm would get in our way"));
	 tokenizer.reset();
	
	 // Then process tokens - same between 4.x and 5.x
	 // NOTE: Here I'm adding a single expected attribute to handle string tokens,
	 //  but you would probably want to do something more meaningful/elegant
	 CharTermAttribute attr = tokenizer.addAttribute(CharTermAttribute.class);
	 while(tokenizer.incrementToken()) {
	     // Grab the term
	     String term = attr.toString();
	     System.out.println(term);
	     // Do something crazy...
	 }
	 tokenizer.close();*/
	 /*******************************************************************************************************************/
	 /*******************************************************************************************************************/
    if (docsPath == null) {
      System.err.println("Usage: " + usage);
      System.exit(1);
    }

    final Path docDir = Paths.get(docsPath);
    if (!Files.isReadable(docDir)) {
      System.out.println("Document directory '" +docDir.toAbsolutePath()+ "' does not exist or is not readable, please check the path");
      System.exit(1);
    }
    
    Date start = new Date();
    try {
      System.out.println("Indexing to directory '" + indexPath + "'...");

      Directory dir = FSDirectory.open(Paths.get(indexPath));
      //Directory ramDir = new RAMDirectory();
      Analyzer analyzer = new Analyzer(){   //first time creation of index without gram reduction
		  @Override
		  protected TokenStreamComponents createComponents(String fieldName){
			AttributeFactory factory = AttributeFactory.DEFAULT_ATTRIBUTE_FACTORY;
			Tokenizer source = new NGramTokenizer(factory,3,10);
			TokenStream filter = new LowerCaseFilter(source);
			filter = new NewlineFilter(filter);
			//filter = new presufFilter(filter);
			filter = new EmptySpaceFilter(filter);
			return new TokenStreamComponents(source,filter);
		  };
	  };
      //Analyzer analyzer = new StandardAnalyzer(); //for testing if this is faster
      IndexWriterConfig iwc = new IndexWriterConfig(analyzer);

      if (create) {
        // Create a new index in the directory, removing any
        // previously indexed documents:
        iwc.setOpenMode(OpenMode.CREATE);
      } else {
        // Add new documents to an existing index:
        iwc.setOpenMode(OpenMode.CREATE_OR_APPEND);
      }

      // Optional: for better indexing performance, if you
      // are indexing many documents, increase the RAM
      // buffer.  But if you do this, increase the max heap
      // size to the JVM (eg add -Xmx512m or -Xmx1g):
      //
      //iwc.setRAMBufferSizeMB(256.0);

      writer = new IndexWriter(dir, iwc); //writes to files
      //IndexWriter writer = new IndexWriter(ramDir, iwc); //writes to RAM
      indexDocs(writer, docDir);

      // NOTE: if you want to maximize search performance,
      // you can optionally call forceMerge here.  This can be
      // a terribly costly operation, so generally it's only
      // worth it when your index is relatively static (ie
      // you're done adding documents to it):
      //
      // writer.forceMerge(1);

      writer.close();
      
      Date end = new Date();
      System.out.println(end.getTime() - start.getTime() + " total milliseconds passed for indexing");
      String field = "contents";
      IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath))); //reads index files
      //IndexReader reader = DirectoryReader.open(ramDir); //reads index stored in RAM

      
      //****************FREQUENCY COMPUTATION******************//
      Date freqstart = new Date();
      termFrequencies = new HashMap<String, Float>();
      invertedDocumentFrequencies = new HashMap<String, Float>();
      invertedDocumentFrequencies = getIdfs(reader, field);
      
      Date freqend = new Date();
      System.out.println(freqend.getTime() - freqstart.getTime() + " total milliseconds to find the frequencies ");
     
      //create a directory to store numeric data
      File directory = new File("numeric_data");
      if(!directory.exists()){
    	  directory.mkdir();
      }
      /*for (String term: tf_Idf_Weights.keySet()){
    	  String value = tf_Idf_Weights.get(term).toString();
    	  System.out.println(term + " ~---~ " + value);
      }*/
    
      System.out.println("Updating index with stop words");
      analyzer = new Analyzer(){ //this is to update the index by discarding useless grams coming from the frequency calculation
		  @Override
		  protected TokenStreamComponents createComponents(String fieldName){
			AttributeFactory factory = AttributeFactory.DEFAULT_ATTRIBUTE_FACTORY;
			Tokenizer source = new NGramTokenizer(factory,3,10);
			List<String> stopWords = (List<String>) cUselessGrams((float) 0.01, invertedDocumentFrequencies, reader);
			/*for(String stopWord: stopWords){
				System.out.println(stopWord);
			}*/
			System.out.println("Number of useless grams: " + stopWords.size());
			TokenStream filter = new StopFilter(source,StopFilter.makeStopSet(stopWords));
			filter = new LowerCaseFilter(source);
			filter = new NewlineFilter(filter);
			//filter = new presufFilter(filter);
			filter = new EmptySpaceFilter(filter);
			return new TokenStreamComponents(source,filter);
		  };
	  };
      //analyzer = new StandardAnalyzer(); //for testing if this is faster
	  
      iwc = new IndexWriterConfig(analyzer);
      iwc.setOpenMode(OpenMode.CREATE_OR_APPEND);
      writer = new IndexWriter(dir, iwc);
      indexDocs(writer, docDir);
      writer.close();
      System.out.println("Updating done");
      termFrequencies = getFrequencyMap(reader,field);
      
      termFrequencies = sortByValues(termFrequencies);
      //Write full filtered term list into file here
      try (Writer fileWriter = new BufferedWriter(new OutputStreamWriter(
              new FileOutputStream("numeric_data/terms.txt"), "utf-8"))) {
    	  	for (String term: termFrequencies.keySet()){
              fileWriter.write(term + "\n");
    	  	}
	  }
      //For observing frequencies
      try (Writer fileWriter = new BufferedWriter(new OutputStreamWriter(
              new FileOutputStream("numeric_data/frequencies.txt"), "utf-8"))) {
    	  	for (String term: termFrequencies.keySet()){
              String value = termFrequencies.get(term).toString();  
              //System.out.println(term + " -> " + value);
              fileWriter.write(term + " -> " + value + "\n");
    	  	}
	  }
      
      invertedDocumentFrequencies = getIdfs(reader, field);
      invertedDocumentFrequencies = sortByValues(invertedDocumentFrequencies);
      
      //System.out.println("(MAX) . bill wil's selectivity -> " + selectivity(". bill wil", invertedDocumentFrequencies, reader));
      //System.out.println("(MIN)  so 's selectivity -> " + selectivity(" so ", invertedDocumentFrequencies, reader));
      //System.out.println("c: " + determineIndexSelectivity(invertedDocumentFrequencies));
      //System.out.println("#of useless grams: " + cUselessGrams((float) 0.01, invertedDocumentFrequencies, reader).size());
      
      //For observing idfs
      try (Writer fileWriter = new BufferedWriter(new OutputStreamWriter(
              new FileOutputStream("numeric_data/idfs.txt"), "utf-8"))) {
    	  	for (String term: invertedDocumentFrequencies.keySet()){
              String value = invertedDocumentFrequencies.get(term).toString();  
              //System.out.println(term + " -> " + value);
              fileWriter.write(term + " -> " + value + "\n");
    	  	}
	  }
      reader.close();
    } catch (IOException e) {
      System.out.println(" caught a " + e.getClass() +
       "\n with message: " + e.getMessage());
    }
  }
  
  /*** GET ALL THE TOTALFREQS ***/
  static HashMap<String, Float> getFrequencyMap(IndexReader reader, String field) throws IOException
  {
	  HashMap<String, Float> termFrequencies = new HashMap<>();
	  final Terms terms = MultiFields.getTerms(reader, field);
	  TermsEnum termsEnum = terms.iterator();
	  BytesRef bytesRef = null;
      while ((bytesRef = termsEnum.next()) != null) {
    	  if(termsEnum.seekExact(bytesRef)){//seeks to the exact term
	    	  bytesRef = termsEnum.term();
	    	  String term = bytesRef.utf8ToString();
		      float frequency = reader.totalTermFreq(new Term(field,term));//reference variable is faster
		      termFrequencies.put(term, frequency);
    	  }
      }
      return termFrequencies;
  }
  
  /*** GET ALL THE IDFs ***/
  public static HashMap<String, Float> getIdfs(IndexReader reader, String field) throws IOException
     {
  	  	HashMap<String, Float> docFrequencies = new HashMap<>();
     
	    TermsEnum termEnum = MultiFields.getTerms(reader, field).iterator();
	    BytesRef bytesRef = null;
	    while ((bytesRef = termEnum.next()) != null) 
	    {
	        if (termEnum.seekExact(bytesRef)) 
	        {
	        	String term = bytesRef.utf8ToString(); 
	        	float idf = (float) Math.log(reader.numDocs()/(double) (termEnum.docFreq()+1) + 1.0);
	        	//System.out.println(term + "'s docfreq = " + termEnum.docFreq() + " and number of docs is " + reader.numDocs());
	            docFrequencies.put(term, idf); 
	        }
	    }
	    return docFrequencies;
     }

  /**
   * Indexes the given file using the given writer, or if a directory is given,
   * recurses over files and directories found under the given directory.
   * 
   * NOTE: This method indexes one document per input file.  This is slow.  For good
   * throughput, put multiple documents into your input file(s).  An example of this is
   * in the benchmark module, which can create "line doc" files, one document per line,
   * using the
   * <a href="../../../../../contrib-benchmark/org/apache/lucene/benchmark/byTask/tasks/WriteLineDocTask.html"
   * >WriteLineDocTask</a>.
   *  
   * @param writer Writer to the index where the given file/dir info will be stored
   * @param path The file to index, or the directory to recurse into to find files to index
   * @throws IOException If there is a low-level I/O error
   */
  static void indexDocs(final IndexWriter writer, Path path) throws IOException {
    if (Files.isDirectory(path)) {
      Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
        @Override
        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
          try {
            Thread docAdder = new indexDoc(writer, file, attrs.lastModifiedTime().toMillis());
			docAdder.start();
			docAdder.join();
          } catch (IOException ignore) {
            // don't index files that can't be read.
          }
          return FileVisitResult.CONTINUE;
        }
      });
    } else {
         Thread docAdder = new indexDoc(writer, path, Files.getLastModifiedTime(path).toMillis());
		 docAdder.start();
		 docAdder.join();
    }
  }

  
  	private static HashMap<String, Float> sortByValues(HashMap<String, Float> map) { //function for sorting frequencies in ascending order
  		//SORTS A HASHMAP BY VALUES
  	    List list = new LinkedList(map.entrySet());
  	    // Defined Custom Comparator here
  	    Collections.sort(list, new Comparator() {
  	         public int compare(Object o1, Object o2) {
  	            return ((Comparable) ((Map.Entry) (o1)).getValue())
  	               .compareTo(((Map.Entry) (o2)).getValue());
  	         }
  	    });
  	
  	    // Here I am copying the sorted list in HashMap
  	    // using LinkedHashMap to preserve the insertion order
  	    HashMap sortedHashMap = new LinkedHashMap();
  	    for (Iterator it = list.iterator(); it.hasNext();) {
  	           Map.Entry entry = (Map.Entry) it.next();
  	           sortedHashMap.put(entry.getKey(), entry.getValue());
  	    } 
  	    return sortedHashMap;
  	}
	public static float selectivity(String term, HashMap<String, Float> frequencyMap, IndexReader reader){
		float totalTermCount = 0;
		float termFrequency = frequencyMap.get(term);
		//System.out.println("Term Freq: " + termFrequency);
		//System.out.println("Total Term Count: " + totalTermCount);
  		return termFrequency/reader.numDocs();
  	}
	
	public static ArrayList<String> cUselessGrams(float c, HashMap<String, Float> frequencyMap, IndexReader reader){
		//need reverse order iteration
		ArrayList<String> uselessGrams = new ArrayList<>();
		List<Entry<String,Float>> list = new ArrayList<>(frequencyMap.entrySet());
		//System.out.println("creating useless gram list");
		for( int i = list.size() -1; i >= 0 ; i --){
		    String term = list.get(i).getKey();
		    //System.out.println("Looking for " + term + " if its useless");
		    if (selectivity(term, frequencyMap, reader) > c){//if selectivity is large, it is not very useful
				//System.out.println("It is useless");
				uselessGrams.add(term);
		    }
		    else{
		    	break;
		    }
		}
		return uselessGrams;
	}
	
	public static float determineIndexSelectivity(HashMap<String, Float> frequencyMap){
		float totalTermCount = 0;
		for (float freq: frequencyMap.values()){
            totalTermCount += freq;
  	  	}
		float numberOfDistinctKey = frequencyMap.size();
		
		float defaultIndexSelectivity = numberOfDistinctKey/totalTermCount;
		//System.out.println("Distinct key: " + numberOfDistinctKey);
		//System.out.println("Default index selectivity: " + defaultIndexSelectivity);
		return defaultIndexSelectivity;
	}
}





/** Indexes a single document */
 public class indexDoc extends Thread {
	 
	 public IndexWriter writer;
	 public Path file;
	 public long lastModified;
	 
	 public indexDoc(IndexWriter writer, Path file, long lastModified){
		 this.writer = writer;
		 this.file = file;
		 this.lastModified = lastModified;
	 }
	 public void run() throws IOException{
	 
		try (InputStream stream = Files.newInputStream(file)) {
		  // make a new, empty document
		  Document doc = new Document();
		  
		  // Add the path of the file as a field named "path".  Use a
		  // field that is indexed (i.e. searchable), but don't tokenize 
		  // the field into separate words and don't index term frequency
		  // or positional information:
		  Field pathField = new StringField("path", file.toString(), Field.Store.YES);
		  doc.add(pathField);
		  
		  // Add the last modified date of the file a field named "modified".
		  // Use a LongField that is indexed (i.e. efficiently filterable with
		  // NumericRangeFilter).  This indexes to milli-second resolution, which
		  // is often too fine.  You could instead create a number based on
		  // year/month/day/hour/minutes/seconds, down the resolution you require.
		  // For example the long value 2011021714 would mean
		  // February 17, 2011, 2-3 PM.
		  doc.add(new LongField("modified", lastModified, Field.Store.NO));
		  
		  // Add the contents of the file to a field named "contents".  Specify a Reader,
		  // so that the text of the file is tokenized and indexed, but not stored.
		  // Note that FileReader expects the file to be in UTF-8 encoding.
		  // If that's not the case searching for special characters will fail.
		  doc.add(new TextField("contents", new BufferedReader(new InputStreamReader(stream, StandardCharsets.UTF_8))));
		  if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
			// New index, so we just add the document (no old document can be there):
			System.out.println("adding " + file);
			writer.addDocument(doc);
		  } else {
			// Existing index (an old copy of this document may have been indexed) so 
			// we use updateDocument instead to replace the old one matching the exact 
			// path, if present:
			System.out.println("updating " + file);
			writer.updateDocument(new Term("path", file.toString()), doc);
		  }
		}
	 }
  }
  


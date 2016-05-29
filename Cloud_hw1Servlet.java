package com.cloud;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

import javax.servlet.http.*;

import com.google.appengine.api.search.*;

@SuppressWarnings("serial")
public class Cloud_hw1Servlet extends HttpServlet {
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		
		
		SearchService searchService = SearchServiceFactory.getSearchService();
		Index index = searchService.getIndex(
		      IndexSpec.newBuilder().setName("indexx"));
		 
		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream("PP.txt"),"UTF-8"));                
		
	   String lines = br.readLine();
	    ArrayList<String> buffer = new ArrayList<String>();
	    String paragraphID = "1";
	    String chapterID = "1";
        int pid = Integer.parseInt(paragraphID);
		int cid = Integer.parseInt(chapterID);

    	
	    
	    while(lines != null)
        {   
            
            if(lines != null)
            {   
                StringBuilder str = new StringBuilder();
                String[] splitStr = lines.split(" ");

                if(splitStr[0].contains("chapter") && splitStr[1].contains("paragraph")){
                		chapterID = splitStr[0].substring(7);
                		paragraphID = splitStr[1].substring(9);
                		pid = Integer.parseInt(paragraphID);
                		cid = Integer.parseInt(chapterID);
	
            	}	
                else{
	                
	                	for (int i = 0; i < splitStr.length; i++) {
		                    str.append(splitStr[i]).append(" ");
		                }
		
		                buffer.add(str.toString());  

                		StringBuilder sb = new StringBuilder();

                		for(String newparagraph : buffer){
                			sb.append(newparagraph);
                		}

                		Document document = Document.newBuilder()
                			.addField(Field.newBuilder()
                				.setName("chapterId")
                				.setNumber(cid))
                			.addField(Field.newBuilder()
                				.setName("paragraphId")
                				.setNumber(pid))
                			.addField(Field.newBuilder()
                				.setName("content")
                				.setText(sb.toString()))
      	    			      .build();

                		try {
                		    index.put(document);
                		  } catch (PutException e) {
                		    if (StatusCode.TRANSIENT_ERROR.equals(e.getOperationResult().getCode())) {
                		    	index.put(document);
                		    }
                		  }
               		    buffer.clear();

                		//System.out.println(sb.toString()); System.out.println(cid);System.out.println(pid);
	            }
            }

            lines=br.readLine();
        }
	    
	    String queryString = req.getParameter("q");
	    SortOptions sortOptions = SortOptions.newBuilder()
	    	       .addSortExpression(SortExpression.newBuilder()
	    	           .setExpression("chapterId")
	    	           .setDirection(SortExpression.SortDirection.ASCENDING))
	    	       .addSortExpression(SortExpression.newBuilder()
	    	           .setExpression("paragraphId")
	    	           .setDirection(SortExpression.SortDirection.ASCENDING))
	    	       .setLimit(1000)
	    	       .build();
	    QueryOptions options = QueryOptions.newBuilder()
	    	     .setLimit(1000)
	    	     .setSortOptions(sortOptions)
	    	     .build();
	    
	    Query query = Query.newBuilder()
	    	     .setOptions(options)
	    	     .build(queryString);
	    
	    resp.getWriter().println("Results for " + "\""+queryString+"\""+"\n");
	    Results<ScoredDocument> results = index.search(query);
	    for (ScoredDocument document : results) {
	    	
	    	resp.getWriter().println("Chapter "+document.getOnlyField("chapterId").getNumber().intValue()+" Paragraph " + document.getOnlyField("paragraphId").getNumber().intValue()+"\n");
	    	resp.getWriter().println(document.getOnlyField("content").getText()+"\n");
	    	
	    }

       br.close();

	}
}

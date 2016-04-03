Insight Data Engineering - Coding Challenge -- Submition by Pradeep Gharat pgh01@hotmail.com
===============================================================================================

# Table of Contents
1. [Overview](README.md#Overview)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Testing](README.md#testing)
4. [Possible enhancements](README.md#future-enhancements)


## Overview
[Back to Table of Contents](README.md#table-of-contents)
  Tested using python 2.7 on windows+cygwin laptop. Following python libraries are used by this code:json,datetime,itertools,collections and sys.
  The approach taken for implementing this solution was to create a NESTED Dictionary ( defaultdict(dict)) structure that holds the Node & Edge information
along with time stamp. The outer dict holds the node name. Its value is another dict which has edge name and timestamp as the Key value pair. 
For example a 'Apache' --> 'Storm' Arc created at 'Mar 06 2016 23:05:52' would be stored as { Apache  : { Storm : Mar 06 2016 23:05:52 }}.
   A Class called Graph manages the dict contents via published methods 
	  add_edge    : for new hashtag set, add 2 entries (node1 --> node2) and (node2-->node1).
       count_nodes : count of number of nodes in the graph
       list_nodes  : list of node names in the graph
       count_edges : list of tuples. tuples are in the (1,n) form where n is count of edges.
       get_avgVertex : returns the degree of vertex in the graph in decimal format rounded to 2 places.
       list_edges  : list of edges for a given node
       prune_nodes : removes edges that fall out of the 60 second window. removes nodes without edges.
 


## Details of Implementation
[Back to Table of Contents](README.md#table-of-contents)
   The alogrithm for the program is as follows:
	1. Open files and initialize the Graph object
	2. For reach record in the tweet input file
		2.a parse to record to json format, ignore if error and pass to next record.
		2.b get the created_at timestamp and list of hash tags
		2.c update maxtimestamp and cutoff time values
		2.d if #hash tags > 2 and timestamp within the window create pairs of hashtag names representing a edge
		2.e prune any edges and nodes that have fallen beyond the time window
		2.f calculation the degree of vertex and write to the output file
      3. Close the files and exit

3. [Testing](README.md#testing)
	3.A. Ran the Insight Engineering provided test ( manually checked the results from temp folder and the run output folder since the diff
         was missing. the results had correct 2 records in the output.
		
			C:\insightCode\pgh-challenge-master\insight_testsuite>bash run_tests.sh
			run_tests.sh: line 61: diff: command not found
			[PASS]: test-2-tweets-all-distinct
	3.B Run the program using the testdata01.txt file. the input timestamp and hash tags are
			2016-03-28 23:23:12 [u'hiring', u'PaloAlto', u'Healthcare', u'Job', u'Jobs']
			
			C:\insightCode\pgh-challenge-master\insight_testsuite\test_pgh\tweet_output>cat testout01.txt
			4.0
	3.C Run the program using the testdata01.txt file. the input timestamp and hash tags are:
			2016-03-24 17:51:10 [u'Spark', u'Apache']

C:\insightCode\pgh-challenge-master\insight_testsuite>python ../src/average_degree.py ./test_pgh/tweet_input/testdata02.txt 
	./test_pgh/tweet_output/testout02.txt

C:\insightCode\pgh-challenge-master\insight_testsuite>cat ./test_pgh/tweet_output/testout02.txt
1.0

3.D  Run the program using the testdata01.txt file. the input timestamp and hash tags are:

2016-03-24 17:51:10 [u'Spark', u'Apache']
2016-03-24 17:51:15 [u'Storm', u'Apache', u'Hadoop']

C:\insightCode\pgh-challenge-master\insight_testsuite>python ../src/average_degree.py 
./test_pgh/tweet_input/testdata03.txt ./test_pgh/tweet_output/testout03.txt

C:\insightCode\pgh-challenge-master\insight_testsuite>cat ./test_pgh/tweet_output/testout03.txt
1.0
2.0

3.E  Run the program using the testdata01.txt file. the input timestamp and hash tags are:

2016-03-24 17:51:10 [u'Spark', u'Apache']
2016-03-24 17:51:15 [u'Storm', u'Apache', u'Hadoop']
2016-03-24 17:51:30 [u'Apache']
2016-03-24 17:51:55 [u'Spark', u'Flink']
2016-03-24 17:51:58 [u'Spark', u'Hbase']
2016-03-24 17:52:12 [u'Hadoop', u'Apache']
2016-03-24 17:52:10 [u'Flink', u'Hbase']
2016-03-24 17:51:10 [u'Cassandra', u'NoSQL']


C:\insightCode\pgh-challenge-master\insight_testsuite>python ../src/average_degree.py 
./test_pgh/tweet_input/testdata08.txt ./test_pgh/tweet_output/testout08.txt

C:\insightCode\pgh-challenge-master\insight_testsuite>cat ./test_pgh/tweet_output/testout08.txt
1.0
2.0
2.0
2.0
2.0
1.67
2.0
2.0

## [Possible enhancements](README.md#future-enhancements)

4.1  --> per line processing is slower, we could have a configurable parameter for batch size and process set of rows
4.2  --> Nested Dict does not scale linearly. when the inputs records were duplicated to 110,000 records the processing time was 90 seconds.
	    try pandas data frame or any other data structure that allows indexed access by Node/Edge name or by timestamp.



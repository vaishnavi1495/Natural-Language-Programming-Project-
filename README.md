# Semantic Search using NLP features
This is an individual Project.

## PROGRAMMING TOOLS AND LIBRARIES:
•	SOLR (7.5)
•	Python (3.7)
•	WordNet
•	NLTK
•	rake-nltk parser
•	Pysolr (3.7.0)

Sources for Installation of above libraries and tools are mentioned in the report.

Reuter Corpus can be downloaded from nltk_data site or else use from the attached folder.

The SOLR must be installed to run the project successfully.
And from the command prompt run following commands
1. cd the path to bin folder of solr 
   cd C:\Users\bhosa\Desktop\NLP\Project\solr-7.5.0\bin\
2. solr.cmd start

Syntax to create core on SOLR : solr create -c task1
As mentioned below, in the program task1 core is used if you want to use other core 
create it using the above command and edit this server path of SOLR with the core name.  
server = pysolr.Solr('http://localhost:8983/solr/task1/', timeout=100000)

Following program tested successfully on Python 3.7
### How to Run?
1. python DeepSemanticSearch.py
2. It will ask to enter corpus file path. Give the appropriate path of the 
   corpus file. 
   Ex.., C:/Users/bhosa/Desktop/NLP/Project/Reuter/corpus
3. It will take few minutes to exatrct features and add to the SOLR server then
   program will ask for the query. Pass the sentence. 
   Ex.., American Express may sell Shearson 
5. Program will give the output of all top 10 search result and extracted NLP features.  

1) Download Solr from below command
wget http://archive.apache.org/dist/lucene/solr/5.3.1/solr-5.3.1.tgz

2) Unpack $ tar zxf solr-5.x.x.tgz

3) cd solr-5.x.x

4) Create a core with name core: $ bin/solr create -c core
Create a core with name core: $ bin/solr create -c city
Create a core with name core: $ bin/solr create -c university
Create a core with name core: $ bin/solr create -c property

5) git clone https://github.com/AgrimSharma/solr_django.git

6) cd solr_django

7) ./local.sh

8) Add City - http://localhost:8001/solr/city/
Add University - http://localhost:8001/solr/university/
Add Property - http://localhost:8001/solr/property/

9) Search City Vise - http://localhost:8001/solr/search_city/

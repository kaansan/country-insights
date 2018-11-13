# country-insights
* _An API who gives insights about countries._

![Alt Text](country-insights.gif)

# Tech Stack
* Python 3
* Elasticsearch
* Flask
* Pandas

# Installation
    # create your virtualenv and then ...
    $ git clone git@github.com:kaansan/country-insights.git
    $ pip install -r requirements.txt
    
# How to run
 
fire up elasticsearch in a terminal with
    
    $ elasticsearch

with a another terminal type
    
    $ python app.py
    
for testing api endpoints, start server and type
   
    $ python tests.py


# Endpoints

* __*http://localhost:port/country/<country_code>*__
    
        for example, http://localhost:port/country/afg/
        # returns insights about afghanistan

* __*http://localhost:port/country/<country_code>/population/*__
    
        for example, http://localhost:port/country/afg/population/
        # returns population for afghanistan
      
* __*http://localhost:port/country/all/*__
    
        for example, http://localhost:port/country/all/
        # returns every insight for every country
 

# Source
https://data.worldbank.org/
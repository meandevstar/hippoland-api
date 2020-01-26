## Hippoland Product Scraper API

Hippoland Product Scraper API written in Django

### API Endpoints

#### Users

* **/api/users/** (User registration endpoint)
* **/api/users/login/** (User login endpoint)
* **/api/users/logout/** (User logout endpoint)


#### Products

* **/api/products/** (Product create and list endpoint)
* **/api/products/{product-id}/** (Product retrieve, update and destroy endpoint)

### Install 

    pip install -r requirements.txt

### Usage
  - Run API server
    cd scraper
    python3 -B manage.py runserver
  
  - Run scraper script
    scrapy runspider -a page=1,limit=36 scraper/scraper.py

    Options: `page` for crawl start point, `limit` for crawl pagination page size 

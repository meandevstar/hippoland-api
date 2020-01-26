import sys
import re
import time
import scrapy
from scraperapp.wsgi import *
from products.models import Product


class ProductListCrawler(scrapy.Spider):
    name = "product_list_crawler"

    PRODUCTS_SELECTOR = "#products-list div .product-box"
    IMAGE_SELECTOR = ".image-wrapper img::attr(src)"
    URL_SELECTOR = "::attr(href)"
    TITLE_SELECTOR = "span.title::text"
    SKU_SELECTOR = ".attributes-wrapper .sku-label ::text"
    PRICE_SELECTOR = ".price-box .price ::text"
    DESCRIPTION_SELECTOR = "#full-description .text-page ::text"

    def create_desc_callback(self, product_obj):
        """
        Passing already crawled product data to description parser.
        """

        return lambda response: self.parse_desc(response, product_obj)

    # def get_headers(self, url):
    #     return {
    #         "User-Agent":
    #             "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
    #         "Accept": "*/*",
    #         "Accept-Language": "en-US,en;q=0.5",
    #         "Referer": url,
    #         "X-Requested-With": "XMLHttpRequest",
    #         "appVersion": "0.1",
    #         "appOS": "web",
    #         "X-Anonymous-ID": "undefined",
    #     }

    def start_requests(self):
        args = {
            "limit": 36,
            "page": 1
        }
        for pair in sys.argv[2].split(","):
            args[pair.split("=")[0]] = int(pair.split("=")[1])

        print("\n==> Crawler Setting\n", args, "\n\n")

        urls = [
            "https://www.hippoland.net/produkti?limit={}&p={}".format(
                args.get("limit"), args.get("page")
            )
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

    def parse(self, response):
        """
        Scraping product details on product list page.
        """

        product_obj = {}
        url = ""
        sku = ""

        for product in response.css(self.PRODUCTS_SELECTOR):
            url = product.css(self.URL_SELECTOR).get()
            sku = product.css(self.TITLE_SELECTOR).get()

            product_obj = {
                "image_url": product.css(self.IMAGE_SELECTOR).get(),
                "url": url,
                "name": sku,
                "sku": re.sub("[\n SUB:]", "", product.css(self.SKU_SELECTOR).get()),
                "price": float(re.sub("[,&nbsp;\xa0]", "", product.css(self.PRICE_SELECTOR).get()))
            }

            if url is not None:
                time.sleep(2)
                yield response.follow(
                    url,
                    callback=self.create_desc_callback(product_obj),
                )

        # Parsing until pagination finishes.
        next_page = response.css("a.next::attr(href)").get()
        print("\n==> Next Page: ", next_page, "\n\n")
        if next_page is not None:
            yield response.follow(
                next_page,
                callback=self.parse,
            )

    def parse_desc(self, response, product_obj):
        """
        Scraping product description on product detail page.
        """

        description_list = response.css(self.DESCRIPTION_SELECTOR).getall()
        product_obj["description"] = ""

        for description_item in description_list:
            product_obj["description"] += description_item.strip(" ")

        # Find by SKU id and update or create if it does not exists.
        product, created = Product.objects.get_or_create(
            sku=product_obj.get("sku"), defaults=product_obj)

        if not created:
            for attr, value in product_obj.items():
                setattr(product, attr, value)
            product.save()

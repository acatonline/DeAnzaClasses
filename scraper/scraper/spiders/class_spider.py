from datetime import datetime
from pathlib import Path

import scrapy


class ClassSpider(scrapy.Spider):
    name = "get_classes"

    async def start(self):
        urls = [
            "https://www.deanza.edu/schedule/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        self.classes_found = []

    def parse(self, response):
        filename = "debug.txt"
        terms = []
        for class_terms in response.css("#term-select button::attr(value)").getall():
            terms.append(class_terms)
        for term in terms:
            for class_prefix in response.css("#dept-select option::attr(value)").getall():
                if class_prefix:
                    self.classes_found.append(f"https://www.deanza.edu/schedule/listings.html?dept={class_prefix}&t={term}")
                    # yield scrapy.Request(
                    #     url=f"https://www.deanza.edu/schedule/listings.html?dept={class_prefix}&t={term}",
                    #     callback=self.parse_classes,
                    # )
        # Path(filename).write_text(classname)
        # Path("temp.html").write_text(response.text)
        # Path("terms.txt").write_text("\n".join(terms))
        if len(self.classes_found) == 0:
            raise Exception("No classes found")
        
        yield scrapy.Request(
            url=self.classes_found[0],
            callback=self.chained_classes,
            cb_kwargs={
                "linkPosition": 0,
            }
        )

    def chained_classes(self, response, linkPosition):
        print(response.status)
        print(response.url)
        print(datetime.now())
        if linkPosition + 1 < len(self.classes_found):
            yield scrapy.Request(
                url=self.classes_found[linkPosition + 1],
                callback=self.chained_classes,
                cb_kwargs={
                    "linkPosition": linkPosition + 1,
                }
            )
    
    def parse_classes(self, response):
        print(response.status)
        print(response.url)
        print(datetime.now())
        # for class_name in response.css(".course-title::text").getall():
        #     classname += "\n" + class_name
        # Path("classes.txt").write_text(classname)
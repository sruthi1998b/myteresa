import scrapy
from scrapy.http import *
from mytheresa.items import *
h={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
class Mytheresa(scrapy.Spider):
    name='mytheresa'
    start_urls=['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self,response):
        # urls =response.xpath('//div[@class="category-products"]/ul/li/a[@class="product-image"]/@href').extract()
        urls =response.xpath('//a[@class="product-image"]/@href').extract()
        for url in urls:
            yield Request(url,headers=h,callback=self.parsedata,dont_filter=True)
        nxtpage = response.xpath('//li[@class="next"]/a/@href').extract_first('')
        if nxtpage:
            yield Request(nxtpage,headers=h,callback=self.parse,dont_filter=True)
    def parsedata(self,response):
        product_name =response.xpath('//div[@class="product-name"]/span/text()').extract_first('').strip()
        bredcrumb_list=[]
        bredcrumb_=response.xpath('//div[@class="breadcrumbs"]/ul/li//text()').extract()
        for i in bredcrumb_:
            if i.strip():bredcrumb_list.append(i.strip())
        imagelink =response.xpath('//img[@class="gallery-image"]/@src').extract_first('').strip()
        if imagelink:
            imagelink = 'https:'+imagelink
        brand =response.xpath('//div[@class="product-shop"]/div/span/a/text()').extract_first('')
        price =response.xpath('//span[@class="regular-price"]/span/text() | //p[@class="special-price"]/span/text()').extract_first('').strip() 
        product_id =response.xpath('//div[@class="product-sku pa1-rm-tax"]/span/text()').extract_first('').strip().replace("item no.","").replace('\xa0','')
        size_xpath =response.xpath('//ul[@id="product-dropdown-sizes"]/li//text()').extract()
        size_list=[]
        for size in size_xpath:
            if size.strip():
                size_list.append(size.strip())
        desc = ' '.join(' '.join(response.xpath('//p[@class="pa1-rmm product-description"]/parent::div//text()').extract()).strip().split()) 
        image =response.xpath('//div[@class="product-image-gallery"]//img/@data-src').extract()
        otherimagelist=[]
        for img in image:
            img_link = 'https:'+img
            otherimagelist.append(img_link)
        listprice =response.xpath('//p[@class="old-price"]/span/text()').extract_first('') 
        discount=response.xpath('//span[@class="price-reduction-notice"]/text()').extract_first('') 
        item =MytheresaItem()
        item['product_url'] = response.url
        item['breadcrumbs'] =bredcrumb_list
        item['image_url'] =imagelink
        item['brand'] = brand
        item['product_name'] =product_name
        item['listing_price'] = listprice
        item['offer_price'] = price
        item['discount'] = discount
        item['product_id'] = product_id
        item['sizes'] = size_list
        item['description'] = desc
        item['other_images'] = otherimagelist
        yield item
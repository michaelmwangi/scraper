import json
import requests
from parser import Parser


class Scraper:
    username = "Thumb"
    password = "Scraper"
    base_url = "https://yolaw-tokeep-hiring-env.herokuapp.com/"

    def __init__(self, map_url=None):
        """
        Initializes the scrapper
        @param map_url: the url location of the page map
        """
        self.page_map_url = map_url
        self.pages_map = None # a dict of pages to parse when initialized
        
        if map_url:
            self._get_pages_map()
        

    def _get_pages_map(self):
        """
        Initializes the page map and prepares it as a dict for later processing/usage
        This function expects a json page map that is formatted according to the instructions given
        """    
        html = self._fetch_page(self.page_map_url)
        self.pages_map = json.loads(html)
    
    def _fetch_page(self, url):
        """
        makes a get request to the url given and returns a response obj .
        by using requests we dont have to follow 302 codes as the lib does that for us
        """
        
        resp = requests.get(url)
        if resp.status_code != 200:
            if resp.status_code == 401:
                # we need auth
                resp = requests.get(url, auth=(self.username, self.password))
            else:
                raise ScrapingException("Cannot fetch the pages map error code is {}".format(resp.status_code))
        
        return resp.text

    def scrap(self):
        """
        kick start the scraper 
        """
        if not self.pages_map:
            print("Cannot scrap the pages map has not been initialized")
            return 
        
        parser = Parser()
        cur_url = self.base_url
        cur_pg = '0' # the start page key as per instructions    
        keys = list(self.pages_map.keys())
        while keys:
            print ("Move to page {}".format(cur_pg))
            test_query = self.pages_map[cur_pg]['xpath_test_query']
            test_result = self.pages_map[cur_pg]['xpath_test_result']
            nxt_btn_query = self.pages_map[cur_pg]['xpath_button_to_click']
            nxt_pg = self.pages_map[cur_pg]['next_page_expected']

            html = self._fetch_page(cur_url)
            parser.set_html_content(html)
            test_data = parser.xpath_search(test_query)

            if test_data != test_result:
                print("ALERT - Can't move to page {}: page {} link has been tampered with!!".format(nxt_pg, cur_pg))
                break

            keys.remove(cur_pg)
            btn = parser.xpath_search_attr(nxt_btn_query, "href")
            if nxt_pg in keys and btn:                
                cur_pg = nxt_pg
                nxt_url = btn[0]
                cur_url = self.base_url+nxt_url                
            else:
                print("Cannot move on, the next page {} is was not found on the pages map".format(nxt_pg))
                break
        
        

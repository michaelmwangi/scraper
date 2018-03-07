import json
import requests
from Queue import deque
from parser import Parser
from collections import namedtuple

class Scraper:
    username = "Thumb"
    password = "Scraper"
    base_url = "https://yolaw-tokeep-hiring-env.herokuapp.com/"

    def __init__(self, map_url=None, max_loops=1):
        """
        Initializes the scrapper
        @param map_url: the url location of the page map
        @param max_loops: the maximum number of times we should loop on a page
        """
        self.page_map_url = map_url
        self.pages_map = None # a dict of pages to parse when initialized
        self.max_loops = max_loops
        self.visited_pages = dict() # a dict of pages we have vsisted # page_name:visited_times

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

    def _max_loops_reached(self, pagename):
        """
        Checks whether the page identitified by pagename has reached the total number of allowed
        loops
        returns True/False 
        """
        num = self.visited_pages.setdefault(pagename, 0)
        if num >= self.max_loops:
            return True
        return False

    def scrap(self):
        """
        kick start the scraper 
        """
        if not self.pages_map:
            print("Cannot scrap the pages map has not been initialized")
            return 
        
        parser = Parser()
        pages_queue = deque()
        page =  namedtuple('page', 'name url') # structure to hold current page info

        start_pg = page('0', self.base_url)                
        pages_queue.append(start_pg) # insert the first page to kick us off

        # we continue to process new pages as long as the pages queue is not empty
        # and we have valid pages to process
        while pages_queue:
            current_pg = pages_queue.popleft()
            if self._max_loops_reached(current_pg.name):
                print("Cannot proceed with scrapping, maximum loops {} reached on page {}".format(self.max_loops, current_pg.name))
                break

            cur_pg = current_pg.name
            print ("Move to page {}".format(cur_pg))
            test_query = self.pages_map[cur_pg]['xpath_test_query']
            test_result = self.pages_map[cur_pg]['xpath_test_result']
            nxt_btn_query = self.pages_map[cur_pg]['xpath_button_to_click']
            nxt_pg = self.pages_map[cur_pg]['next_page_expected']

            html = self._fetch_page(current_pg.url)
            parser.set_html_content(html)
            test_data = parser.xpath_search(test_query)
                                    
            if test_data != test_result:
                print("ALERT - Can't move to page {}: page {} link has been tampered with!!".format(nxt_pg, cur_pg))
                break

            btn = parser.xpath_search_attr(nxt_btn_query, "href")
            if btn:     
                if btn[0] == '/':
                    nxt_url = self.base_url
                else:    
                    nxt_url = self.base_url + btn[0]
                                
                pg = page(nxt_pg, nxt_url)    
                # queue the next page for scrapping
                pages_queue.append(pg)
            else:
                print("Cannot proceed with the page scrapping, could not find button in page {}".format(cur_pg))
                break
       
        
        

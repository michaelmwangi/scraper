
import sys
import StringIO
import unittest
from parser import Parser
from scraper import Scraper


def load_test_file():
    fname = "sample.html"
    f = open(fname, 'r')
    html_cont = f.read()
    return html_cont.decode('utf-8')

class TestParser(unittest.TestCase):

    def setUp(self):
        self.html = load_test_file()
        self.parser = Parser(self.html)
    
    def test_xpath_search(self):
        xpath_test = '/html/body/ul/li[2]//text()'
        res = self.parser.xpath_search(xpath_test)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], 'link 2 ')

    def test_xpath_search_attr(self):
        xpath_test = '/html/body/a'
        res = self.parser.xpath_search_attr(xpath_test, 'href')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], '/nowhere')
    
    def test_set_html_content(self):
        test_html = "<html><p>testing</p></html>"
        self.parser.set_html_content(test_html)
        res = self.parser.html()
        self.assertEqual(res, test_html)
        self.parser.set_html_content(self.html)



class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper()
        self.scraper.pages_map = {"0":
                                    {
                                    "next_page_expected":"2",
                                    "xpath_button_to_click":"/html/body/a",
                                    "xpath_test_query":"/html/body/p//text()",
                                    "xpath_test_result": "does not exist"
                                    }   
                                }
        self.scraper._fetch_page = self._fetch_page
        
    def _fetch_page(self, url):
        return load_test_file()

    def test_scrap(self):
        tmp_out = StringIO.StringIO()
        old_out = sys.stdout
        sys.stdout = tmp_out
        self.scraper.scrap()
        sys.stdout = old_out
        output = tmp_out.getvalue().strip()
        self.assertIn('Can\'t move to page 2', output)
        
if __name__ == '__main__':
    unittest.main()
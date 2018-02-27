import StringIO
from lxml import html, etree
from scraperexceptions import ScrapingException

# TODO handle encoding eg make sure we are using a standard one eg utf-8

class Parser:
    """
    Parse the html input and also conduct search
    """
    
    # this will help work with broken html
    parser = etree.HTMLParser()

    def __init__(self, html=None):
        """
        initialize the parser 
        """
        if html:
            if isinstance(html, str):
                raise ScrapingException("Cannot initialize parser! expected html content to be a string")
            self._html_txt = html
            self._html_tree = etree.parse(StringIO.StringIO(self._html_txt), parser=self.parser)
        else:
            self._html_txt = None
            self._html_tree = None

    def set_html_content(self, html):
        """
        Sets the html content and also prepares the html_tree obj
        """
        self._html_txt = html
        self._html_tree = etree.parse(StringIO.StringIO(self._html_txt), parser=self.parser)

    def html(self):

        return self._html_txt

    def xpath_search(self, xpath):
        """
        find and return a list of elements that match the xpath
        each element is treated with the base set encoding
        @param xpath: the xpath used
        return list of elements matchin the xpath
        """

        return self._html_tree.xpath(xpath)
    
    def xpath_search_attr(self, xpath, attr):
        """
        finds and returns the attribute value of the element identified by the 
        xpath
        @param xpath: The xpath query
        @param attr: the attribute of the element 
        return list of attribute values 
        """

        elems = self.xpath_search(xpath)
        vals = list()

        for elem in elems:
            vals.append(elem.attrib[attr])

        return vals



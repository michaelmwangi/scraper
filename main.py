from scraper import Scraper


if __name__ == '__main__':
    scraper = Scraper('https://s3-eu-west-1.amazonaws.com/legalstart/thumbscraper_input_tampered.hiring-env.json')
    scraper.scrap()
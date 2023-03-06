import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup


class SicavScraper:
    def __init__(self):
        self.base_url = 'https://www.cnmv.es/Portal/Consultas/'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/110.0.0.0 Safari/537.36',
        }
        self.session = requests.Session()

    def scrape_data(self, id_=18) -> list:
        listings = []
        page_number = 0
        while True:
            url = f'{self.base_url}MostrarListados.aspx?id={id_}&page={page_number}'

            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                logging.info(f'Response status code: {response.status_code}')
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
                logging.error(f'Error occurred while fetching page {page_number}: {e}')
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            current_listings = self.parse_listings(soup)
            listings.extend(current_listings)

            # If this is the last page, break out of the loop
            if page_number == self.find_number_of_pages(soup):
                break

            # Otherwise, increment the page number and continue with the loop
            page_number += 1

        return listings

    # Get the value of the last page
    def find_number_of_pages(self, soup: BeautifulSoup) -> int | None:
        pagination_ul = soup.find('ul', class_='pagination')
        if not pagination_ul:
            return None

        last_page_a = pagination_ul.find_all('a')[-1]
        url_last_page = last_page_a.attrs.get('href')
        if not url_last_page:
            return None

        # Parse the URL
        parsed_url = urlparse(url_last_page)

        # Extract query parameters from the url
        query_params = parse_qs(parsed_url.query)
        page_param = query_params.get('page')
        if not page_param or not page_param[0].isdigit():
            return None

        last_page = int(page_param[0])
        return last_page

    def parse_listings(self, soup: BeautifulSoup) -> list:
        listings = []
        ul_listings = soup.find('ul', id='listaElementosPrimernivel')
        a_listings = ul_listings.find_all('a')
        for a_listing in a_listings:
            url_details_part = a_listing.attrs.get('href')
            listing_details_soup = self.get_listing_details(url_details_part)
            listing_item = {}

            try:
                registry_number = listing_details_soup.find('td', {'data-th': 'Nº Registro oficial'}).text.strip()
                listing_item['registry_number'] = int(registry_number)
            except:
                pass

            try:
                registry_date = listing_details_soup.find('td', {'data-th': 'Fecha registro oficial'}).text.strip()
                date_object = datetime.strptime(registry_date, '%d/%m/%Y')
                listing_item['registry_date'] = datetime.strftime(date_object, '%Y-%m-%d')
            except:
                pass

            try:
                address = listing_details_soup.find('td', {'data-th': 'Domicilio'}).text.strip()
                listing_item['address'] = address
            except:
                pass

            try:
                initial_share_capital = listing_details_soup.find('td',
                                                                  {'data-th': 'Capital social inicial'}).text.strip()
                initial_share_capital = initial_share_capital.replace('.', '').replace(',', '.')
                listing_item['initial_share_capital'] = float(initial_share_capital)
            except:
                pass

            try:
                maximum_statutory_capital = listing_details_soup.find('td', {
                    'data-th': 'Capital máximo estatutario'}).text.strip()
                maximum_statutory_capital = maximum_statutory_capital.replace('.', '').replace(',', '.')
                listing_item['maximum_statutory_capital'] = float(maximum_statutory_capital)
            except:
                pass

            try:
                isin = listing_details_soup.find('td', {'data-th': 'ISIN'}).text.strip()
                listing_item['isin'] = isin
            except:
                pass

            try:
                date_latest_brochure = listing_details_soup.find('td', {'data-th': 'Fecha último folleto'}).text.strip()
                date_object = datetime.strptime(date_latest_brochure, '%d/%m/%Y')
                listing_item['date_latest_brochure'] = datetime.strftime(date_object, '%Y-%m-%d')
            except:
                pass

            listing_item['name'] = a_listing.attrs.get('title')
            listings.append(listing_item)

        return listings

    def get_listing_details(self, url_details_part: str) -> BeautifulSoup | None:

        url_details = f'{self.base_url}{url_details_part}'

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                             '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                   'Referer': 'https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18',
                   }

        try:
            res_listing_details = self.session.get(url_details, headers=headers)
            res_listing_details.raise_for_status()  # Raise an exception for a non-200 status code
            logging.info(f'Listings details page response: {res_listing_details.status_code}')
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            logging.error('Failed to get listing details... getting new session')
            self.session = requests.Session()
            res_listing_details = self.session.get(url_details, headers=headers)

        soup_details = BeautifulSoup(res_listing_details.text, 'html.parser')

        return soup_details

from bs4 import BeautifulSoup
import requests


class WebScraper:
    def __init__(self, website: str = "https://marknadssok.fi.se") -> None:
        self.website = website

    def _load_data_list_from_rows(self, content_rows, data_list):
        """
        Extracts information from HTML elements in each row and adds it to the data_list.

        Args:
            content_rows (list): List of HTML row elements to extract data from.
            data_list (list): The list where extracted data is appended as dictionaries.
        """
        for row in content_rows:  # iterate through each row in the content body
            if row is not content_rows[0]:  # skip the header row
                cols = row.findAll("td")

                # extract data from each cell in the row
                date = cols[0].text
                emitter = cols[1].text
                name = cols[2].text
                position = cols[3].text
                related = cols[4].text
                character = cols[5].text
                instrument_name = cols[6].text
                instrument_type = cols[7].text
                isbn = cols[8].text
                transaction_date = cols[9].text
                volume = cols[10].text
                volume_unit = cols[11].text
                price = cols[12].text
                currency = cols[13].text
                statue = cols[14].text
                details = (
                    self.website + cols[15].a["href"]
                )  # construct the full URL for detailed information

                # append the extracted data as a dictionary to data_lis
                data_list.append(
                    {
                        "date": date,
                        "emitter": emitter,
                        "name": name,
                        "position": position,
                        "related": related,
                        "character": character,
                        "instrument name": instrument_name,
                        "instrument type": instrument_type,
                        "isbn": isbn,
                        "transaction date": transaction_date,
                        "volume": volume,
                        "volume unit": volume_unit,
                        "price": price,
                        "currency": currency,
                        "statue": statue,
                        "details": details,
                    }
                )

    def _get_all_tr_elements_from_website(self, company: str) -> list[str]:
        page_number = 1
        URL = f"{self.website}/Publiceringsklient/sv-SE/Search/Search?Utgivare={company}&Page={page_number}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        content_rows = soup.findAll("tr")
        return content_rows

    def fetch_all_insider_data(self, company: str) -> list[any]:
        data_list = []
        content_rows = self._get_all_tr_elements_from_website(company=company)
        self._load_data_list_from_rows(data_list=data_list, content_rows=content_rows)
        return data_list

    def fetch_latest_insider_data(self, company: str) -> None:
        pass


if __name__ == "__main__":
    web_scraper = WebScraper()
    data_list = web_scraper.fetch_all_insider_data("nibe")
    print(data_list)  # result

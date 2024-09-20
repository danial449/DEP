from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""

    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None


@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    # def save_to_excel(self, filename):
    #     """saves pandas dataframe to excel (xlsx) file

    #     Args:
    #         filename (str): filename
    #     """

    #     if not os.path.exists(self.save_at):
    #         os.makedirs(self.save_at)
    #     self.dataframe().to_excel(f"output/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

def main():
    
    ########
    # input 
    ########
    
    # read search from arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    if args.search:
        search_list = [args.search]
        
    if args.total:
        total = args.total
    else:
        # if no total is passed, we set the value to random big number
        total = 1_000_000

    if not args.search:
        search_list = []
        # read search from input.txt file
        input_file_name = 'input.txt'
        # Get the absolute path of the file in the current working directory
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        # Check if the file exists
        if os.path.exists(input_file_path):
        # Open the file in read mode
            with open(input_file_path, 'r') as file:
            # Read all lines into a list
                search_list = file.readlines()
                
        if len(search_list) == 0:
            print('Error occured: You must either pass the -s search argument, or add searches to input.txt')
            sys.exit()
        
    ###########
    # scraping
    ###########
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(5000)
        
        for search_for_index, search_for in enumerate(search_list):
            print(f"-----\n{search_for_index} - {search_for}".strip())

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(3000)

            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            # scrolling
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration
            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)

                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    >= total
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                else:
                    # logic to break from loop to not run infinitely
                    # in case arrived at all available listings
                    if (
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        == previously_counted
                    ):
                        listings = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).all()
                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        print(
                            f"Currently Scraped: ",
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count(),
                        )

            business_list = BusinessList()

            # Counter for scraped businesses
            scraped_count = 0

            # scraping
            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(5000)
            
                    # Update this XPath with the correct one you find
                    name_xpath = '//h1[contains(@class, "DUwDvf")]'
                    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                    website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                    phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                    
                    business = Business()
                    
                    name_locator = page.locator(name_xpath)
                    if name_locator.count() > 0:
                        business.name = name_locator.first.inner_text() or ""
                    else:
                        business.name = ""
                    
                    address_locator = page.locator(address_xpath)
                    if address_locator.count() > 0:
                        business.address = address_locator.first.inner_text() or ""
                    else:
                        business.address = ""
                    
                    website_locator = page.locator(website_xpath)
                    if website_locator.count() > 0:
                        business.website = website_locator.first.inner_text() or ""
                    else:
                        business.website = ""
                    
                    phone_number_locator = page.locator(phone_number_xpath)
                    if phone_number_locator.count() > 0:
                        business.phone_number = phone_number_locator.first.inner_text() or ""
                    else:
                        business.phone_number = ""
            
                    business_list.business_list.append(business)

                     # Increment and print the scraped count
                    scraped_count += 1
                    print(f"Scraped {scraped_count}/{len(listings)}: {business.name}")

                except Exception as e:
                    print(f'Error occurred: {e}')

            
            #########
            # output
            #########
            # business_list.save_to_excel(f"google_maps_data_{search_for.strip()}".replace(' ', '_'))
            business_list.save_to_csv(f"google_maps_data_{search_for.strip()}".replace(' ', '_'))

        browser.close()


if __name__ == "__main__":
    main()
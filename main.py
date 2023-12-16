import sys
import json
from datetime import datetime, timedelta

"""_method_

    filter_by_date(date_str, offers)
        It takes check-in date string from the MOCK_DATA JSON file and the offers list from the input JSON file. 
        Offer needs to be valid till check-in date + 5 days. 
        It returns the filter offers list.
    
    filter_by_category(offers):
        It takes offer list as an argument and only select offers with category that is Restaurant, Retail or Activity
            Restaurant: 1 
            Retail: 2
            Hotel: 3
            Activity: 4
        If an offer is available in multiple merchants, only select the closest merchant.
        If there are multiple offers in the same category give priority to the closest merchant offer.
        
        It returns a filtered offers list
        
    filter_by_distance(offers):
        It takes offer list as an argument. 
        If there are multiple offers with different categories, select the closest merchant offers when selecting 2 offers
        The method returns a list of the 2 closest offers. 
"""

"""_class_
        Filter class provide the IO handling using exception handler to read and write a JSON file.
        The result is written in the output.json file
"""


def parse_time(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt


def filter_by_date(date_str, offers):
    date = parse_time(date_str)

    selected_offers_for_date = []

    for offer in offers:
        valid_to = parse_time(offer["valid_to"])
        difference = valid_to - date

        # If the difference is less than 5 days, add the offer to the list of selected offers for this date
        if difference <= timedelta(days=5) and difference >= timedelta(days=0):
            selected_offers_for_date.append(offer)
    return selected_offers_for_date


def filter_by_distance(offers):
    offers.sort(key=lambda offer: offer["merchants"][0]["distance"])

    nearest_offers = offers[:2]
    return nearest_offers


def filter_by_category(offers):
    # Define the category IDs for Restaurant, Retail, and Activity
    category_ids = [1, 2, 4]

    selected_offers_list = []

    for offer in offers:
        if offer["category"] in category_ids:
            # Sort the merchants by distance and select the nearest one
            nearest_merchant = min(
                offer["merchants"], key=lambda merchant: merchant["distance"]
            )

            # Create a new offer dictionary that includes only the nearest merchant
            new_offer = {**offer, "merchants": [nearest_merchant]}

            # If the category is not in the selected_offers_list or if the new offer's distance is less than the current offer's distance
            if (
                offer["category"] not in [o["category"] for o in selected_offers_list]
                or nearest_merchant["distance"]
                < min(
                    [
                        o
                        for o in selected_offers_list
                        if o["category"] == offer["category"]
                    ],
                    key=lambda o: o["merchants"][0]["distance"],
                )["merchants"][0]["distance"]
            ):
                # Remove the existing offer for this category if it exists
                selected_offers_list = [
                    o
                    for o in selected_offers_list
                    if o["category"] != offer["category"]
                ]
                selected_offers_list.append(new_offer)
    return selected_offers_list


class Filter:
    def __init__(self, dates_file, offer_file):
        try:
            with open(dates_file, "r") as f:
                dates = json.load(f)
            self.dates = [date["date"] for date in dates]
        except ValueError:
            print(
                f"Error: One or more dates in '{dates_file}' are not in the 'YYYY-MM-DD' format."
            )
            self.dates = None
        except FileNotFoundError:
            print(f"Error: The file '{dates_file}' does not exist.")
            self.dates = None

        try:
            with open(offer_file, "r") as f:
                data = json.load(f)
                self.offers = data["offers"]
        except FileNotFoundError:
            print(f"Error: The file '{offer_file}' does not exist.")
            self.offers = None

    def filter_offers(self):
        selected_offers = {}
        # Iterate over the dates
        for self.date in self.dates:
            date_filter = filter_by_date(self.date, self.offers)
            category_filter = filter_by_category(date_filter)
            distance_filter = filter_by_distance(category_filter)

            selected_offers[self.date] = {"offers": distance_filter}
        with open("output.json", "w") as f:
            json.dump(selected_offers, f, indent=4)


if __name__ == "__main__":
    solution = Filter(sys.argv[1], sys.argv[2])
    selected_offers = solution.filter_offers()
    print ("The selected offers are saved in the output.json file. Look for it!")

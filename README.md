## Filter Travel Offer

## Summary
Part of Ascenda travel platform is to find nearby offers for our customers. When a user books a hotel using Ascenda travel platform, we find nearby offers around the hotel customer booked and send those offers in the booking confirmation email. So when the customer stays at the hotel, he can enjoy nearby offers from Restaurants, Retail stores & Tourist Activity places.

**The program takes Check-in Dates and input JSON files and returns the near-by suitable Offers for the customers to improve their experiences while enjoying travel services.**

The **input** includes:

 - **Check-in date JSON file**: Instead of providing a specific check-in
   date, I believe providing a JSON file including the check-in dates of    customers is much more convenient and expandable. Due to the fact   that the check-in date could be provided in SQL datetime (***YYYY-MM-DD   HH:MM:SS***), I made a MOCK_DATA.json to provide basic example on how check-in dates are arranged. For further development, check-in dates can be associated with the customers based on when the customers make the payment (electronic or non-electronic). These attributes need to be precise to store in the database and each customer is 1-on-1 mapping in the dictionary.
   
 - **Offers input JSON file:**  this API returns us a JSON response including offer details & merchant details. Merchants giving these offers are categorized by the external partner.

    
The **output.json** includes:

 - The **offers** for each check-in dates (in hour, minute and second division). Therefore, the company can automatically filter and send offers as soon as the customers finish their reservation via emails, phone number, etc.

## Step-by-step

1.  **Load Check-in Date JSON**
2.  **Load Input JSON**
3.  **Filter Offers**
5.  **Save to Output JSON**


## Installation

1. Download the source code or clone the repository to your local machine.
2. Install Python 3 and Dependencies such as ***datetime*** and ***sys*** (if not installed by default)
3. After installing the dependencies, run the application with the following command:

   `py .\main.py .\MOCK_DATA.json .\input.json`

   You can replace **MOCK_DATA.json** with your **Check-in Dates** JSON file and **input.json** with your **Offers List** JSON file


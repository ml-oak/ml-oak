import requests
import csv

class GooglePlace:
    def __init__(self, api_key, place_id, name):
        self.api_key = api_key
        self.place_id = place_id
        self.name = name
        self.details = self._get_place_details()

    def _get_place_details(self):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        response = requests.get(endpoint_url, params={"placeid": self.place_id, "key": self.api_key})
        data = response.json()
        return data.get("result", {})

    def get_phone_number(self):
        return self.details.get("formatted_phone_number", "N/A")

    def get_email(self):
        return self.details.get("website", "N/A")

def scrape_google_maps(api_key, location, keyword):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    response = requests.get(endpoint_url, params={"query": f"{keyword} in {location}", "key": api_key})
    data = response.json()

    # Write results to a CSV file
    with open("google_places.csv", "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Place ID", "Phone Number", "Email"])

        # Get phone number and email for each place and write to CSV directly
        for place in data["results"]:
            name = place["name"]
            place_id = place["place_id"]
            google_place = GooglePlace(api_key, place_id, name)
            phone_number = google_place.get_phone_number()
            email = google_place.get_email()

            csv_writer.writerow([name, place_id, phone_number, email])

    print("Results saved to google_places.csv.")
# Example usage
if __name__ == "__main__":
    api_key = ""
    location = "San Francisco, CA"  # Specify the location you want to search
    keyword = "autoshops"     # Specify the type of businesses you want to search
    
    scrape_google_maps(api_key, location, keyword)

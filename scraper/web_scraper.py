import requests
from bs4 import BeautifulSoup
import json
import string

class NationalDays:

    def __init__(self):
        self.days = {}
        self.base = "https://nationaldaycalendar.com/"

    def get_month(self, month):
        if month not in self.days:
            self.days[month] = {}

        URL = self.base + month + "/"

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    def add_days(self, soup, month):
        print("Scraping " + month + "...")
        results = soup.find_all('a')

        for item in results:
            word = str(item)
            temp = word.strip()
            last = len(temp) - 1

            # Checks to only get dates we want
            check_indicator = temp[last - 6] + temp[last - 5] + temp[last - 4] + temp[last - 3] + temp[last - 2] + temp[last - 1]+ temp[last]
            double_check = temp[last - 12] + temp[last - 11] + temp[last - 10] + temp[last - 9] + temp[last - 8] + temp[last - 7] + temp[last - 6] + temp[last - 5] + temp[last - 4]
            
            if check_indicator == "Day</a>" and double_check != "ter A Day":
                day, date = self.get_day(temp)
                if day == False:
                    continue
                else:
                    if date not in self.days[month]:
                        self.days[month][date] = []
                    # Add the data
                    self.days[month][date].append(day)
        
        print("Done with " + month + "!\n")

    def get_day(self, string):
        ptr = 41
        tmp = ""
        while string[ptr] !="/":
            tmp = tmp + string[ptr]
            ptr = ptr + 1

        words = tmp.split('-') 

        if words[len(words) - 1] == "day" or words[0] != "national":
            return (False, False)

        # Get the holiday name
        ptr = 0
        day = words[ptr]
        while words[ptr] != "day":
            if ptr == len(words) - 1:
                return (False, False)
            ptr = ptr + 1
            day = day + " " + words[ptr]

        # Get the date of the corresponding holiday
        date = words[ptr + 1]
        for i in range(ptr + 2, len(words)):
            date = date + " " + words[i]
        
        return(day, date)

    def main(self, months):
        for month in months:
            soup = self.get_month(month)
            self.add_days(soup, month)
        
        # Dump to JSON
        with open('data.json', 'w') as fp:
            json.dump(self.days, fp, indent=4)
        
if __name__ == "__main__":
    scraper = NationalDays()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    scraper.main(months)
import requests
from bs4 import BeautifulSoup
import json
import string

class National_Days:

    def __init__(self):
        self.days = {}
        self.baseURL = "https://nationaldaycalendar.com/"

    def get_month(self, month):
        if month not in self.days:
            self.days[month] = {}

        URL = self.baseURL + month + "/"

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    def add_days(self, soup, month):
        results = soup.find_all('a')

        for item in results:
            word = str(item)
            temp = word.strip()
            last = len(temp) - 1
            check_indicator = temp[last - 6] + temp[last - 5] + temp[last - 4] + temp[last - 3] + temp[last - 2] + temp[last - 1]+ temp[last]
            if check_indicator == "Day</a>":
                day, first = self.get_day(temp, last)
                if day == "Register A Day":
                    continue
                else:
                    date = self.get_date(temp, first)
                    if date not in self.days[month]:
                        self.days[month][date] = []
                    self.days[month][date].append(day)

    def get_day(self, string, last):
        ptr = last - 6
        tmp = ""
        while tmp != ">":
            tmp = string[ptr - 1]
            ptr = ptr - 1

        day = ""
        for i in range(ptr + 1, last - 3):
            if string[i] == "\u2019":
                day = day + "'"
            else:
                day = day + string[i]
        
        return (day, ptr)


    def get_date(self, string, first):
        print(string)
        print(string[first - 3] + string[first - 2] + string[first - 1] + string[first])
        ptr = first
        tmp = string[ptr]
        while not tmp.isnumeric():
            print(tmp)
            tmp = string[ptr - 1]
            ptr = ptr - 1

        date = tmp

        if string[ptr].isnumeric():
            date = string[ptr] + tmp
        # while tmp != "\"":
        #     date = date + tmp
        #     tmp = string[ptr + 1]
        #     ptr = ptr + 1
            # day = day + string[i]

        
        return date

    def main(self, months):
        for month in months:
            soup = self.get_month(month)
            self.add_days(soup, month)
        
        with open('data.json', 'w') as fp:
            json.dump(self.days, fp, indent=4)
        


if __name__ == "__main__":
    scraper = National_Days()
    months = ["January"]
    scraper.main(months)

# # URL = "https://nationaldaycalendar.com/january/"
# # page = requests.get(URL)

# # soup = BeautifulSoup(page.content, "html.parser")

# # results = soup.find_all('a')

# # print(len(results))

# days = []

# for item in results:
#     word = str(item)
#     temp = word.strip()
#     last = len(temp) - 1
#     check_indicator = temp[last - 6] + temp[last - 5] + temp[last - 4] + temp[last - 3] + temp[last - 2] + temp[last - 1]+ temp[last]
#     if check_indicator == "Day</a>":
#         print(word)

#         ptr = last - 6
#         tmp = ""
#         while tmp != ">":
#             tmp = temp[ptr - 1]
#             ptr = ptr - 1

#         day = ""
#         for i in range(ptr + 1, last - 3):
#             day = day + temp[i]
        
#         days.append(day)
        

#     # else:
#     #     results.remove(item)

# print(days)
#     # if last > 7:
#     #     print(temp[last - 6] + temp[last - 5] + temp[last - 4] + temp[last - 3] + temp[last - 2] + temp[last - 1]+ temp[last])
#     # print("\n\n\n")

# # print(len(list(soup.children)))

# # results = soup.a

# # print(results)

# # results = soup.find(id="ff-main-container")

# # print(results.prettify())

# # for item in results:
#     # print(item)

# # main_content = results.find_all("div", class_="ndc-text-january-1---10-national-days")

# # for item in main_content:
# #     print(item)

# # job_elements = main_content.find_all("div", class_="ndc-text-january-1---10-national-days")

# print("\n\n BREAK \n\n")

# # print(main_content.a)

# # for ele in main_content:
# #     # day = ele.find("a", class_="day")
# #     # print(day)
# #     print(ele, end="\n"*2)

# # test = main_content.find("li", class_="title")

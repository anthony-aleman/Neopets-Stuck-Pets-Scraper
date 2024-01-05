from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from datetime import datetime
import random
import asyncio
import httpx
from tkinter import *

wait_times = [1, 3, 5, 8, 10, 12, 13, 14, 15]



'''
What I want to do:

- Use GUI to select which pets to search for
  - Allow user to select a list of pets to search for
- Run scraper asynchronously as to scrape multiple pages at once
- Give users the choice to store results in a csv, txt file or a json file

'''

neopets_list = [
    "nimmo", "scorchio","jubjub","grarrl",
    "skeith","korbat","lenny","wocky",
    "bruce", "kiko","kau","usul",
    "aisha","chia","eyrie","tuskaninny",
    "flotsam","jetsam","kacheek","uni","buzz","lupe",
    "elephante","gelert","mynci","kyrii",
    "peophin","quiggle","shoyru","acara",
    "zafara","blumaroo","techo","moehog",
    "poogle", "kougra", "grundo", "koi",
    "meerca", "chomby", "pteri", "krawk",
    "tonu", "draik", "lxi", "yurble",
    "ruki", "bori", "hissi", "lutari",
    "xweetok", "ogrin", "gnorbu", "vandagyre",
]

jub_jub = ["jubjub"]

test_list = [
    "nimmo",
    "draik", "ixi", "yurbie",
]

results_list = []

test_results = []

def wait():
    global wait_times
    time.sleep(random.choice(wait_times))
    

def pet_loop(pet_list):
    for pet in pet_list:
        # Wait random amount of seconds before initializing search for pet
        wait()
        for page in range(1,3):     
            # Capture results from page 1 -> page 6 of pet and store in global results list
            print(f"Capture page for pet[{pet}] at page[{page}]")
            capture_page(page_number=page, pet=pet)
        

def capture_page(page_number=1, pet="nimmo"):
    """
    capture_page() returns a list of Dictionaries holding the "name", "color", "species", "stuck_pets_link", 
    """
    
    global results_list
    try:
        # Wait for another random amount of seconds before request
        wait()
                    
        print(f"Results for pet: {pet}, page: {page_number} ")
        # Capture response of Stuck pet page 
        page_res = requests.get(f"https://www.stuckpets.com/neopets/{pet}/page/{page_number}",timeout=1)
        
        # Determine whether page returns anything
        if page_res:
            
            # Use BS4 to find 
            soup = BeautifulSoup(
                                page_res.content, 'html.parser'
                            )
            
            for row in soup.find_all("tr",
                            attrs={
                                "class": "pet-tr",
                            }):
                
                
                name = row.td.contents[0]["title"].split(" ", 3)[0]
                color = row.td.contents[0]["title"].split(" ", 3)[2]
                species = row.td.contents[0]["title"].split(" ", 3)[3]
                link = row.a["href"]
                        # Store result as 'res' Dict
                res = {
                    "name": name,
                    "color": color,
                    "species":species,
                    "link": link,
                }
                print("Link: ",row.a["href"])
                print("name: ", row.td.contents[0]["title"].split(" ", 3)[0])
                print("color: ", row.td.contents[0]["title"].split(" ", 3)[2])
                print("species", row.td.contents[0]["title"].split(" ", 3)[3])
                
                if res:
                    results_list.append(res)
                else:
                    print("Results are empty")
        else:
            return (f"Page Result Returned Nothing on pet [{pet}] page number[{page_number}]")    
    except ConnectionError as e:
        print(f"There was a network problem at pet[{pet}] page number[{page_number}]: ", e)
    except TimeoutError as e:
        print("There was a Timeout: ", e)
    


def capture_pages(start_page=1, end_page=6, pet="nimmo"):
    # Declare use of global results list to hold Dict 'res'
    global results_list, wait_times
    
    for i in range(start_page, end_page):
            try:
                # Wait for another random amount of seconds before request
                wait()
                
                print(f"Capturing pet: {pet}, page: {i} ")
                # Capture response of Stuck pet page 
                page_res = requests.get(f"https://www.stuckpets.com/neopets/{pet}/page/{i}",timeout=1)
                
                # If Page Result is valid
                if page_res:
                    soup = BeautifulSoup(
                                page_res.content, 'html.parser'
                            )
                    
                    # Find each table row with class="pet-tr"
                    for row in soup.find_all("tr",
                            attrs={
                                "class": "pet-tr",
                            }):
                        
                        # Split the text to capture each attribute
                        name = row.td.contents[0]["title"].split(" ", 3)[0]
                        color = row.td.contents[0]["title"].split(" ", 3)[2]
                        species = row.td.contents[0]["title"].split(" ", 3)[3]
                        link = row.a["href"]
                        # Store result as 'res' Dict
                        res = {
                            "name": name,
                            "color": color,
                            "species":species,
                            "link": link,
                        }
                        print(res)
                        
                        # If result is valid append to the global result list
                        if res:
                            results_list.append(res)
                        else:
                            print("Error reading Name/Color/Species")
                            continue
                        
                    else:
                        print("Response returned nothing")
                        continue
            except TypeError as e:
                print("Type Error occured: ", e)
                continue
            except (requests.exceptions.InvalidURL) as e:
                print("The URL provided was invalid: ", e);
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                print("A connection error or timeout occurred:", e)
            except requests.exceptions.HTTPError as e:
                print("HTTP Error occured: ", e)
            except requests.exceptions.RequestException as e:
                print("Error occured: ", e)
                
                
def create_time_stamped_df():
    global results_list
    # Create String to add to end of neopets filename
    date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    
    # Final Step create a csv from the results list
    df = pd.DataFrame.from_dict(results_list)
    df.to_csv(f"neopets_{date}.csv")
    
def test_page_loop():
    for pet in test_list:
        # Wait random amount of seconds before initializing search for pet
        wait()
        for page in range(1,3):     
            # Capture results from page 1 -> page 6 of pet and store in global results list
            print(f"Capture page for pet[{pet}] at page[{page}]")
            capture_page(page_number=page, pet=pet)


def main_loop():
    """
    Loop through every pet and every page scraping the:
    -Name
    -Color
    -Species
    """
    pet_loop(pet_list=neopets_list)
    
    """
    Store Information inside DataFrame w/TimeStamped Filename CSV
    neopets_year_month_day_hour_minute_second.csv
    """
    create_time_stamped_df()
                        
root.mainloop()                
main_loop()


"""
NEXT GOAL:
Find pets with names that contain
    -solely letters, 
    -no numbers, 
    -inital character capitalized, 
    -Total Characters <= 8
"""
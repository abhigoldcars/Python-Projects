from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Setting up session
s = requests.session()  


films = []

# Lists contaiting web scraped data
names = []
ratings = []
genres = []

# Define path where your films are present 

path = input("Enter the path where your films are: ")

# Films with extensions
filmswe = os.listdir(path)

for film in filmswe:
    # Append into my films list (without extensions)
    films.append(os.path.splitext(film)[0])
    

for line in films:
    
    title = line.lower()
    
    query = "+".join(title.split()) 
    URL = "https://www.imdb.com/search/title/?title=" + query
    print(URL)
    # print(release)
    try: 
        response = s.get(URL)

        
        content = response.content

        # print(response.status_code)

        soup = BeautifulSoup(response.content, features="html.parser") 
        #searching all films containers found
        containers = soup.find_all("div", class_="lister-item-content")
        for result in containers:
            name1 = result.h3.a.text
            name = result.h3.a.text.lower()

            
            if title in name:
                #scraping rating
                rating = result.find("div",class_="inline-block ratings-imdb-rating")["data-value"]
                #scraping genre
                genre = result.p.find("span", class_="genre")
                genre = genre.contents[0]

                #appending name, rating and genre to individual lists
                names.append(name1)
                ratings.append(rating)
                genres.append(genre)
                


    except Exception:
        print("Try again with valid combination of tile and release year")

#storing in pandas dataframe
df = pd.DataFrame({'Film Name':names,'Rating':ratings,'Genre':genres}) 

#making csv using pandas
df.to_csv('film_ratings.csv', index=False, encoding='utf-8')

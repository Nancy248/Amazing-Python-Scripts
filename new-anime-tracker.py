import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse as parse
import re
import argparse

def get_anime_details(anime_name):
    anime_name = (" ".join(anime_name.split())).title().replace(" ", "-")
    search_url = f"https://www.anime-planet.com/anime/{anime_name}"

    try:
        source_code = requests.get(search_url)
        source_code.raise_for_status()  # Check for HTTP errors
        content = source_code.content
        soup = BeautifulSoup(content, features="html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error accessing the website: {e}")
        return None

def extract_details(soup):
    try:
        info = soup.find('div', {'class': 'pure-1 md-3-5'})
        description = info.find('p').getText() if info else "Description not found"

        total_episodes = soup.find('div', {'class': 'pure-1 md-1-5'})
        episode_count = re.sub("[^0-9]", "", total_episodes.find('span').getText()) if total_episodes else "N/A"

        active_years = soup.find('span', {'class': 'iconYear'})
        years_active = active_years.getText() if active_years else "N/A"

        rating = soup.find('div', {'class': 'avgRating'})
        average_rating = rating.find('span').getText() if rating else "N/A"

        tags = soup.find('div', {'class': 'tags'})
        tag_list = [tag.getText() for tag in tags.find('ul').find_all('li')] if tags else []

        return {
            "description": description,
            "episode_count": episode_count,
            "years_active": years_active,
            "average_rating": average_rating,
            "tags": tag_list
        }
    except AttributeError:
        print("Error extracting anime details.")
        return None

def main():
    try:
        anime_name = input("Enter the name of the anime: ")
        anime_soup = get_anime_details(anime_name)

        if anime_soup:
            anime_details = extract_details(anime_soup)

            if anime_details:
                print("\nAbout the Anime:\n", "\t\t", anime_details["description"], "\n")
                print("Total number of episodes:\t", anime_details["episode_count"])
                print("Years Active (From-To):\t", anime_details["years_active"])
                print("Rating:", anime_details["average_rating"])

                if anime_details["tags"]:
                    print("\nTags:\n")
                    for tag in anime_details["tags"]:
                        print(tag)
            else:
                print("Anime details not found.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()

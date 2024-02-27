import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import logging
from fake_useragent import UserAgent
import streamlit as st

logging.basicConfig(filename='scraper.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class LinkedInScraper:
    def __init__(self):
        self.scraped_profiles = []
        self.user_agent = UserAgent()
        self.session = requests.Session()

    def login_to_naukri(self, username, password):
        try:
            login_url = "https://www.naukri.com/recruit/login"
            headers = {'User-Agent': self.user_agent.random}
            login_data = {
                'username': username,
                'password': password
            }
            response = self.session.post(login_url, data=login_data, headers=headers)
            response.raise_for_status()
            
            if 'session_cookie_name' in response.cookies:
                st.success("Login successful.")
                return True
            else:
                st.error("Login failed. Please check your credentials.")
                return False
        except Exception as e:
            logging.error(f"An error occurred during login: {e}")
            st.error("An error occurred during login.")
            return False

    def scrape_profile_info(self, profile_url):
        try:
            headers = {'User-Agent': self.user_agent.random}
            response = self.session.get(profile_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
           
        except Exception as e:
            logging.error(f"An error occurred while scraping {profile_url}: {e}")
            return None

    def scrape_profiles(self, urls):
        for url in urls:
            profile_info = self.scrape_profile_info(url)
            if profile_info:
                self.scraped_profiles.append(profile_info)
        return self.scraped_profiles

    def download_csv(self):
        if not self.scraped_profiles:
            st.error("No data to download.")
            return
        try:
            file_path = st.text_input("Enter file path to save CSV:", "")
            if file_path:
                pd.DataFrame(self.scraped_profiles).to_csv(file_path, index=False)
                st.success("CSV file downloaded successfully.")
        except Exception as e:
            logging.error(f"Error downloading CSV file: {e}")
            st.error("Error downloading CSV file.")

def main():
    scraper = LinkedInScraper()

    st.title("Naukri Profile Scraper")

    urls_text = st.text_area("Enter Profile URLs (one per line):", height=200)
    urls = urls_text.split("\n") if urls_text else []

 

    if st.button("Download CSV"):
        scraper.download_csv()

if __name__ == "__main__":
    main()

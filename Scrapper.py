import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

csv_file_path = 'Dataset.csv'
df = pd.read_csv(csv_file_path)


output_csv_path = r'data.csv'


with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    
    csv_writer = csv.writer(csvfile)

   
    csv_writer.writerow(['Title', 'Content', 'Author', 'URL'])

    existing_urls = set()

    for index, row in df.iterrows():
        website_link = row[df.columns[0]]

        try:
            response = requests.get(website_link)
            soup = BeautifulSoup(response.text, 'html.parser')

          
            title_element = soup.find('h1', class_=['headline', 'native_story_title', 'artTitle font_faus', 'HNMDR', 'title', 'story-heading headline'])
            content_elements = soup.find_all('div', class_=['mainArea', 'storycontent', 'artText medium', '_s30J clearfix  ', 'artText', 'flt videoDescCont', 'story-with-main-sec', 'story_details'])
            author_element = soup.find('div', class_='author_name')

           
            if title_element and content_elements:
                title = title_element.text.strip()
                main_area = '\n'.join([paragraph.text.strip() for paragraph in content_elements])
                author = author_element.text.strip() if author_element else None

                
                if website_link not in existing_urls:
                   
                    csv_writer.writerow([title, main_area, author, website_link])
                    existing_urls.add(website_link)

            else:
                print(f"Error: Could not find title or content elements on {website_link}")

        except Exception as e:
            print(f"Error scraping {website_link}: {e}")

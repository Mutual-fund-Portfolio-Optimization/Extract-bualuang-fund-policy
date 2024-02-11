from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_a(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('a')
    img_sources = [img.get('href') for img in img_tags]
    return list(set(img_sources))


def extract_content(urls):
    # DataFrame to store the extracted data
    df = pd.DataFrame(columns=["name", "policy"])
    
    # Selenium WebDriver setup
    chrome_options = Options()
    edge_options = webdriver.EdgeOptions()
    # Uncomment the next line if you prefer Chrome to run headless
    # chrome_options.add_argument("--headless")
    service = Service(executable_path='msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=edge_options)
    
    for url in urls:
        print(url)
        driver.get(url)
        
        # Wait for the dynamic content to load
        time.sleep(5)  # Adjust time as necessary
        
        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        fund_name_element = soup.find(class_="fund-code")
        if fund_name_element:
            fund_name = fund_name_element.get_text().strip()
        else:
            fund_name = "Fund name not found"
        
        # Find elements by class name for fund names
        summary_details = soup.find_all(class_="summary-detail")
        for summary_detail in summary_details:
            # Find the fund name
        
            investment_policy_p = summary_detail.find('p', string=lambda text: 'Investment Policy' in text)
            if investment_policy_p:
                next_p_tag = investment_policy_p.find_next_sibling('p')
                if next_p_tag:
                    policy_text = next_p_tag.get_text(separator='\n', strip=True)
                else:
                    policy_text = "Policy details not found"
            else:
                policy_text = "Investment Policy not found"
            new_df = pd.DataFrame({"name": [fund_name], "policy": [policy_text]})
            df = pd.concat([df, new_df], ignore_index=True)
            print(df.to_string())
            df.to_excel("data.xlsx")
    driver.quit()
    return df

if __name__ == "__main__":
    with open("html.txt", "r", encoding="utf-8") as file:
        html_content = file.read()
    a_list = extract_a(html_content)
    # pprint.pprint(a_list)
    extract_content(a_list)
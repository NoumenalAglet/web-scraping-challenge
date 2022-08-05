# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Defining dictionary to be returned
    scraped_data = {}

    # Setting up Chrome driver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    # Latest News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div',class_='content_title').get_text()
    news_para = soup.find('div',class_='article_teaser_body').get_text()

    # JPL Space Images
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    high_res_img = browser.find_by_tag('button')[1]
    high_res_img.click()

    html = browser.html
    soup = bs(html, "html.parser")
    feat_image = soup.find("img", class_='headerimage').get('src')
    feat_image_url = f'https://spaceimages-mars.com/{feat_image}'

    # Facts Table
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)
    table_df = table[1]
    table_df.columns=['Parameter', 'Value']

    table_html = table_df.to_html()

    # Hemipshere Images
    url = "https://marshemispheres.com/"
    browser.visit(url)
    hemispheres = []
    image = browser.find_by_css('a.product-item img')

    for i in range(len(image)):
        hemi_dict ={}
        browser.find_by_css('a.product-item img')[i].click()
        samples = browser.links.find_by_text('Sample').first
        hemi_dict['title'] = browser.find_by_css('h2.title').text
        hemi_dict['img_url'] = samples['href']
        hemispheres.append(hemi_dict)
        browser.back()

    # Collecting into dictionary
    scraped_data = {
        'news_title': news_title,
        'news': news_para,
        'url_featured_image': feat_image_url,
        'mars_facts': table_html,
        'hemisphere': hemispheres
    }
    
    browser.quit()
    return scraped_data
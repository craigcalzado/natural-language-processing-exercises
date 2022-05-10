#imports
import pandas as pd
import requests
from bs4 import BeautifulSoup

#acquire news article links
def blog_links():
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    urls = [links.attrs['href'] for links in soup.select('.entry-featured-image-url')]
    
    return urls

def article(url):
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    
    return {
        'title':soup.select_one('.entry-title').text,
        'content':soup.select_one('.post-content-inner').text.strip(),
    }

def get_blog_articles():
    links = blog_links()
    df = pd.DataFrame([article(link) for link in links])
    return df

def news_card():
    response = requests.get('https://inshorts.com/en/read', headers={'User-Agent': 'Codeup Data Science'})
    soup = BeautifulSoup(response.text)
    author = soup.select_one('.author').text
    published = soup.select_one('.time').attrs['content']
    headline = soup.find_all('span', itemprop = 'headline')[0].get_text()
    
    return author, published, headline

# make function to create a list of urls 
# probably could just call this line in the main function but it was fun

def create_urls(base_url, categories):
    '''
    This function takes in a baseurl and list of categories
    It will create a new list with the base url a / and each category
    
    This is for scraping info from the inshorts website
    '''
    
    website_list = [base_url + '/' + category for category in categories]
    
    return website_list

def get_blog_articles2(base_url, categories): # title_finder, body_finder
    '''
    This function takes in a list of website urls, 
    the title finder and body finder (must be the same for each article)
    And returns a list of dictionaries with title text and body text in dictionaries
    Keys in dictionaries are 'title' and 'content'
    Returns dataframe of Titles, Articles, and Categories
    '''
    
    # initalize empty list for the dictionaries
    article_list = []
    
    # set up headers
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # create list of websites using the categories
    website_list = create_urls(base_url, categories)
    
    # loop through list of websites and category list
    for website, category in zip(website_list, categories): 
        
        # get response
        response = get(website, headers=headers)
    
        # create soup object
        soup = BeautifulSoup(response.text)
        
        # find titles
        headlines= soup.find_all('span', itemprop = 'headline')
        
        # find bodies 
        bodies = soup.find_all('div', itemprop = 'articleBody')
        
        # loop through length of headlines (could also be bodies) use index to get text and add to dictionary
        for i in range(len(headlines)):
            title = headlines[i].get_text()
            body = bodies[i].get_text()
            
            # create dictionary
            dictionary = {'title': title,
                         'content': body,
                         'category': category}
            
            # add dictionary to list of dictionaries
            article_list.append(dictionary)
        
    return pd.DataFrame(article_list)

# make function to create a list of urls 
# probably could just call this line in the main function but it was fun

def create_urls(base_url, categories):
    '''
    This function takes in a baseurl and list of categories
    It will create a new list with the base url a / and each category
    
    This is for scraping info from the inshorts website
    '''
    
    website_list = [base_url + '/' + category for category in categories]
    
    return website_list


def get_blog_articles2(base_url, categories): # title_finder, body_finder
    '''
    This function takes in a list of website urls, 
    the title finder and body finder (must be the same for each article)
    And returns a list of dictionaries with title text and body text in dictionaries
    Keys in dictionaries are 'title' and 'content'
    Returns dataframe of Titles, Articles, and Categories
    '''
    
    # initalize empty list for the dictionaries
    article_list = []
    
    # set up headers
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # create list of websites using the categories
    website_list = create_urls(base_url, categories)
    
    # loop through list of websites and category list
    for website, category in zip(website_list, categories): 
        
        # get response
        response = get(website, headers=headers)
    
        # create soup object
        soup = BeautifulSoup(response.text)
        
        # find titles
        headlines= soup.find_all('span', itemprop = 'headline')
        
        # find bodies 
        bodies = soup.find_all('div', itemprop = 'articleBody')
        
        # loop through length of headlines (could also be bodies) use index to get text and add to dictionary
        for i in range(len(headlines)):
            title = headlines[i].get_text()
            body = bodies[i].get_text()
            
            # create dictionary
            dictionary = {'title': title,
                         'content': body,
                         'category': category}
             
            # add dictionary to list of dictionaries
            article_list.append(dictionary)
        
    return pd.DataFrame(article_list)
    
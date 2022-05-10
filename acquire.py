# Imports

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import re
import requests
from requests import get
from bs4 import BeautifulSoup

###########################

def parse_gulde_news():
    """ returns dataframe of scraped web-scraping-demo.zgulde.net/news """
    # set url
    url = 'https://web-scraping-demo.zgulde.net/news' 
    agent = 'codeup ds germain'
    # query
    response = requests.get(url, headers={'User-Agent': agent}) 
    # soup
    soup = BeautifulSoup(response.text) 
    # raw list of articles
    articles = soup.select('.grid.gap-y-12 > div') 
    # list of dicts for dataframe
    article_list = [] 
    # parse each article
    for article in articles: 
        # grab title
        title = article.h2.text 
        # grab date, author, contents of article
        date, author, contents = article.select('.py-3')[0]\
            .find_all('p') 
        # add dict of info to list
        article_list.append({'title':title, 'date':date.text,
            'author':author.text, 'contents':contents.text}) 
    # return dataframe
    return pd.DataFrame(article_list) 


def parse_gulde_people():
    """ returns dataframe of scraped web-scraping-demo.zgulde.net/people """
    # set url
    url = 'https://web-scraping-demo.zgulde.net/people' 
    agent = 'codeup ds germain'
    # query
    response = requests.get(url, headers={'User-Agent': agent}) 
    # soup
    soup = BeautifulSoup(response.text) 
    # raw list of people
    people = soup.find_all('div', {'class':'person'}) 
    # list of dicts for dataframe
    info_list = [] 
    # parse each person
    for person in people: 
        # grab name
        name = person.h2.text 
        # grab more info
        quote, email, phone, address = person.find_all('p') 
        # fix info
        quote, email, phone, address = quote.text.strip(), email.text, phone.text, address.text.strip()
        # set regex for address fix
        regexp = r'\s{2,}' 
        # fix address
        address = re.sub(regexp, ' ', address) 
        # create dict
        person_dict = {'name':name, 'quote':quote, 'email':email, 
                       'phone':phone, 'address':address} 
        # add dict to list
        info_list.append(person_dict) 
    # return dataframe
    return pd.DataFrame(info_list) 


##############################

def codeup_blog_urls():
    
    """ return list of URLs for codeup blogs for exercise """
    
    url1 = 'https://codeup.com/codeup-news/codeup-launches-first-podcast-hire-tech/' 

    url2 ='https://codeup.com/tips-for-prospective-students/why-should-i-become-a-system-administrator/'
    
    url3 ='https://codeup.com/codeup-news/codeup-candidate-for-accreditation/'
    
    url4 ='https://codeup.com/codeup-news/codeup-takes-over-more-of-the-historic-vogue-building/'
    
    url5 ='https://codeup.com/codeup-news/inclusion-at-codeup-during-pride-month-and-always/'
    
    return [url1, url2, url3, url4, url5]

def acquire_codeup_blog(url):
    
    """ returns dict of one codeup blog's title, date, category, and content """
    
    # set agent
    agent = 'codeup ds germain'
    
    # query
    response = requests.get(url, headers={'User-Agent': agent})
    
    # soup
    soup = BeautifulSoup(response.text)
    
    # get title
    title = soup.select('.entry-title')[0].text
    
    # get date
    date = soup.select('.published')[0].text
    
    # get category
    category = soup.find_all('a', {'rel':'category tag'})[0].text
    
    # grab all unformatted paragraphs
    paragraphs = soup.find_all('div', {'class':'et_pb_module et_pb_post_content et_pb_post_content_0_tb_body'})[0]\
    .find_all('p')
    
    # create list for formatted paragraphs
    paragraph_list = []
    
    # iterate paragraphs
    for paragraph in paragraphs:
        
        # add to list
        paragraph_list.append(paragraph.text)
        
    # destroy href markers
    content = " ".join(paragraph_list).replace('\xa0', ' ')
    
    # create dict
    blog_info_dict = {'title':title, 'date':date, 'category':category, 'content':content}
    
    # return dict
    return blog_info_dict

def get_blogs():
    
    """ queries, returns a dataframe of each codeup blog article's stuff """
    
    list_of_blog_dicts = []
    for url in codeup_blog_urls():
        list_of_blog_dicts.append(acquire_codeup_blog(url))
    return pd.DataFrame(list_of_blog_dicts)

#####################################

def get_article(article, category):
    '''
    This function takes in an article and category and pulls
    the elements from the article of that category to be
    utilized within another function
    '''
    # Attribute selector
    title = article.select("[itemprop='headline']")[0].text
    
    # article body
    content = article.select("[itemprop='articleBody']")[0].text
    
    output = {}
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output


def get_article1(url):
    """ return dataframe of articles in inshorts category URL """
    # set agent
    agent = 'codeup ds germain' 
    # query
    response = requests.get(url, headers={'User-Agent': agent}) 
    # soup
    soup = BeautifulSoup(response.text) 
    # get cat
    category = soup.find_all('li', {'class':'active-category selected'})[0].text 
    # get raw cards
    cards = soup.select('.news-card') 
    # create list of dicts for dataframe
    card_dict_list = [] 
    # iterate each card
    for card in cards: 
        # headline
        headline = card.find_all('span', {'itemprop':'headline'})[0].text 
        # publish time
        publish_time = card.find_all('span', {'class':'time'})[0].text 
        # content
        content = card.find_all('div', {'itemprop':'articleBody'})[0].text.strip() 
        # create dict
        card_dict = {'headline':headline, 'publish_time':publish_time,
                       'category':category, 'content':content} 
        # push dict to list
        card_dict_list.append(card_dict) 
    # return dataframe
    return pd.DataFrame(card_dict_list) 



def inshorts_urls():
    """ return list of inshorts URLs for exercise """

    url1 = 'https://inshorts.com/en/read/business'
    url2 = 'https://inshorts.com/en/read/sports'
    url3 = 'https://inshorts.com/en/read/technology'
    url4 = 'https://inshorts.com/en/read/entertainment'
    return [url1, url2, url3, url4]



def get_news():
    """ query, return dataframe of inshorts business, 
        sports, tech, entertainment articles """
    # empty dataframe
    df = pd.DataFrame() 
    # read each url in list
    for url in inshorts_urls(): 
        # add each dataframe of cards to df
        df = pd.concat([df, get_article(url)])
    # return all urls' cards
    return df 


def get_all_news_articles(categories):
    """
    Takes in a list of categories where the category is part of the URL pattern on inshorts
    Returns a dataframe of every article from every category listed
    Each row in the dataframe is a single article
    """
    all_inshorts = []

    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles

    df = pd.DataFrame(all_inshorts)
    return df


def get_articles(category, base ="https://inshorts.com/en/read/"):
    """
    This function takes in a category as a string. Category must be an available category in inshorts
    Returns a list of dictionaries where each dictionary represents a single inshort article
    """
    
    # We concatenate our base_url with the category
    url = base + category
    
    # Set the headers
    headers = {"User-Agent": "Mozilla/4.5 (compatible; HTTrack 3.0x; Windows 98)"}

    # Get the http response object from the server
    response = get(url, headers=headers)

    # Make soup out of the raw html
    soup = BeautifulSoup(response.text)
    
    # Ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    output = []
    
    # Iterate through every article tag/soup 
    for article in articles:
        
        # Returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        # Append the dictionary to the list
        output.append(article_data)
    
    # Return the list of dictionaries
    return output

#def get_blog_articles(url):
    '''
    This function takes in a url and pull the necessary elements off the website
    then creates a dictionary with those elements
    '''

    # create an empty dictionary to append to
    blog_dict = {}
    
    # fetch the data
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    
    # pull the elements from the soup
    article = soup.find('div', class_='jupiterx-post-content') # pulling body of text
    title = soup.find('h1', class_='jupiterx-post-title') # pulling title as text
    
    # append the elements to the dictionary
    blog_dict = {'title': title.text,
                'content': article.text}
    
    # return dictionary
    return blog_dict

##################################


def get_front_page_links():
    """
    Short function to hit the codeup blog landing page and return a list of all the urls to further blog posts on the
    page.
    """
    response = requests.get("https://codeup.com/blog/", headers={"user-agent": "Codeup DS"})
    soup = BeautifulSoup(response.text)
    links = [link.attrs["href"] for link in soup.select(".more-link")]
    return links

def parse_codeup_blog_article(url):
    "Given a blog article url, extract the relevant information and return it as a dictionary."
    response = requests.get(url, headers={"user-agent": "Codeup DS"})
    soup = BeautifulSoup(response.text)
    return {
        "title": soup.select_one(".entry-title").text,
        "published": soup.select_one(".published").text,
        "content": soup.select_one(".et_pb_post_content").text.strip(),
    }


def get_blog_articles():
    "Returns a dataframe where each row is a blog post from the codeup blog landing page."
    links = get_front_page_links()
    df = pd.DataFrame([parse_codeup_blog_article(link) for link in links])
    return df
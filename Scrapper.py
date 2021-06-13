
import requests
from bs4 import BeautifulSoup
import pprint

'''
This scraping module works for hacker news only.


It only shows the Title, Link, Votes of articles 
that have more than 99 votes.

Can change the "pages" variable into desired scraping 
amount of pages

Ex: if pages = 3, it will scrape info from pages 1 ~ 3, and 
display those that have more than 99 votes



'''

target_website = 'https://news.ycombinator.com/'
pages = 1


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda x: x['Votes'], reverse=True)


def create_custom_hn(links, subtext):
    '''
    function: create_custom_hn
    param: bs4.element.ResultSet, bs4.element.ResultSet
    return:  list (containing dictionary)
    utility:
    - gather title, link and votes of each article and establish it as 
    a dict. Then append it into a list.

    '''
    hn = []
    for idx, items in enumerate(links):
        title = links[idx].getText()

        # none if doesn't have a proper link
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'Title': title, 'Link': href, 'Votes': points})
    return sort_stories_by_votes(hn)


def hn_multi_page_scrape():
    '''
    function: hn_multi_page_scrape
    param: N/A
    return:  N/A
    utility:
    - iterates depending amount of pages requesetd
    - request desired html info for each requested page
    - and displays the info
    '''
    print("Start of multi_page_scrape")

    for page in range(1, (pages+1)):
        page_change = target_website + "/news?p=" + str(page)

        # html request
        res = requests.get(page_change)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        pprint.pprint(create_custom_hn(links, subtext), sort_dicts=False)


if __name__ == '__main__':
    hn_multi_page_scrape()

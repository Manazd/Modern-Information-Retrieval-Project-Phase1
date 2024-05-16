from requests import get
from bs4 import BeautifulSoup
from collections import deque
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
import json


class IMDbCrawler:
    """
    put your own user agent in the headers
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    top_250_URL = 'https://www.imdb.com/chart/top/'

    def __init__(self, crawling_threshold=1100):
        """
        Initialize the crawler

        Parameters
        ----------
        crawling_threshold: int
            The number of pages to crawl
        """
        # TODO
        self.crawling_threshold = crawling_threshold
        self.not_crawled = deque()
        self.crawled = []
        self.added_ids = set()
        self.add_list_lock = Lock()
        self.add_queue_lock = Lock()

    def get_id_from_URL(self, URL):
        """
        Get the id from the URL of the site. The id is what comes exactly after title.
        for example the id for the movie https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1 is tt0111161.

        Parameters
        ----------
        URL: str
            The URL of the site
        Returns
        ----------
        str
            The id of the site
        """
        # TODO
        return URL.split('/')[4]

    def write_to_file_as_json(self):
        """
        Save the crawled files into json
        """
        with open('IMDB_crawled.json', 'w') as f:
            json.dump(list(self.crawled), f, indent=2)

        with open('IMDB_not_crawled.json', 'w') as f:
            json.dump(list(self.not_crawled), f, indent=2)
        
        with open('IMDB_added_ids.json', 'w') as f:
            json.dump(list(self.added_ids), f, indent=2)

    def read_from_file_as_json(self):
        """
        Read the crawled files from json
        """
        with open('IMDB_crawled.json', 'r') as f:
            self.crawled = json.load(f)

        with open('IMDB_not_crawled.json', 'r') as f:
            self.not_crawled = json.load(f)

        with open('IMDB_added_ids.json', 'r') as f:
            self.added_ids = json.load(f)

    def crawl(self, URL):
        """
        Make a get request to the URL and return the response

        Parameters
        ----------
        URL: str
            The URL of the site
        Returns
        ----------
        requests.models.Response
            The response of the get request
        """
        # TODO
        return get(URL, headers=self.headers)

    def extract_top_250(self):
        """
        Extract the top 250 movies from the top 250 page and use them as seed for the crawler to start crawling.
        """
        # TODO update self.not_crawled and self.added_ids

        top_250 = 'https://www.imdb.com/chart/top/'
        html_response = get(top_250, headers=self.headers)
        soup = BeautifulSoup(html_response.text, 'html.parser')  

        tag = soup.find('script', {'id': '__NEXT_DATA__'})
        json_data = json.loads(tag.contents[0])
        movies = json_data['props']['pageProps']['pageData']['chartTitles']['edges']

        for i, movie in enumerate(movies):
            id = movie['node']['id']
            link = 'https://www.imdb.com/title/' + str(id)
            self.added_ids.add(id)
            self.not_crawled.append(link)

    def get_imdb_instance(self):
        return {
            'id': None,  # str
            'title': None,  # str
            'first_page_summary': None,  # str
            'release_year': None,  # str
            'mpaa': None,  # str
            'budget': None,  # str
            'gross_worldwide': None,  # str
            'rating': None,  # str
            'directors': None,  # List[str]
            'writers': None,  # List[str]
            'stars': None,  # List[str]
            'related_links': None,  # List[str]
            'genres': None,  # List[str]
            'languages': None,  # List[str]
            'countries_of_origin': None,  # List[str]
            'summaries': None,  # List[str]
            'synopsis': None,  # List[str]
            'reviews': None,  # List[List[str]]
        }

    def start_crawling(self):
        """
        Start crawling the movies until the crawling threshold is reached.
        TODO: 
            replace WHILE_LOOP_CONSTRAINTS with the proper constraints for the while loop.
            replace NEW_URL with the new URL to crawl.
            replace THERE_IS_NOTHING_TO_CRAWL with the condition to check if there is nothing to crawl.
            delete help variables.

        ThreadPoolExecutor is used to make the crawler faster by using multiple threads to crawl the pages.
        You are free to use it or not. If used, not to forget safe access to the shared resources.
        """

        self.extract_top_250()
        futures = []
        crawled_counter = 0
        lock = Lock()

        with ThreadPoolExecutor(max_workers=20) as executor:
            while self.not_crawled and crawled_counter < self.crawling_threshold:
                URL = self.not_crawled.popleft()
                futures.append(executor.submit(self.crawl_page_info, URL))
                with lock:
                    crawled_counter += 1
                if not self.not_crawled:
                    wait(futures)
                    futures = []
                

    def crawl_page_info(self, URL):
        """
        Main Logic of the crawler. It crawls the page and extracts the information of the movie.
        Use related links of a movie to crawl more movies.
        
        Parameters
        ----------
        URL: str
            The URL of the site
        """
        html_response = self.crawl(URL)
        imdb_instance  = self.get_imdb_instance()
        doc = BeautifulSoup(html_response.text, "html.parser")
        self.extract_movie_info(doc, imdb_instance, URL)

        print("new iteration")
        pass

    def extract_movie_info(self, res, movie, URL):
        """
        Extract the information of the movie from the response and save it in the movie instance.

        Parameters
        ----------
        res: requests.models.Response
            The response of the get request
        movie: dict
            The instance of the movie
        URL: str
            The URL of the site
        """
        # TODO
        summary_url = self.get_summary_link(URL)
        summary_soup = BeautifulSoup(self.crawl(summary_url).text, "html.parser")

        review_url = self.get_review_link(URL)
        review_soup = BeautifulSoup(self.crawl(review_url).text, "html.parser")
        mpaa_url = URL + 'parentalguide'
        mpaa_soup = BeautifulSoup(self.crawl(mpaa_url).text, "html.parser")

        movie_id = self.get_id_from_URL(URL)
        related_links = self.get_related_links(res)

        for link in related_links:
            id = self.get_id_from_URL(link)
            if id not in self.added_ids:            
              with self.add_queue_lock:
                self.not_crawled.append(link)
              with self.add_list_lock:
                self.added_ids.add(id)
  
        movie['id'] = movie_id
        movie['title'] = self.get_title(res)
        movie['first_page_summary'] = self.get_first_page_summary(res)
        movie['release_year'] = self.get_release_year(res)
        movie['mpaa'] = self.get_mpaa(mpaa_soup, res)
        movie['budget'] = self.get_budget(res)
        movie['gross_worldwide'] = self.get_gross_worldwide(res)
        movie['directors'] = self.get_director(res)
        movie['writers'] = self.get_writers(res)
        movie['stars'] = self.get_stars(res)
        movie['related_links'] = related_links
        movie['genres'] = self.get_genres(res)
        movie['languages'] = self.get_languages(res)
        movie['countries_of_origin'] = self.get_countries_of_origin(res)
        movie['rating'] = self.get_rating(res)
        movie['summaries'] = self.get_summary(summary_soup)
        movie['synopsis'] = self.get_synopsis(summary_soup)
        movie['reviews'] = self.get_reviews_with_scores(review_soup)

        with self.add_queue_lock:
          self.crawled.append(movie)

    def get_summary_link(self, url):
        """
        Get the link to the summary page of the movie
        Example:
        https://www.imdb.com/title/tt0111161/ is the page
        https://www.imdb.com/title/tt0111161/plotsummary is the summary page

        Parameters
        ----------
        url: str
            The URL of the site
        Returns
        ----------
        str
            The URL of the summary page
        """
        try:
            str = url + '/plotsummary'
            return str
        except:
            print("failed to get summary link")
            return "No summary link"

    def get_review_link(self, url):
        """
        Get the link to the review page of the movie
        Example:
        https://www.imdb.com/title/tt0111161/ is the page
        https://www.imdb.com/title/tt0111161/reviews is the review page
        """
        try:
            str = url + '/reviews'
            return str
        except:
            print("failed to get review link")
            return "No review link"

    def get_title(self, soup):
        """
        Get the title of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The title of the movie

        """
        try:
            movie_title = soup.find('title')
            return movie_title.string
        except:
            print("failed to get title")
            return "No title"

    def get_first_page_summary(self, soup):
        """
        Get the first page summary of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The first page summary of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            summary = json_data['props']['pageProps']['aboveTheFoldData']['plot']['plotText']['plainText']
            return summary
        except:
            print("failed to get first page summary")
            return "No first page summary"

    def get_director(self, soup):
        """
        Get the directors of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The directors of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            data = json_data['props']['pageProps']['mainColumnData']['directors']
            num_directors = data[0]['totalCredits']
            
            directors = []

            for director in data:
                credits = director['credits']
                for credit in credits:
                    director_name = credit['name']['nameText']['text']
                    directors.append(director_name)
            return directors
        except:
            print("failed to get director")
            res = ['No directors']
            return res

    def get_stars(self, soup):
        """
        Get the stars of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The stars of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            stars = json_data['props']['pageProps']['aboveTheFoldData']['principalCredits'][2]['credits']
                
            stars_names = []
            
            for star in stars:
                name = star['name']['nameText']['text']
                stars_names.append(name)
            return stars_names
        except:
            print("failed to get stars")
            res = ['No stars']
            return res

    def get_writers(self, soup):
        """
        Get the writers of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The writers of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            data = json_data['props']['pageProps']['mainColumnData']['writers']
            
            writers = []
            
            for writer in data:
                credits = writer['credits']
                for credit in credits:
                    director_name = credit['name']['nameText']['text']
                    writers.append(director_name)
            return writers
        except:
            print("failed to get writers")
            res = ['No writers']
            return res

    def get_related_links(self, soup):
        """
        Get the related links of the movie from the More like this section of the page from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The related links of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            more_like_this_list = json_data['props']['pageProps']['mainColumnData']['moreLikeThisTitles']['edges']    
            
            links = []
            
            for movie in more_like_this_list:
                id = movie['node']['id']
                link = 'https://www.imdb.com/title/' + id
                links.append(link)
            return links
        except:
            print("failed to get related links")
            res = ['No related links']
            return res

    def get_summary(self, soup):
        """
        Get the summary of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The summary of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            summaries_list = json_data['props']['pageProps']['contentData']['categories'][0]['section']['items']

            summaries = []

            for i, summary in enumerate(summaries_list):
                text = summary['htmlContent']
                summaries.append(text)    
            return summaries 
        except:
            print("failed to get summary")
            res = ['No summary']
            return res

    def get_synopsis(self, soup):
        """
        Get the synopsis of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The synopsis of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            synopsis_list = json_data['props']['pageProps']['contentData']['categories'][1]['section']['items']
            synopsis = []
            texts = synopsis_list[0]['htmlContent'].split('<br/><br/>')
            for text in texts:
                synopsis.append(text)
            return synopsis
        except:
            print("failed to get synopsis")
            res = ['No synopsis']
            return res

    def get_reviews_with_scores(self, soup):
        """
        Get the reviews of the movie from the soup
        reviews structure: [[review,score]]

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[List[str]]
            The reviews of the movie
        """
        try:
            rating_tags = soup.find_all('span', class_='rating-other-user-rating')

            ratings = []

            for rate in rating_tags:
                rating = rate.find('span').text
                ratings.append(rating)

            reviews_list = soup.find_all('div', class_='lister-item mode-detail imdb-user-review collapsable')

            results_list = []

            for i, item in enumerate(reviews_list):
                review_text = item.find('div', class_='text show-more__control').text
                results_list.append([ratings[i], review_text])
            
            return results_list
        except:
            print("failed to get reviews")
            res_1 = ['No generes']
            res = []
            res.append(res_1)
            return res

    def get_genres(self, soup):
        """
        Get the genres of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The genres of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            genres_tag = json_data['props']['pageProps']['aboveTheFoldData']['genres']['genres']
            
            genres = []
            
            for genre in genres_tag:
                genres.append(genre['text'])
            return genres    
        except:
            print("Failed to get generes")
            res = ['No generes']
            return res

    def get_rating(self, soup):
        """
        Get the rating of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The rating of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            imdb_rating = json_data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
            return str(imdb_rating)
        except:
            print("failed to get rating")
            return "No rating"

    def get_mpaa(self, soup, res):
        """
        Get the MPAA of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The MPAA of the movie
        """
        try:
            # Get mpaa from parentalguide
            # doc = soup.find('tr', class_="ipl-zebra-list__item")
            # mpaa = doc.find_all('td')[1].text

            tag = res.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            mpaa = json_data['props']['pageProps']['aboveTheFoldData']['certificate']['rating']
            return mpaa
        except:
            print("failed to get mpaa")
            return "No mpaa"

    def get_release_year(self, soup):
        """
        Get the release year of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The release year of the movie
        """
        try:
            release_year = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(release_year.contents[0])
            year = str(json_data['props']['pageProps']['aboveTheFoldData']['releaseYear']['year'])
            return year
        except:
            print("failed to get release year")
            return "No release year"

    def get_languages(self, soup):
        """
        Get the languages of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The languages of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])
            spoken_languages = json_data['props']['pageProps']['mainColumnData']['spokenLanguages']['spokenLanguages']
           
            languages = []
           
            for language in spoken_languages:
                languages.append(language['text']) 
            return languages
        except:
            print("failed to get languages")
            res = ['No languages']
            return res

    def get_countries_of_origin(self, soup):
        """
        Get the countries of origin of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The countries of origin of the movie
        """
        try:
            tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(tag.contents[0])

            countries_of_origin = json_data['props']['pageProps']['mainColumnData']['countriesOfOrigin']['countries']

            countries = []
            for counrty in countries_of_origin:
                countries.append(counrty['text']) 
            return countries
        except:
            print("failed to get countries of origin")
            res = ['No countries of origin']
            return res

    def get_budget(self, soup):

        """
        Get the budget of the movie from box office section of the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The budget of the movie
        """
        try:
            budget_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(budget_tag.contents[0])
            amount = json_data['props']['pageProps']['mainColumnData']['productionBudget']['budget']['amount']
            currency = json_data['props']['pageProps']['mainColumnData']['productionBudget']['budget']['currency']
            budget = f'{amount} {currency}'
            return budget
        except:
            print("failed to get budget")
            return "No budget"

    def get_gross_worldwide(self, soup):
        """
        Get the gross worldwide of the movie from box office section of the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The gross worldwide of the movie
        """
        try:
            gross_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            json_data = json.loads(gross_tag.contents[0])
            money = json_data['props']['pageProps']['mainColumnData']['worldwideGross']['total']['amount']
            return str(money)
        except:
            print("failed to get gross worldwide")
            return "No gross worldwide"


def main():
    imdb_crawler = IMDbCrawler(crawling_threshold=1100)
    # imdb_crawler.read_from_file_as_json()
    imdb_crawler.start_crawling()
    imdb_crawler.write_to_file_as_json()


if __name__ == '__main__':
    main()
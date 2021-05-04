import rdflib
import lxml.html
import requests

'''
Global params
'''
WIKI_PREFIX = "https://en.wikipedia.org"
EXAMPLE_PREFIX = "http://example.org/"
URL = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"
DIRECTORS_URL = []
ACTORS_URL=[]
PRODUCERS_URL=[]


def create_ontology():
    '''
    :return: ontology.nt.
    '''
    res = requests.get(URL)
    doc = lxml.html.fromstring(res.content)
    graph =rdflib.Graph()
    movie_links=doc.xpath("//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/a/@href |"
                    " //table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/b/a/@href |"
                    "//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/span/span/span/a/@href"
                    "")
    global  DIRECTORS_URL
    global ACTORS_URL
    global PRODUCERS_URL
    for link in movie_links:
        movie = rdflib.URIRef(EXAMPLE_PREFIX+create_name(link))
        create_directors(graph, link, movie)
        create_producers(graph, link, movie)
        create_actors(graph, link, movie)
        create_length(graph, link, movie)
        create_based_on(graph, link, movie)
        create_released_date(graph, link, movie)
    for link in DIRECTORS_URL:
        create_occupartion(graph,link)
        create_birthday(graph,link)
    for link in PRODUCERS_URL:
        create_occupartion(graph,link)
        create_birthday(graph,link)
    for link in ACTORS_URL:
        create_occupartion(graph,link)
        create_birthday(graph,link)
    graph.serialize("ontology.nt", format="nt")

def create_occupartion(graph,link):
    '''

    :param graph:
    :param link:
    :return: update graph with Relation
    '''
    occupartion_is = rdflib.URIRef(EXAMPLE_PREFIX + 'occupartion')
    occupartions = Occupartion_info(link)
    people = rdflib.URIRef(EXAMPLE_PREFIX+create_name(link))
    if occupartions!=None:
        for occupartion in occupartions:
            if occupartion!= ', ':
                occupartion_o = rdflib.URIRef(EXAMPLE_PREFIX + occupartion.replace(" ", "_"))
                graph.add((people, occupartion_is, occupartion_o))


def Occupartion_info(link):
    '''

       :param link of movie
       :return: xpath human
       '''
    occupartions = []
    res = requests.get(WIKI_PREFIX + link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox != []:
        occupartions = infobox[0].xpath("//table//th[contains(text(), 'Occupartion')]/../td/a[text() !=' ' and text()!=', ']/text() |"
                                     "//table//th[contains(text(), 'Occupartion')]/../td/div/ul/li[text() !=' ' and text()!=', ']/text()|"
                                     "//table//th[contains(text(), 'Occupartion')]/../td/div/ul/li/a[text() !=' ' and text()!=', ']/text()|"
                                     "//table//th[contains(text(), 'Occupartion')]/../td[text() !=' ' and text()!=', ']/text()|"
                                    " //table//th[contains(text(), 'Occupartion')]/../td/ul/li/a[text() !=' ' and text()!=', ']/text()"
                                     )
        if occupartions==[]:
            occupartions = infobox[0].xpath("//table//th[contains(text(), 'Occupation')]/../td/a[text() !=' ' and text()!=', ']/text() |"
                                     "//table//th[contains(text(), 'Occupation')]/../td/div/ul/li[text() !=' ' and text()!=', ']/text()|"
                                     "//table//th[contains(text(), 'Occupation')]/../td/div/ul/li/a[text() !=' ' and text()!=', ']/text()|"
                                    "//table//th[contains(text(), 'Occupation')]/../td/ul/li/a[text() !=' ' and text()!=', ']/text()|"
                                     "//table//th[contains(text(),'Occupation')]/../td[text() !=' ' and text()!=', ']/text()|"
                                            "//table//th/span[contains(text(),'Occupation(s)')]/../../td/a[text() !=' ' and text()!=', ']/text()|"
                                            "//table//th/span[contains(text(),'Occupation(s)')]/../../td/div/ul/li[text() !=' ' and text()!=', ']/text()|"
                                            "//table//th/span[contains(text(),'Occupation(s)')]/../../td/ul/li/a[text() !=' ' and text()!=', ']/text()|"
                                            "//table//th/span[contains(text(),'Occupation(s)')]/../../td[text() !=' ' and text()!=', ']/text()|"
                                            "//table//th/span[contains(text(),'Occupation(s)')]/../../td/a[text() !=' ' and text()!=', ']/text()")
        return occupartions

def create_birthday(graph,link):
    '''

    :param graph:
    :param link:
    :return: update graph with Relation
    '''
    born_at = rdflib.URIRef(EXAMPLE_PREFIX + 'born_at')
    Birthday = BirthDay_info(link)
    people = rdflib.URIRef(EXAMPLE_PREFIX+create_name(link))
    if Birthday!=None:
        for occupartion in Birthday:
            if occupartion!= ', ':
                date = rdflib.URIRef(EXAMPLE_PREFIX + occupartion.replace(" ", "_"))
                graph.add((people, born_at, date))


def BirthDay_info(link):
    '''
       :param link of movie
       :return: xpath human
       '''
    Birthday = []
    res = requests.get(WIKI_PREFIX + link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    new_dates=[]
    if infobox != []:
        Birthday = infobox[0].xpath( "//table//th[contains(text(), 'Born')]/../td/div/ul/li/span/span[contains(@class,'bday')]/text() |"
            "//table//th[contains(text(), 'Born')]/../td/div/ul/li/span/span[contains(@class,'bday')]/text()|"
            "//table//th[contains(text(), 'Born')]/../td[text() !=' ']/span/span[contains(@class,'bday')]/text()|"
            "//table//th[contains(text(), 'Born')]/../td/span/span[contains(@class,'bday')]/text()|"
            "//table//th[contains(text(), 'Born')]/../td/span/div/ul/li/span/span[contains(@class,'bday')]/text() |"
            "//table//th[contains(text(), 'Born')]/../td/span/span[contains(@class,'bday')]/text()|"
            "//table//th[contains(text(), 'Born')]/../td/div/div/ul/li/span/span[contains(@class,'bday')]/text()|"
                                     "//table//th[contains(text(), 'Born')]/../td/span/span/span[contains(@class,'bday')]/text()")

        if Birthday==[]:
            Birthday = infobox[0].xpath("//table//th[contains(text(), 'Born')]/../td/div/ul/li/span/span/text() |"
                                        "//table//th[contains(text(), 'Born')]/../td/div/ul/li/span/span/text()|"
                                        "//table//th[contains(text(), 'Born')]/../td[text() !=' ']/span/span/text()|"
                                        "//table//th[contains(text(), 'Born')]/../td[text() !=' ']/text()|"
                                        "//table//th[contains(text(), 'Born')]/../td/span/span/text()|"
                                        "//table//th[contains(text(), 'Born')]/../td/span/div/ul/li/span/span/text() |"
                                        "//table//th[contains(text(), 'Born')]/../td/span/span/text()"
                                        )
        if Birthday == []:
            Birthday = infobox[0].xpath(
                "//table//th[contains(text(), 'Born')]/../td/div/ul/li/text() |"
                "//table//th[contains(text(), 'Born')]/../td/div/ul/li/text()|"
                "//table//th[contains(text(), 'Born')]/../td[text() !=' ']/text()|"
                "//table//th[contains(text(), 'Born')]/../td[text() !=' ']/text()|"
                "//table//th[contains(text(), 'Born')]/../td/span/span/text()|"
                "//table//th[contains(text(), 'Born')]/../td/span/div/ul/li/text() |"
                "//table//th[contains(text(), 'Born')]/../td/text()"
            )
        for i in range(len(Birthday)):
                if Birthday[i] == "" or Birthday[i] == " ":
                    continue
                else:
                    check = list(Birthday[i])
                    for char in check:
                        if char.isnumeric():
                            new_dates.append(Birthday[i])
                            break
        return new_dates
    return Birthday


def create_directors(graph,link,movie):
    '''

    :param graph:
    :param link:
    :param movie:
    :return: update graph with Relation
    '''
    Directed_by = rdflib.URIRef(EXAMPLE_PREFIX + 'Directed_by')
    directors = director_info(link)
    for director in directors:
        director_o = rdflib.URIRef(EXAMPLE_PREFIX + director.replace(" ", "_"))
        graph.add((movie, Directed_by, director_o))

def director_info(link):
    '''

    :param link of movie
    :return: xpath result
    '''
    directors=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    global DIRECTORS_URL
    if infobox !=[]:
        directors = infobox[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td[text() !=' ']/text()"
                                     )
        DIRECTORS_URL+=infobox[0].xpath( "//table//th[contains(text(), 'Directed by')]/../td/a/@href|"
                                   "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/@href")
    return directors

def create_actors(graph,link,movie):
    '''

    :param graph:
    :param link:
    :param movie:
    :return: update graph with Relation
    '''
    Starring = rdflib.URIRef(EXAMPLE_PREFIX + 'Starring')
    actors = actor_info(link)
    for actor in actors:
        actor_o = rdflib.URIRef(EXAMPLE_PREFIX + actor.replace(" ", "_"))
        graph.add((movie, Starring, actor_o))

def actor_info(link):
    '''

    :param link of movie
    :return: xpath result
    '''
    actors=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    global ACTORS_URL
    if infobox !=[]:
        actors = infobox[0].xpath("//table//th[contains(text(), 'Starring')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Starring')]/../td[text() !=' ']/text()"
                                     )
        ACTORS_URL+=infobox[0].xpath("//table//th[contains(text(), 'Starring')]/../td/a/@href|"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/a/@href")
    return actors

def create_producers(graph,link,movie):
    '''

    :param graph:
    :param link:
    :param movie:
    :return: update graph with Relation
    '''
    producer_by = rdflib.URIRef(EXAMPLE_PREFIX + 'Produced_by')
    producers = producer_info(link)
    for producer in producers:
        producer_o = rdflib.URIRef(EXAMPLE_PREFIX + producer.replace(" ", "_"))
        graph.add((movie, producer_by, producer_o))

def producer_info(link):
    '''

    :param link of movie
    :return: xpath result
    '''
    producers=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    global PRODUCERS_URL
    if infobox !=[]:
        producers = infobox[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Produced by')]/../td[text() !=' ' and text() !=': ']/text()"
                                     )
        PRODUCERS_URL+= infobox[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/@href|"
                                   "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/@href")

    return producers




def create_released_date(graph,link,movie):
    '''

    :param graph:
    :param link:
    :param movie:
    :return: update graph with Relation
    '''
    released_date = rdflib.URIRef(EXAMPLE_PREFIX + 'released_date')
    dates = release_date_info(link)
    for date in dates:
        date_o = rdflib.URIRef(EXAMPLE_PREFIX + date.replace(" ", "_"))
        graph.add((movie, released_date, date_o))

def release_date_info(link):
    '''

    :param link of movie
    :return: xpath result
    '''
    dates=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    new_dates=[]
    if infobox !=[]:
        dates = infobox[0].xpath("//table//th/div[contains(text(), 'Release date')]/../../td/div/ul/li/span/span/text() |"
                                 "//table//th/div[contains(text(), 'Release date')]/../../td/div/ul/li/span/span/text()|"
                                     "//table//th/div[contains(text(), 'Release date')]/../../td[text() !=' ']/span/span/text()|"
                                 "//table//th/div[contains(text(), 'Publication date')]/../../td[text() !=' ']/text()|"
                                 "//table//th[contains(text(), 'Release date')]/../td/span/span/text()|"
                                 "//table//th/div[contains(text(), 'Release date')]/../../td/span/div/ul/li/span/span/text() |"
                                 "//table//th/div[contains(text(), 'Release date')]/../../td/span/span/text()"
                                 )
        if dates==[]:
            dates = infobox[0].xpath(
                "//table//th/div[contains(text(), 'Release date')]/../../td/div/ul/li/text() |"
                "//table//th/div[contains(text(), 'Release date')]/../../td/div/ul/li/text()|"
                "//table//th/div[contains(text(), 'Release date')]/../../td[text() !=' ']/text()|"
                "//table//th/div[contains(text(), 'Publication date')]/../../td[text() !=' ']/text()|"
                "//table//th[contains(text(), 'Release date')]/../td/span/span/text()|"
                "//table//th/div[contains(text(), 'Release date')]/../../td/span/div/ul/li/text() |"
                "//table//th/div[contains(text(), 'Release date')]/../../td/text()"
                )
            for i in range(len(dates)):
                if dates[i] == "" or dates[i] == " ":
                    continue
                else:
                    check = dates[i].split()
                    for char in check:
                        if char.isnumeric():
                            new_dates.append(dates[i])
                            break
            return new_dates

    for i in range(len(dates)):
        if  dates[i]=="" or dates[i]==" " :
            continue
        else :
                    new_dates.append(dates[i])

    return new_dates


def create_based_on(graph,link,movie):
    '''

    :param graph:
    :param link:
    :param movie:
    :return: update graph with Relation
    '''
    based_on = rdflib.URIRef(EXAMPLE_PREFIX + 'Based_on')
    books = book_info(link)
    for book in books:
        book_o = rdflib.URIRef(EXAMPLE_PREFIX + (book.replace(" ", "_")).replace('"',""))
        graph.add((movie, based_on, book_o))

def book_info(link):
    '''

    :param link of movie
    :return: xpath result
    '''
    books=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox !=[]:
        books = infobox[0].xpath("//table//th[contains(text(), 'Based on')]/../td/i/a/text() |"
                                     "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Based on')]/../td[text() !=' ']/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/a/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/i/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/i/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/i/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/a/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/div/a/text() | "
                                 "//table//th[contains(text(), 'Based on')]/../td/div/a/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/div/i/a/text()")

    new_books=[]
    flag=False
    for i in range(len(books)):
        if str(books[i].replace(" ",""))=="by":
            flag=True
            continue
        if (flag==True):
            flag=False
            continue
        if (books[i]==" "):
            continue
        new_books.append(books[i])
    return new_books


def create_length(graph,link,movie):
    '''

    :param graph:
    :param link:
    :param movie:
    :return: update graph with Relation
    '''
    Running_time = rdflib.URIRef(EXAMPLE_PREFIX + 'Running_time')
    lentgth = length_info(link)
    for l in lentgth:
        length_o = rdflib.URIRef(EXAMPLE_PREFIX + l.replace(" ", "_"))
        graph.add((movie, Running_time, length_o))

def length_info(link):
    '''

    :param link of movie
    :return: xpath result
    '''
    lentgth=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox !=[]:
        lentgth = infobox[0].xpath("//table//div[contains(text(), 'Running time')]/../../td/a/text() |"
                                     "//table//div[contains(text(), 'Running time')]/../../td/div/ul/li/text()|"
                                     "//table//div[contains(text(), 'Running time')]/../../td/div/ul/li/a/text()|"
                                     "//table//div[contains(text(), 'Running time')]/../../td[text() !=' ']/text()"
                                     )
    return lentgth


def create_name(link):
    '''
    :param link:
    :return: movie's name
    '''
    name = link.split("wiki/")[1].replace(" ", "_")
    return name


def checkAll():
    '''
    :return: check if that all movies in ontology (we used it after each xpath query)
    '''
    res = requests.get(URL)
    doc = lxml.html.fromstring(res.content)
    movie_links = doc.xpath(
        "//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/a/@href |"
        " //table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/b/a/@href |"
        "//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/span/span/span/a/@href"
        "")
    moves = []
    for link in movie_links:
        moves.append(link.split("wiki/")[1])
    doc=open('ontology.nt','r').read()
    for movie in moves:
        if movie not in doc:
            print(movie)

def check_perosons():
    '''
    :return: check if that all persons in ontology (we used it after each xpath query)
    '''
    global  ACTORS_URL  #todo:change according the check
    persons=[]
    for person in ACTORS_URL: # todo : change it too
        persons.append(person.split("wiki/")[1])
    doc = open('ontology.nt', 'r').read()
    for person in persons:
        if person not in doc:
            print(person)

if __name__ == '__main__':

    create_ontology()
    #checkAll()
    #check_perosons()
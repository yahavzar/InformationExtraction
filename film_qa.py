import rdflib
import lxml.html
import requests

WIKI_PREFIX = "https://en.wikipedia.org"
EXAMPLE_PREFIX = "http://example.org/"
URL = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"
DIRECTORS_URL = []

def create_ontology():
    res = requests.get(URL)
    doc = lxml.html.fromstring(res.content)
    graph =rdflib.Graph()
    links_text_forDebug=doc.xpath("//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/a/text() |"
                    " //table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/b/a/text() |"
                    "//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/span/span/span/a/text()"
                    "")
    movie_links=doc.xpath("//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/a/@href |"
                    " //table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/b/a/@href |"
                    "//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../../td[1]/i/span/span/span/a/@href"
                    "")
    #links2 = doc.xpath("//table[@class='wikitable sortable']/tbody/tr/td[2]/a[1][text() >'2009']/../..")
    for link in movie_links:
        movie = rdflib.URIRef(EXAMPLE_PREFIX+create_name(link))
        create_directors(graph, link, movie)
        create_producers(graph, link, movie)
        create_actors(graph, link, movie)
        create_length(graph, link, movie)
        #create_academy_award(graph, link, movie)
    graph.serialize("ontology.nt", format="nt")


def create_directors(graph,link,movie):
    Directed_by = rdflib.URIRef(EXAMPLE_PREFIX + 'Directed_by')
    directors = director_info(link)
    for director in directors:
        director_o = rdflib.URIRef(EXAMPLE_PREFIX + director.replace(" ", "_"))
        graph.add((movie, Directed_by, director_o))

def director_info(link):
    directors=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox !=[]:
        directors = infobox[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td[text() !=' ']/text()"
                                     )
    return directors

def create_academy_award(graph,link,movie):
    academy_award = rdflib.URIRef(EXAMPLE_PREFIX + 'won')
    awards = director_info(link)
    for award in awards:
        award_o = rdflib.URIRef(EXAMPLE_PREFIX + award.replace(" ", "_"))
        graph.add((movie, academy_award, award_o))

def academy_award_info(link):
    awards=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox !=[]:
        awards = infobox[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td[text() !=' ']/text()"
                                     )
    return awards

def create_length(graph,link,movie):
    Running_time = rdflib.URIRef(EXAMPLE_PREFIX + 'Running_time')
    lentgth = length_info(link)
    for l in lentgth:
        length_o = rdflib.URIRef(EXAMPLE_PREFIX + l.replace(" ", "_"))
        graph.add((movie, Running_time, length_o))

def length_info(link):
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

def create_actors(graph,link,movie):
    Starring = rdflib.URIRef(EXAMPLE_PREFIX + 'Starring')
    actors = actor_info(link)
    for actor in actors:
        actor_o = rdflib.URIRef(EXAMPLE_PREFIX + actor.replace(" ", "_"))
        graph.add((movie, Starring, actor_o))

def actor_info(link):
    actors=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox !=[]:
        actors = infobox[0].xpath("//table//th[contains(text(), 'Starring')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Starring')]/../td[text() !=' ']/text()"
                                     )
    return actors

def create_producers(graph,link,movie):
    producer_by = rdflib.URIRef(EXAMPLE_PREFIX + 'Produced_by')
    producers = producer_info(link)
    for producer in producers:
        producer_o = rdflib.URIRef(EXAMPLE_PREFIX + producer.replace(" ", "_"))
        graph.add((movie, producer_by, producer_o))

def producer_info(link):
    producers=[]
    res = requests.get(WIKI_PREFIX+link)
    doc = lxml.html.fromstring(res.content)
    infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    if infobox !=[]:
        producers = infobox[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/text() |"
                                     "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/text()|"
                                     "//table//th[contains(text(), 'Produced by')]/../td[text() !=' ' and text() !=': ']/text()"
                                     )
    return producers



def create_name(link):
    name = link.split("wiki/")[1].replace(" ", "_")
    return name


def checkAll():
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


if __name__ == '__main__':

    create_ontology()
    checkAll()
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
        Directed_by = rdflib.URIRef(EXAMPLE_PREFIX+'Directed_by')
        directors = director_info(link)
        for director in directors:
            director_o = rdflib.URIRef(EXAMPLE_PREFIX+director.replace(" ", "_"))
            graph.add((movie,Directed_by,director_o))
    graph.serialize("ontology.nt", format="nt")


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
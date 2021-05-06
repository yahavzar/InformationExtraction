import rdflib
import lxml.html
import requests
import sys

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
        res = requests.get(WIKI_PREFIX + link)
        doc = lxml.html.fromstring(res.content)
        infobox = doc.xpath("//table[contains(@class, 'infobox')]")
        create_directors(graph, infobox, movie)
        create_producers(graph, infobox, movie)
        create_actors(graph, infobox, movie)
        create_length(graph, infobox, movie)
        create_based_on(graph, infobox, movie)
        create_released_date(graph, infobox, movie)
    for link in DIRECTORS_URL:
        res = requests.get(WIKI_PREFIX + link)
        doc = lxml.html.fromstring(res.content)
        infobox = doc.xpath("//table[contains(@class, 'infobox')]")
        create_occupartion(graph,link,infobox)
        create_birthday(graph,link,infobox)
    for link in PRODUCERS_URL:
        res = requests.get(WIKI_PREFIX + link)
        doc = lxml.html.fromstring(res.content)
        infobox = doc.xpath("//table[contains(@class, 'infobox')]")
        create_occupartion(graph,link,infobox)
        create_birthday(graph,link,infobox)
    for link in ACTORS_URL:
        res = requests.get(WIKI_PREFIX + link)
        doc = lxml.html.fromstring(res.content)
        infobox = doc.xpath("//table[contains(@class, 'infobox')]")
        create_occupartion(graph,link,infobox)
        create_birthday(graph,link,infobox)
    graph.serialize("ontology.nt", format="nt")


def question(q,ontology):
    '''

    :param q - question:
    :param ontology:
    :return: print answer to question using ontology
    '''
    g = rdflib.Graph()
    g.parse(ontology, format="nt")
    if "directed" in q :
        film = (q.split("directed")[1:])[0].split("?")[0:][0].strip().replace(" ","_")

        query = "select ?p                 where{<http://example.org/" + film + "> <http://example.org/Directed_by> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "produced" in q :
        film = (q.split("produced")[1:])[0].split("?")[0:][0].strip().replace(" ","_")

        query = "select ?p                 where{<http://example.org/" + film + "> <http://example.org/Produced_by> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "long is" in q:
        film = (q.split("long is")[1:])[0].split("?")[0:][0].strip().replace(" ", "_")

        query = "select ?p                 where{<http://example.org/" + film + "> <http://example.org/Running_time> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "starred in" in q:
        film = (q.split("starred in")[1:])[0].split("?")[0:][0].strip().replace(" ", "_")

        query = "select ?p                 where{<http://example.org/" + film + "> <http://example.org/Starring> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "released" in q:
        film = (q.split("When was")[1:])[0].split("released")[0:][0].strip().replace(" ", "_")
        query = "select ?p                 where{<http://example.org/" + film + "> <http://example.org/released_date> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "born" in q:
        person = (q.split("When was")[1:])[0].split("born")[0:][0].strip().replace(" ", "_")
        query = "select ?p                 where{<http://example.org/" + person + "> <http://example.org/born_at> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "occupation" in q:
        person = (q.split("occupation of")[1:])[0].split("?")[0:][0].strip().replace(" ", "_")
        query = "select ?p                 where{<http://example.org/" + person + "> <http://example.org/occupartion> ?p . }"
        result = list(g.query(query))
        result.sort()
        parse_result(result)
        return
    if "based on a book" in q:
        film = (q.split("Is")[1:])[0].split("based")[0:][0].strip().replace(" ", "_")
        query = "select ?p                 where{<http://example.org/" + film + ">  <http://example.org/Based_on> ?p . }"
        result = list(g.query(query))
        if len(result)>0:
            print("Yes")
        else:
            print("No")
        return
    if "star in" in q:
        person = (q.split("Did")[1:])[0].split("star")[0:][0].strip()
        film = (q.split("star in")[1:])[0].split("?")[0:][0].strip().replace(" ", "_")
        query = "select ?p              where{ <http://example.org/" + film + "> <http://example.org/Starring> ?p . }"
        result = list(g.query(query))
        new_result=[]
        for i in range(len(result)):
            new_result.append(
                str(result[i]).replace("(rdflib.term.URIRef('http://example.org/", "").replace("'),)", "").replace("_"," "))
        if person in new_result:
            print("Yes")
        else:
            print("No")
        return
    if "based on books" in q:
        query = "select distinct ?f                 where{?f  <http://example.org/Based_on> ?b . }"
        result = list(g.query(query))
        print(len(result))
        return
    if "won an academy award" in q:
        person = (q.split("starring")[1:])[0].split("won an academy")[0:][0].strip().replace(" ", "_")
        query = "select ?f                where{ ?f  <http://example.org/Starring> <http://example.org/"+ person +"> . }"
        result = list(g.query(query))
        print(len(result))
        return
    if "are also" in q:
        occupation1 = (q.split("How many")[1:])[0].split("are also")[0:][0].strip().replace(" ", "_")
        occupation2 = (q.split("are also")[1:])[0].split("?")[0:][0].strip().replace(" ", "_")
        query = "select ?p                 where{ ?p <http://example.org/occupartion> <http://example.org/"+occupation1+">  ." \
                                                 "?p <http://example.org/occupartion> <http://example.org/"+occupation2+"> .}"
        result = list(g.query(query))
        result.sort()
        print(len(result))
        return

def parse_result(result):
    '''
    :param result:
    :return: print result in format.
    '''
    for i in range(len(result)):
        print(
            str(result[i]).replace("(rdflib.term.URIRef('http://example.org/", "").replace("'),)", "").replace("_",
                                                                                                               " "),
            end="")
        if i < len(result) - 1:
            print(", ", end="")

def create_occupartion(graph,link,infobox):
    '''

    :param graph:
    :param link:
    :param infobox
    :return: update graph with Relation
    '''
    occupartion_is = rdflib.URIRef(EXAMPLE_PREFIX + 'occupartion')
    occupartions = Occupartion_info(infobox)
    people = rdflib.URIRef(EXAMPLE_PREFIX+create_name(link))
    if occupartions!=None:
        for occupartion in occupartions:
            if occupartion!= ', ':
                occupartion_o = rdflib.URIRef(EXAMPLE_PREFIX + occupartion.strip().replace(" ", "_"))
                graph.add((people, occupartion_is, occupartion_o))


def Occupartion_info(infobox):
    '''

       :param infobox of movie
       :return: xpath human
       '''
    occupartions = []
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
        for i in range(len(occupartions)):
            occupartions[i]=occupartions[i].lower()
        new=[]
        for i in range(len(occupartions)):
            new+=occupartions[i].replace("•",",").split(",")
        return new

def create_birthday(graph,link,infobox):
    '''

    :param graph of ontology
    :param link of person
    :param infobox of person
    :return: update graph with Relation
    '''
    born_at = rdflib.URIRef(EXAMPLE_PREFIX + 'born_at')
    Birthday = BirthDay_info(infobox)
    people = rdflib.URIRef(EXAMPLE_PREFIX+create_name(link))
    if Birthday!=None:
        for occupartion in Birthday:
            if occupartion!= ', ':
                date = rdflib.URIRef(EXAMPLE_PREFIX + occupartion.strip().replace(" ", "_"))
                graph.add((people, born_at, date))


def BirthDay_info(infobox):
    '''
       :param infobox of person
       :return: xpath human
       '''
    Birthday = []
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


def create_directors(graph,infobox,movie):
    '''

    :param graph:
    :param infobox:
    :param movie:
    :return: update graph with Relation
    '''
    Directed_by = rdflib.URIRef(EXAMPLE_PREFIX + 'Directed_by')
    directors = director_info(infobox)
    for director in directors:
        director_o = rdflib.URIRef(EXAMPLE_PREFIX + director.strip().replace(" ", "_"))
        graph.add((movie, Directed_by, director_o))

def director_info(infobox):
    '''

    :param infobox of movie
    :return: xpath result
    '''
    directors=[]
    global DIRECTORS_URL
    global ACTORS_URL
    global PRODUCERS_URL
    if infobox !=[]:
        directors = infobox[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/@title |"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/@title|"
                                     "//table//th[contains(text(), 'Directed by')]/../td[text() !=' ']/text()"
                                     )
        director=infobox[0].xpath( "//table//th[contains(text(), 'Directed by')]/../td/a/@href|"
                                   "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/@href")
        for d in director:
            if d not in DIRECTORS_URL and d not in ACTORS_URL and d not in PRODUCERS_URL:
                DIRECTORS_URL.append(d)
    return directors

def create_actors(graph,infobox,movie):
    '''

    :param graph:
    :param infobox:
    :param movie:
    :return: update graph with Relation
    '''
    Starring = rdflib.URIRef(EXAMPLE_PREFIX + 'Starring')
    actors = actor_info(infobox)
    for actor in actors:
        actor_o = rdflib.URIRef(EXAMPLE_PREFIX + actor.strip().replace(" ", "_"))
        graph.add((movie, Starring, actor_o))

def actor_info(infobox):
    '''

    :param infobox of movie
    :return: xpath result
    '''
    actors=[]
    global ACTORS_URL
    global DIRECTORS_URL
    global PRODUCERS_URL
    if infobox !=[]:
        actors = infobox[0].xpath("//table//th[contains(text(), 'Starring')]/../td/a/@title |"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/a/@title|"
                                     "//table//th[contains(text(), 'Starring')]/../td[text() !=' ']/text()"
                                     )
        actor=infobox[0].xpath("//table//th[contains(text(), 'Starring')]/../td/a/@href|"
                                     "//table//th[contains(text(), 'Starring')]/../td/div/ul/li/a/@href")

        for a in actor:
            if a not in ACTORS_URL and a not in DIRECTORS_URL and a not in PRODUCERS_URL:
                ACTORS_URL.append(a)
    return actors

def create_producers(graph,infobox,movie):
    '''

    :param graph:
    :param infobox:
    :param movie:
    :return: update graph with Relation
    '''
    producer_by = rdflib.URIRef(EXAMPLE_PREFIX + 'Produced_by')
    producers = producer_info(infobox)
    for producer in producers:
        producer_o = rdflib.URIRef(EXAMPLE_PREFIX + producer.strip().replace(" ", "_"))
        graph.add((movie, producer_by, producer_o))

def producer_info(infobox):
    '''

    :param infobox of movie
    :return: xpath result
    '''
    producers=[]
    global PRODUCERS_URL
    if infobox !=[]:
        producers = infobox[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/@title |"
                                     "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/@title|"
                                     "//table//th[contains(text(), 'Produced by')]/../td[text() !=' ' and text() !=': ']/text()"
                                     )
        producer= infobox[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/@href|"
                                   "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/@href")
        for p in producer:
            if p not in ACTORS_URL and p not in DIRECTORS_URL and p not in PRODUCERS_URL:
                PRODUCERS_URL.append(p)

    return producers




def create_released_date(graph,infobox,movie):
    '''

    :param graph:
    :param infobox:
    :param movie:
    :return: update graph with Relation
    '''
    released_date = rdflib.URIRef(EXAMPLE_PREFIX + 'released_date')
    dates = release_date_info(infobox)
    for date in dates:
        date_o = rdflib.URIRef(EXAMPLE_PREFIX + date.strip().replace(" ", "_"))
        graph.add((movie, released_date, date_o))

def release_date_info(infobox):
    '''

    :param infobox of movie
    :return: xpath result
    '''
    dates=[]
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


def create_based_on(graph,infobox,movie):
    '''

    :param graph:
    :param infobox:
    :param movie:
    :return: update graph with Relation
    '''
    based_on = rdflib.URIRef(EXAMPLE_PREFIX + 'Based_on')
    books = book_info(infobox)
    for book in books:
        book_o = rdflib.URIRef(EXAMPLE_PREFIX + (book.replace(" ", "_").strip()).replace('"',""))
        graph.add((movie, based_on, book_o))

def book_info(infobox):
    '''

    :param infobox of movie
    :return: xpath result
    '''
    books=[]
    if infobox !=[]:
        books = infobox[0].xpath("//table//th[contains(text(), 'Based on')]/../td/i/a/@title |"
                                     "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/text()|"
                                     "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/a/@title|"
                                     "//table//th[contains(text(), 'Based on')]/../td[text() !=' ']/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/a/@title|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/i/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/i/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/i/text()|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/a/@title|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/div/a/@title | "
                                 "//table//th[contains(text(), 'Based on')]/../td/div/a/@title|"
                                 "//table//th[contains(text(), 'Based on')]/../td/div/ul/li/div/i/a/@title")

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


def create_length(graph,infobox,movie):
    '''

    :param graph:
    :param infobox:
    :param movie:
    :return: update graph with Relation
    '''
    Running_time = rdflib.URIRef(EXAMPLE_PREFIX + 'Running_time')
    lentgth = length_info(infobox)
    for l in lentgth:
        length_o = rdflib.URIRef(EXAMPLE_PREFIX + l.strip().replace(" ", "_"))
        graph.add((movie, Running_time, length_o))

def length_info(infobox):
    '''

    :param infobox of movie
    :return: xpath result
    '''
    lentgth=[]
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
    name = link.split("wiki/")[1].strip().replace(" ", "_")
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
    args = sys.argv
    if len(args)<2 or len(args)>3:
        print("invalid number of args - try again")
    else:
        if args[1]=="question":
            ontology='ontology.nt'
            question(args[2],ontology)
        elif args[1]== "create":
            create_ontology()
        else:
            print("invalid command - try again.")

    #checkAll()
    #check_perosons()
    #="Is The Brave (2012 film) based on a book?"
    #question(q,ontology)
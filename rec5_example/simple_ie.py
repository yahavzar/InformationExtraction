import requests
import lxml.html
import rdflib

WIKI_PREFIX = "http://en.wikipedia.org"
EXAMPLE_PREFIX = "http://example.org"
BORN_IN = rdflib.URIRef(f'{EXAMPLE_PREFIX}/born_in')
POSITION = rdflib.URIRef(f'{EXAMPLE_PREFIX}/position')
DOB = rdflib.URIRef(f'{EXAMPLE_PREFIX}/dob')
LOCATED_IN = rdflib.URIRef(f'{EXAMPLE_PREFIX}/located_in')


def get_player_info(url, graph):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    a = doc.xpath("//table[contains(@class, 'infobox')]")
    name = a[0].xpath("//caption//text()")[0].replace(" ", "_")
    ont_name = rdflib.URIRef(f'{EXAMPLE_PREFIX}/{name}')

    b = a[0].xpath("//table//th[contains(text(), 'Date of birth')]")
    dob = b[0].xpath("./../td//span[@class='bday']//text()")[0].replace(" ", "_")
    ont_dob = rdflib.URIRef(f'{EXAMPLE_PREFIX}/{dob}')

    c = a[0].xpath("//table//th[contains(text(), 'Place of birth')]")
    pob = c[0].xpath("./../td//a/text()")[0].replace(" ", "_")
    pob_link = c[0].xpath("./../td//a/@href")[0]
    ont_pob = rdflib.URIRef(f'{EXAMPLE_PREFIX}/{pob}')

    d = a[0].xpath("//table//th[contains(text(), 'Position(s)')]")
    pos = d[0].xpath("./../td//a/text()")[0].replace(" ", "_")
    ont_pos = rdflib.URIRef(f'{EXAMPLE_PREFIX}/{pos}')

    graph.add((ont_name, BORN_IN, ont_pob))
    graph.add((ont_name, DOB, ont_dob))
    graph.add((ont_name, POSITION, ont_pos))
    print(f"{name}: {dob}, {pob}, {pos}, {pob_link}")

    # get_city_info(f"{WIKI_PREFIX}/{pob_link}", graph)


def get_city_info(url, graph):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    a = doc.xpath("//table[contains(@class, 'infobox')]")
    city = a[0].xpath("//th[1]//text()")[0].replace(" ", "_")

    b = a[0].xpath(".//th[contains(text(), 'Country')]")
    country = b[0].xpath("./../td//text()")[0].replace(" ", "_")

    ont_city = rdflib.URIRef(f"{EXAMPLE_PREFIX}/{city}")
    ont_country = rdflib.URIRef(f"{EXAMPLE_PREFIX}/{country}")
    graph.add((ont_city, LOCATED_IN, ont_country))
    print(city + " " + country)


g = rdflib.Graph()
get_player_info(f"{WIKI_PREFIX}/wiki/Kirill_Nababkin", g)
get_player_info(f"{WIKI_PREFIX}/wiki/Cristiano_Ronaldo", g)
get_player_info(f"{WIKI_PREFIX}/wiki/Lionel_Messi", g)
g.serialize("players.nt", format="nt")

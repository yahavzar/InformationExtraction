import rdflib

g = rdflib.Graph()
president_of = rdflib.URIRef('http://example.org/president_of')
born_in = rdflib.URIRef('http://example.org/born_in')

poland = rdflib.URIRef('http://example.org/Poland')
israel = rdflib.URIRef('http://example.org/Israel')

rivlin = rdflib.URIRef('http://example.org/Reuven_Rivlin')
peres = rdflib.URIRef('http://example.org/Shimon_Peres')

g.add((rivlin, president_of, israel))
g.add((rivlin, born_in, israel))
g.add((peres, president_of, israel))
g.add((peres, born_in, poland))

g.serialize("graph.nt", format="nt")



q = "select ?x where " \
    "{ ?x <http://example.org/president_of> ?y ." \
    " ?x <http://example.org/born_in> ?y " \
    "}"
x = g.query(q)
print(list(x))

# g1 = rdflib.Graph()
# g1.parse("graph.nt", format="nt")
# x1 = g1.query(q)
# print(list(x1))

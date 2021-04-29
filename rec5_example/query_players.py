import rdflib
q = "select ?p ?c where {" \
    " ?p <http://example.org/born_in> ?c ." \
    " ?p <http://example.org/position> <http://example.org/Forward>. " \
    "}"

g1 = rdflib.Graph()
g1.parse("players.nt", format="nt")

x1 = g1.query(q)
for result in x1:
    print(result)


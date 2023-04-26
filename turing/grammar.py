import nltk


def test_grammar(grammar, test_set):
    G = nltk.CFG.fromstring(grammar)
    P = nltk.ChartParser(G)
    test_results = []
    for i in test_set:
        i = list(i)
        test_results.append(len(list(P.parse(i))) > 0)
    return G, P, list(zip(test_set, test_results))

from Levenshtein import distance


def EditDistance(source, target):
    return (1-distance(source, target)/len(source))*100

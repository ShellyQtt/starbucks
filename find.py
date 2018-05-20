from calculate import calcDistance,calcRelativity,calcReverseDistance
import heapq
def findTopK(file, longitude, latitude, topK):
    file['Distance'] = file.apply(
        lambda x:calcDistance(longitude, latitude, x.Longitude, x.Latitude),
                              axis=1)

    return file.nsmallest(topK, 'Distance')

def findRange(file, longitude, latitude, range):
    file['Distance'] = file.apply(
        lambda x: calcDistance(longitude, latitude, x.Longitude, x.Latitude),
        axis=1)

    return file[file['Distance'] <= range]

def findTopKWithKeyWord(file, longitude, latitude, topK, keyWord, data):
    file['Distance'] = file.apply(
        lambda x: calcReverseDistance(longitude, latitude, x.Longitude, x.Latitude),
        axis=1)

    file['Relativity'] = calcRelativity(file, keyWord, data)
    return file.sort_values(by=['Relativity', 'Distance'], ascending=False).head(topK)

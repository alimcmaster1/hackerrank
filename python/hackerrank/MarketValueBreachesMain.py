from statistics import mean
from Market import Market

TOLERANCE = 0.35


def numberOfBreaches(input):

    def parseData(input):

        """Parse input and return a dict keyed by hour containing a sorted dict keyed by day
           Since we only compare data points from same hr there is not benefit in sorting first dict"""
        hourToDayMtkData = {}

        for marketData in input:
            marketData = Market(*marketData.split(","))
            hour = marketData.hour
            if marketData.hour not in hourToDayMtkData.keys():
                hourToDayMtkData[hour] = {marketData.dayOfMonth: marketData}
            else:
                if marketData.dayOfMonth not in hourToDayMtkData[hour].keys():
                    hourToDayMtkData[hour].update({marketData.dayOfMonth: marketData})
                # It is possible to have 0, 1, or more than 1 row of input for a given combination of hour of day and day of month. If there is more than 1 row,
                #  the net (ie. total) value of the assets for that hour and day should be calculated.
                else:
                    currentAssetVal = hourToDayMtkData[hour][marketData.dayOfMonth].marketValue
                    netAstVal = marketData.marketValue + currentAssetVal
                    hourToDayMtkData[hour][marketData.dayOfMonth] = Market(netAstVal,
                                                                           hour,
                                                                           marketData.dayOfMonth)
        return hourToDayMtkData

    def findBreaches(mktData):
        breachCount = 0
        for dayPoint in mktData:
            pastValues = []
            for day in mktData[dayPoint].keys():
                # Ensure we only ever have 3 elements to compare
                if len(pastValues) > 3:
                    del pastValues[0]
                todayMktValue = mktData[dayPoint][day].marketValue
                if len(set(pastValues).intersection(set(range(day-3, day+1, 1)))) > 2:
                    mktStatesinPastVals = filter(lambda x: x[1].dayOfMonth in pastValues, mktData[dayPoint].items())
                    meanAssetValue = mean(list(map(lambda mv: mv[1].marketValue, mktStatesinPastVals)))
                    upperBound = meanAssetValue * (1 + TOLERANCE)
                    lowerBound = meanAssetValue * (1 - TOLERANCE)
                    if not lowerBound <= todayMktValue <= upperBound:
                        breachCount += 1
                pastValues.append(day)
        return breachCount

    hourToDayMtkData = parseData(input)
    return findBreaches(hourToDayMtkData)

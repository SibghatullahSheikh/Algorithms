# Metrics to measure how close two items are:
# ~1: very close
# ~0: very distant
try:
    from numpy import array
    from numpy.linalg import norm
    from scipy.stats import pearsonr
    
    def euclidean_metric(X, Y):
        return 1.0 / (1.0 + norm(array(X) - array(Y)))
    
    def pearson_metric(X, Y):
        return pearsonr(array(X), array(Y))[0]

except ImportError:
    from math import sqrt
    
    def euclidean_metric(X, Y):
        sum_of_squares=sum([(x - y)**2 for x, y in zip(X, Y)])
        # we can remove the "sqrt" because we are not interested in the absolute
        # values, but in the comparisons among them
        return 1.0 / (1.0 + (sum_of_squares))
    
    def pearson_metric(X, Y):
        sumX = sum(X)
        sumY = sum(Y)
        
        sumXSq = sum([x**2 for x in X])
        sumYSq = sum([y**2 for y in Y])
        
        pSum = sum([x*y for x, y in zip(X, Y)])
        
        n = float(len(X))
        den = sqrt((sumXSq - sumX**2 / n) * (sumYSq - sumY**2 / n))
        if den == 0: return 0
        
        return (pSum - (sumX * sumY / n)) / den

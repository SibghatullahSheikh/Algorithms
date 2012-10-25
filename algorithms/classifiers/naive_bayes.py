from collections import Counter


class Class:
    def __init__(self, name, base_prob):
        self.name = name
        
        # P(C): Prior probability of this class
        self.prior = 0.0
        
        # P(f|C): probability of feature f within this class
        self.feature_prob = {}
        self.base_prob = base_prob
    
    def P(self, f):
        return self.feature_prob.get(f, self.base_prob)
    
    def __str__(self):
        return '[%s] P(C)=%.4f P(f|C)=%s' % (self.name, self.prior, self.feature_prob)


class ClassCounter:
    def __init__(self, name):
        self.name = name
        
        self.num_items = 0              # P(C)  : tot items of class C
        
        self.features_count = Counter() # P(f|C): tot appearances of feature f in items of class C
        self.num_features = 0           # P(f|C): tot features appearances in items of class C
    
    def __str__(self):
        return '[%s] (%d) features in (%d) items: %s' % (self.name, self.num_features, self.num_items, self.features_count)


class Model:
    """
    P(C|f) = P(f|C) * P(C) / P(f)
    
               (tot items of class C) + k
    P(C) = -------------------------------------
           (tot items) + k * (number of classes)
    
    k: smoothing parameter
    
                        (tot appearances of feature f in items of class C) + k
    P(f|C) = ---------------------------------------------------------------------------------------------------- 
             (tot features appearances in items of class C) + k * (different types of features among all classes)
    
    Smoothing is particularly useful to provide an estimate, different from 0,
    for features that have never been observed in the training set for a given class:
    
                                                                      k
    Base Probability = ----------------------------------------------------------------------------------------------------
                       (tot features appearances in items of class C) + k * (different types of features among all classes)
    
    The training set should have the following format:
    data = (
        ("class_name_1", (
            (f1, f2, ..., fn), # item 1 of class "class_name_1"
            (f1, f2, ..., fn), # item 2 of class "class_name_1"
            ...
        )),
        ("class_name_2", (
            (f1, f2, ..., fn), # item 1 of class "class_name_2"
            (f1, f2, ..., fn), # item 2 of class "class_name_2"
            ...
        )),
        ...
    )
    """
    def __init__(self, data, k=1):
        # keep count of all the different types of features among all the classes
        features_count = set([])
        class_counters = []
        tot_items = 0
        for class_name, class_data in data:
            class_counter = ClassCounter(class_name)
            class_counters.append(class_counter)
            for item in class_data:
                tot_items += 1
                class_counter.num_items += 1
                for feature in item:
                    features_count.add(feature)
                    class_counter.features_count[feature] += 1
                    class_counter.num_features += 1
        
        self.classes = {}
        self.features_num = len(features_count)
        k = float(k)
        for class_counter in class_counters:
            norm = float(class_counter.num_features + k * self.features_num)
            model_class = Class(class_counter.name, k / norm)
            model_class.prior = float(class_counter.num_items + k) / float(tot_items + k*len(class_counters))
            for feature, count in class_counter.features_count.iteritems():
                model_class.feature_prob[feature] = float(count + k) / norm
            self.classes[class_counter.name] = model_class
    
    def __str__(self):
        return '\n'.join(map(str, self.classes.values()))


class ClassProb:
    def __init__(self, model_class):
        self.model_class = model_class
        self.prob = model_class.prior
    
    def __cmp__(self, other):
        return cmp(self.prob, other.prob)


class Classifier:
    def __init__(self, model=None):
        self.model = model
    
    def train(self, data):
        self.model = Model(data)
    
    def get_probabilities(self, item):
        if self.model is None:
            raise Exception("Unable to classify without a model")
        
        class_probs = [ClassProb(c) for c in self.model.classes.values()]
        for c in class_probs:
            for feature in item:
                # P(C|f1, f2, ...) ~ P(C) * P(f1|C) * P(f2|C) * ...
                c.prob *= c.model_class.P(feature)
        
        return class_probs
    
    def classify(self, item):
        probs = self.get_probabilities(item)
        
        # return most likely class
        probs.sort(reverse=True)
        return probs[0].name
    
    def get_normalised_probabilities(self, item):
        probs = self.get_probabilities(item)
        
        # Normalise with "total probability"
        tot_p = sum([c.prob for c in probs])
        class_probs = {}
        for c in probs:
            class_probs[c.model_class.name] = c.prob / tot_p
        return class_probs

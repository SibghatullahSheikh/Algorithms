# Examples taken from the course "Introduction to Artificial Intelligence", Sebastian Thrun and Peter Norvig:
#    https://www.ai-class.com
from nose.tools import assert_almost_equal
def verify(value, expected):
    assert_almost_equal(value, expected, places=4)


from algorithms.classifiers.naive_bayes import Model, Classifier

SPAM_DATA = (
    ("spam", (
        "offer is secret",
        "click secret link",
        "secret sports link",
    )),
    ("ham", (
        "play sports today",
        "went play sports",
        "secret sports event",
        "sports is today",
        "sports costs money",
    ))
)


def simple_tokenizer(text_data):
    return [(name, [item.split() for item in text_items]) for name, text_items in text_data]


def test_NaiveBayesClassifier_without_smoothing():
    model = Model(simple_tokenizer(SPAM_DATA), k=0)
    assert model.features_num == 12
    verify(model.classes["spam"].prior, 0.3750)
    verify(model.classes["spam"].P('secret'), 0.3333)
    verify(model.classes["ham"].P('secret'), 0.0667)
    
    classifier = Classifier(model)
    verify(classifier.get_normalised_probabilities(["sports"])["spam"], 0.1667)
    verify(classifier.get_normalised_probabilities(["secret", "is", "secret"])["spam"], 0.9615)
    verify(classifier.get_normalised_probabilities(["today", "is", "secret"])["spam"], 0)


def test_NaiveBayesClassifier_with_smoothing():
    model = Model(simple_tokenizer(SPAM_DATA), k=1)
    verify(model.classes["spam"].prior, 0.4)
    verify(model.classes["ham"].prior, 0.6)
    verify(model.classes["spam"].P('today'), 0.0476)
    verify(model.classes["ham"].P('today'), 0.1111)
    
    classifier = Classifier(model)
    verify(classifier.get_normalised_probabilities(["today", "is", "secret"])["spam"], 0.4858)

TITLE_DATA = (
    ("movie", (
        "a perfect world",
        "my perfect woman",
        "pretty woman"
    )),
    ("song", (
        "a perfect day",
        "electric storm",
        "another rainy day"
    ))
)

def test_NaiveBayesClassifier_with_smoothing_2():
    model = Model(simple_tokenizer(TITLE_DATA), k=1)
    assert model.features_num == 11
    verify(model.classes["movie"].prior, 0.5000)
    verify(model.classes["song"].prior, 0.5000)
    verify(model.classes["movie"].P('perfect'), 0.1579)
    verify(model.classes["song"].P('perfect'), 0.1053)
    verify(model.classes["movie"].P('storm'), 0.0526)
    verify(model.classes["song"].P('storm'), 0.1053)
    
    classifier = Classifier(model)
    verify(classifier.get_normalised_probabilities(["perfect", "storm"])["movie"], 0.4286)

def test_NaiveBayesClassifier_without_smoothing_2():
    model = Model(simple_tokenizer(TITLE_DATA), k=0)
    classifier = Classifier(model)
    verify(classifier.get_normalised_probabilities(["perfect", "storm"])["movie"], 0.0)




if __name__ == '__main__':
    test_NaiveBayesClassifier_without_smoothing()
    test_NaiveBayesClassifier_with_smoothing()
    
    test_NaiveBayesClassifier_with_smoothing_2()
    test_NaiveBayesClassifier_without_smoothing_2()

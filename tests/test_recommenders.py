# Examples taken from "Programming Collective Intelligence", Toby Segaran:
#    http://shop.oreilly.com/product/9780596529321.do
from nose.tools import assert_almost_equal
def verify(value, expected):
    assert_almost_equal(value, expected, places=4)

from algorithms.recommenders import PreferencesModel


USERS_RATINGS = (
    ('Lisa Rose', (
        ('Lady in the Water', 2.5), ('Snakes on a Plane', 3.5), ('Just My Luck', 3.0), ('Superman Returns', 3.5), ('You, Me and Dupree', 2.5), ('The Night Listener', 3.0)
    )),
    ('Gene Seymour', (
        ('Lady in the Water', 3.0), ('Snakes on a Plane', 3.5), ('Just My Luck', 1.5), ('Superman Returns', 5.0), ('The Night Listener', 3.0), ('You, Me and Dupree', 3.5)
    )),
    ('Michael Phillips', (
        ('Lady in the Water', 2.5), ('Snakes on a Plane', 3.0), ('Superman Returns', 3.5), ('The Night Listener', 4.0)
    )),
    ('Claudia Puig', (
        ('Snakes on a Plane', 3.5), ('Just My Luck', 3.0), ('The Night Listener', 4.5), ('Superman Returns', 4.0), ('You, Me and Dupree', 2.5)
    )),
    ('Mick LaSalle', (
        ('Lady in the Water', 3.0), ('Snakes on a Plane', 4.0), ('Just My Luck', 2.0), ('Superman Returns', 3.0), ('The Night Listener', 3.0), ('You, Me and Dupree', 2.0)
    )),
    ('Jack Matthews', (
        ('Lady in the Water', 3.0), ('Snakes on a Plane', 4.0), ('The Night Listener', 3.0), ('Superman Returns', 5.0), ('You, Me and Dupree', 3.5)
    )),
    ('Toby', (
        ('Snakes on a Plane', 4.5), ('You, Me and Dupree',1.0), ('Superman Returns',4.0)
    ))
)


def verify_ranks(ranks, expected_ranks):
    for (rank, user), (expected_rank, expected_user) in zip(ranks, expected_ranks):
        assert user == expected_user
        verify(rank, expected_rank)


if __name__ == '__main__':
    model = PreferencesModel(USERS_RATINGS)
    
    verify(model.users_similarity('Lisa Rose', 'Gene Seymour') , 0.3961)
    
    verify_ranks(model.similar_users('Toby'),
                 [(0.9912, 'Lisa Rose'), (0.9245, 'Mick LaSalle'), (0.8934, 'Claudia Puig')])
    
    verify_ranks(model.user_based_recommendations('Toby'),
                 [(3.3478, 'The Night Listener'), (2.8325, 'Lady in the Water'), (2.5310, 'Just My Luck')])
    
    verify_ranks(model.similar_items('Superman Returns'),
                 [(0.6580, 'You, Me and Dupree'), (0.4880, 'Lady in the Water'), (0.1118, 'Snakes on a Plane')])
    
    verify_ranks(model.user_recommendations('Just My Luck'),
                 [(4.0, 'Michael Phillips'), (3.0, 'Jack Matthews')])
    
    verify_ranks(model.item_based_recommendations('Toby'),
                 [(3.6100, 'Lady in the Water'), (3.5314, 'The Night Listener'), (2.9610, 'Just My Luck')])
    

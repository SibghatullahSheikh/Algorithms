from collections import defaultdict
from metrics import pearson_metric, euclidean_metric

""" Example Data:
KEYS = {
    "key 1": {"feature 1": rating_1, "feature 2": rating_2, ...},
    "key 2": {"feature 1": rating_1, "feature 2": rating_2, ...},
    ...
}
"""

def similarity(data, a, b, metric=pearson_metric):
    # Get the common subset of features
    features = set(data[a].keys()) & set(data[b].keys())
    if len(features) == 0: return 0
    
    return metric([data[a][feature] for feature in features],
                  [data[b][feature] for feature in features])


def similar_keys(data, a, metric=pearson_metric):
    scores = [(similarity(data, a, b, metric), b) for b in data.keys() if b != a]
    scores.sort(reverse=True)
    return scores


class WeightedRanking:
    def __init__(self):
        self.ranking_sum = defaultdict(float)
        self.weigth_sum  = defaultdict(float)
    
    def add_ranking(self, f, ranking, weight):
        self.ranking_sum[f] += ranking * weight
        self.weigth_sum[f] += weight
    
    def get_weighted_rankings(self):
        rankings = [(ranking / self.weigth_sum[f], f)
                    for f, ranking in self.ranking_sum.items()]
        rankings.sort(reverse=True)
        return rankings


def recommend(data, a, metric=pearson_metric):
    """
    calculate ratings for unrated features of a key as average of all the other
    ratings for that feature weighted by the similarity of the other key
    """
    wr = WeightedRanking()
    for b in data.keys():
        # only different keys
        if b == a: continue
        
        key_sim = similarity(data, a, b, metric)
        if key_sim <= 0: continue
        
        for f in data[b]:
            if f in data[a]: continue
            wr.add_ranking(f, data[b][f], key_sim)
    
    return wr.get_weighted_rankings()


def subset(results, limit):
    if limit is None: limit = len(results)
    return results[0:limit]


class PreferencesModel:
    def __init__(self, data, metric=pearson_metric):
        self.metric = metric
        
        self.users = defaultdict(dict)
        self.items = defaultdict(dict)
        for user, ratings in data:
            for item, rating in ratings:
                self.users[user][item] = rating
                self.items[item][user] = rating
        
        self.item_similars = {}
        for item in self.items.keys():
            self.item_similars[item] = self.similar_items(item, None)
    
    # User based collaborative filtering
    def users_similarity(self, user_a, user_b):
        """
        How similar are these two users?
        """
        return similarity(self.users, user_a, user_b, self.metric)
    
    def similar_users(self, user, limit=3):
        """
        Give me a list of users similar to this one.
        """
        return subset(similar_keys(self.users, user, self.metric), limit)
    
    def user_based_recommendations(self, user, limit=3):
        """
        Suggest to this user a list of items he did not rate and that he could
        like, based on the ratings of users similar to him.
        """
        return subset(recommend(self.users, user, self.metric), limit)
    
    # Item based collaborative filtering
    def items_similarity(self, item_a, item_b):
        """
        How similar are these two items?
        """
        return similarity(self.items, item_a, item_b, self.metric)
    
    def similar_items(self, item, limit=3):
        """
        Give me a list of items similar to this one.
        """
        return subset(similar_keys(self.items, item, self.metric), limit)
    
    def user_recommendations(self, item, limit=3):
        """
        Suggest a list of users that have not rated this item that could like
        it, based on the ratings of similar users.
        """
        return subset(recommend(self.items, item, self.metric), limit)
    
    def item_based_recommendations(self, user, limit=3):
        """
        Suggest to this user a list of items he did not rate and that he could
        like, based on the ratings he gave to similar to items.
        """
        user_ratings = self.users[user]
        
        wr = WeightedRanking()
        
        # items rated by this user
        for (item_a, rating) in user_ratings.items():
            
            # items similar to this one
            for (item_sim, item_b) in self.item_similars[item_a]:
                if item_b in user_ratings: continue
                wr.add_ranking(item_b, rating, item_sim)
        
        return subset(wr.get_weighted_rankings(), limit)

import csv
import sys
from leaderboard import app, load_config, update_scores
from pymongo import MongoClient

def num_above_baseline(username):
    docs = list(app.coll.find({'username': username}).sort([('_id', -1)]))

    for doc in docs:
        overall_score = 0.0
        for dset, vals in doc['dataset_scores'].items():
            overall_score += vals['score'] * app.weight[dset]
        doc['score'] = overall_score

    try:
        pos = next(i for i, doc in enumerate(docs) if doc['score'] >= 0.3702)
        docs = docs[pos:]
        return len(docs)
    except StopIteration:
        return 0

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python {} datasets.toml output.csv".format(sys.argv[0]))
        sys.exit(1)

    load_config(sys.argv[1])
    app.client = MongoClient()
    app.coll = app.client['competition']['results']

    print("Writing results to {}...".format(sys.argv[2]))
    with open(sys.argv[2], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'count-above'])
        for username in app.coll.find().distinct('username'):
            writer.writerow([username, num_above_baseline(username)])

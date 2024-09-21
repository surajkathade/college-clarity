from flask import Flask, jsonify, request
import pandas as pd
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client["college-clarity"]

# Home route
@app.route('/')
def home():
    return "Welcome to the Simple Flask API!"

@app.route('/list', methods=['POST'])
def get_preference_list():
    req = request.get_json()
    airmain = int(req['air_main'])
    airadvanced = int(req['air_advanced'])
    branches = req['branches']
    seattype = req['seattype']
    state = req['state']
    gender = 'Female-only (including Supernumerary)' if req['gender'] == 'Female' else 'Gender-Neutral'
    cutoff_coll = db["josa-cutoffs"]
    rank_coll = db["josa-master-rank-crl"]
    branch_coll = db['branches']
    branch_pipeline = [
        {
            '$match': {
                'Engineering Stream': {
                    '$in': branches
                }
            }
        }, {
            '$group': {
                '_id': None, 
                'allValuesFromBranch': {
                    '$addToSet': '$Academic Program Name'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'allValuesFromBranch': 1
            }
        }
    ]
    branch_list = list(branch_coll.aggregate(branch_pipeline))[0]['allValuesFromBranch']
    # print(branch_list)
    # query = {
    #             'Year': 2024, 
    #             'Round':1, 
    #             "Seat Type": "OPEN", 
    #             'Gender': "Gender-Neutral",
    #             'Opening Rank': {'$lte': air},
    #             'Closing Rank': {'$gte': air},
    #             'Quota': {'$ne': 'HS'}
    #         }
    pipeline = [
                    {
                        '$lookup': {
                            'from': 'institutes', 
                            'localField': 'Institute', 
                            'foreignField': 'Institute', 
                            'as': 'instituteDetails'
                        }
                    }, {
                        '$unwind': '$instituteDetails'
                    }, {
                        '$match': {
                            'Year': 2024, 
                            'Round': 1, 
                            'Seat Type': seattype, 
                            'Gender': gender,
                            'Academic Program Name': {'$in': branch_list}, 
                            '$or': [
                                {
                                    'Quota': 'HS', 
                                    'instituteDetails.State': state
                                }, 
                                { 'Quota': { '$in': ['OS', 'AI'] } }
                            ],
                            '$or': [
                                {
                                    'Closing Rank': { '$gte': airmain },
                                    'instituteDetails.Exam Category': 'JEE Main'
                                }, 
                                {
                                    'Closing Rank': { '$gte': airadvanced },
                                    'instituteDetails.Exam Category': 'JEE Advanced'
                                }
                            ],
                        }
                    },
                    {
                        '$project': {
                        '_id': 0,
                        'instituteDetails': 0
                        }
                    }
                ]
    # if 'All' not in branches:
    #     query['Academic Program Name'] = {'$in': branches}
    pref_list = pd.DataFrame(list(cutoff_coll.aggregate(pipeline)))
    # pref_list = pd.DataFrame(list(cutoff_coll.find(query,{'_id': 0})))
    pref_list['cb'] = pref_list['Institute'] + pref_list['Academic Program Name']
    rank_list = pd.DataFrame(list(rank_coll.find({},{'_id': 0, 'Institute': 1, 'Academic Program Name': 1, 'Rank': 1})))
    rank_list['cb'] = rank_list['Institute'] + rank_list['Academic Program Name']
    rank_list.drop(['Institute','Academic Program Name'],axis=1, inplace=True)
    final_list = pd.merge(pref_list, rank_list, how='inner', on=['cb'])
    final_list.sort_values('Rank', inplace=True, ascending=True)
    final_list.drop(['cb', 'Round', 'Year', 'Quota', 'Seat Type', 'Gender'],axis=1, inplace=True)
    final_list = final_list.head(50)
    final_list.reset_index(drop=True, inplace=True)
    return final_list.to_dict(orient='records'), 200

@app.route('/branches', methods=['GET'])
def get_all_branches():
    branch_coll = db["branches"]
    branch_list = branch_coll.distinct('Engineering Stream')
    sorted_list = sorted(branch_list)
    final_list = ['All']
    final_list.extend(sorted_list)
    return final_list, 200

@app.route('/seattypes', methods=['GET'])
def get_all_seattypes():
    rank_coll = db["josa-cutoffs"]
    branch_list = rank_coll.distinct('Seat Type')
    sorted_list = sorted(branch_list)
    # final_list = ['All']
    # final_list.extend(sorted_list)
    return sorted_list, 200

@app.route('/states', methods=['GET'])
def get_all_states():
    rank_coll = db["institutes"]
    branch_list = rank_coll.distinct('State')
    sorted_list = sorted(branch_list)
    sorted_list.remove('All India')
    # final_list = ['All']
    # final_list.extend(sorted_list)
    return sorted_list, 200

if __name__ == '__main__':
    app.run(debug=True)

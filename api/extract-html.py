from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import os, re

client = MongoClient('mongodb://localhost:27017/')
db = client["college-clarity"]


directory = 'data/josa'

def clean_and_convert(value):
    # Use regular expression to extract numeric part
    numeric_part = re.findall(r'\d+', value)
    if numeric_part:
        return int(numeric_part[0])
    return pd.NA

def cutoff_insertion():
    cutoff_coll = db["josa-cutoffs"]
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')

        headers = [th.text.strip() for th in table.find_all('th')]
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip the header row
            cells = tr.find_all('td')
            row = [cell.text.strip() for cell in cells]
            rows.append(row)

        df = pd.DataFrame(rows, columns=headers)
        df['Institute'] = df['Institute'].str.replace(r'\s+', ' ', regex=True)
        df['Opening Rank'] = df['Opening Rank'].apply(clean_and_convert)
        df['Closing Rank'] = df['Closing Rank'].apply(clean_and_convert)
        match = re.search(r'college-cutoffs-(\d+)-(\d+)', filename)
        df['Year'] = int(match.group(1))
        df['Round'] = int(match.group(2))

        # Display the DataFrame
        print(df)
        cutoff_coll.insert_many(df.to_dict(orient='records'))

def create_master_ranking_crl():
    cutoff_coll = db["josa-cutoffs"]
    rank_coll = db["josa-master-rank-crl"]
    rank_list = pd.DataFrame(list(cutoff_coll.find({'Year': 2024, 
                                                    'Round':5, 
                                                    "Seat Type": "OPEN", 
                                                    'Gender': "Gender-Neutral",
                                                    'Quota': {'$in': ['AI', 'OS']}},
                          {'_id': 0}).sort('Closing Rank', 1)))
    rank_list['Rank'] = rank_list['Closing Rank'].rank(ascending=True, method='min').astype(int)
    print(rank_list)
    rank_coll.insert_many(rank_list.to_dict(orient='records'))
  

def get_preference_list(air, branches):
    cutoff_coll = db["josa-cutoffs"]
    rank_coll = db["josa-master-rank-crl"]
    query = {'Year': 2024, 
                'Round':1, 
                "Seat Type": "OPEN", 
                'Gender': "Gender-Neutral",
                'Opening Rank': {'$lte': air},
                'Closing Rank': {'$gte': air},
                'Quota': {'$ne': 'HS'}
                }
    if 'All' not in branches:
        query['Academic Program Name'] = {'$in': branches}
    pref_list = pd.DataFrame(list(cutoff_coll.find(query,{'_id': 0})))
    pref_list['cb'] = pref_list['Institute'] + pref_list['Academic Program Name']
    rank_list = pd.DataFrame(list(rank_coll.find({},{'_id': 0, 'Institute': 1, 'Academic Program Name': 1, 'Rank': 1})))
    rank_list['cb'] = rank_list['Institute'] + rank_list['Academic Program Name']
    rank_list.drop(['Institute','Academic Program Name'],axis=1, inplace=True)
    final_list = pd.merge(pref_list, rank_list, how='inner', on=['cb'])
    final_list.sort_values('Rank', inplace=True, ascending=True)
    final_list.drop(['cb', 'Round', 'Year', 'Quota', 'Seat Type', 'Gender'],axis=1, inplace=True)
    final_list.reset_index(drop=True, inplace=True)
    print(final_list)

def get_all_branches():
    rank_coll = db["josa-master-rank-crl"]
    branch_list = rank_coll.distinct('Academic Program Name')
    sorted_list = sorted(branch_list)
    print(sorted_list)
    #print(len(branch_list))

def create_institute_collection():
    institute_coll = db["institutes"]
    file_path = os.path.join('data/states', 'states.csv')
    df = pd.read_csv(file_path)
    df['Exam Type'] = df['Institute'].apply(lambda val: 'JEE Advanced' if pd.Series(val).str.contains('Indian Institute', case=False).any() and not pd.Series(val).str.contains('Information', case=False).any() else 'JEE Main')
    institute_coll.insert_many(df.to_dict(orient='records'))

def create_branch_collection():
    branch_coll = db["branches"]
    file_path = os.path.join('data/branches', 'branches.csv')
    df = pd.read_csv(file_path)
    branch_coll.insert_many(df.to_dict(orient='records'))

# get_preference_list(5000, ['Computer Science and Engineering (4 Years, Bachelor of Technology)', 'Mathematics and Computing (4 Years, Bachelor of Technology)'])
# get_preference_list(5000, ['All'])
# get_all_branches()
# create_master_ranking_crl()
# create_institute_collection()
# cutoff_insertion()
create_branch_collection()




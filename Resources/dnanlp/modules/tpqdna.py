#
# Wrapper Functions for the
# Dow Jones DNA Snapshot API
#
# The Python Quants GmbH
#
import os
import json
import time
import requests
import avro.schema
import pandas as pd
from avro.io import DatumReader
from avro.datafile import DataFileReader

# snapshot planning
explain_url = 'https://api.dowjones.com/alpha/extractions/documents/_explain'

# analytics end point
analytics_url = 'https://api.dowjones.com/alpha/analytics'

# snapshot creation
snapshot_create_url = 'https://api.dowjones.com/alpha/extractions/documents/'

# snapshot extraction & download list
snapshot_extraction_list_url = 'https://api.dowjones.com/alpha/extractions/'

djdna_avro_schema = {
    "type": "record",
    "name": "Delivery",
    "namespace": "com.dowjones.dna.avro",
    "doc":
        "Avro schema for extraction content used by Dow Jones' SyndicationHub",
    "fields": [
        {"name": "an", "type": ["string", "null"]},
        {"name": "modification_datetime", "type": ["long", "null"]},
        {"name": "ingestion_datetime", "type": ["long", "null"]},
        {"name": "publication_date", "type": ["long", "null"]},
        {"name": "publication_datetime", "type": ["long", "null"]},
        {"name": "snippet", "type": ["string", "null"]},
        {"name": "body", "type": ["string", "null"]},
        {"name": "art", "type": ["string", "null"]},
        {"name": "action", "type": ["string", "null"]},
        {"name": "credit", "type": ["string", "null"]},
        {"name": "byline", "type": ["string", "null"]},
        {"name": "document_type", "type": ["string", "null"]},
        {"name": "language_code", "type": ["string", "null"]},
        {"name": "title", "type": ["string", "null"]},
        {"name": "copyright", "type": ["string", "null"]},
        {"name": "dateline", "type": ["string", "null"]},
        {"name": "source_code", "type": ["string", "null"]},
        {"name": "modification_date", "type": ["long", "null"]},
        {"name": "section", "type": ["string", "null"]},
        {"name": "company_codes", "type": ["string", "null"]},
        {"name": "publisher_name", "type": ["string", "null"]},
        {"name": "region_of_origin", "type": ["string", "null"]},
        {"name": "word_count", "type": ["int", "null"]},
        {"name": "subject_codes", "type": ["string", "null"]},
        {"name": "region_codes", "type": ["string", "null"]},
        {"name": "industry_codes", "type": ["string", "null"]},
        {"name": "person_codes", "type": ["string", "null"]},
        {"name": "currency_codes", "type": ["string", "null"]},
        {"name": "market_index_codes", "type": ["string", "null"]},
        {"name": "company_codes_about", "type": ["string", "null"]},
        {"name": "company_codes_association", "type": ["string", "null"]},
        {"name": "company_codes_lineage", "type": ["string", "null"]},
        {"name": "company_codes_occur", "type": ["string", "null"]},
        {"name": "company_codes_relevance", "type": ["string", "null"]},
        {"name": "source_name", "type": ["string", "null"]}
    ]
}


def create_snapshot(query, headers):
    ''' Specifies a DNA snapshot.
    '''
    response = requests.request(
        'POST', snapshot_create_url, data=query, headers=headers)
    response = response.json()
    print(response)
    snapshot_create_job_url = response['links']['self']
    # job_status = response['data']['attributes']['current_state']
    return snapshot_create_job_url


def run_snapshot(snapshot_url, headers):
    ''' Runs the specified DNA snapshot process.
    '''
    old_status = ''
    job_status = ''
    response = ''
    while job_status != 'JOB_STATE_DONE':
        if job_status != old_status:
            print('Job status changed:')
            print(job_status)
            if job_status == 'JOB_STATE_FAILED':
                print('Job failed')
                print(response)
                break
            old_status = job_status

        time.sleep(60)
        response = requests.request('GET', snapshot_url, headers=headers)
        response = response.json()
        job_status = response['data']['attributes']['current_state']

    snapshot_files_list = list(response['data']['attributes']['files'])
    return snapshot_files_list


def download_snapshots(snapshot_files, path, headers, verbose=True):
    ''' Downloads DNA snapshot data file-by-file given the files list.
    '''
    for download_file in snapshot_files:
        url = download_file['uri']
        if url[-5:] != '.avro':
            continue
        filename = url.split('/')[-1]
        if verbose:
            print('Downloading file {} \r'.format(filename), end='')
        download = requests.get(url, headers=headers,
                                allow_redirects=True, stream=True)
        filename = os.path.join(path, filename)
        with open(filename, 'wb') as fd:
            for chunk in download.iter_content(chunk_size=128):
                fd.write(chunk)


def avro2dataframe(path, verbose=False):
    ''' Transforms DNA snapshot data in a pandas DataFrame object.
    '''
    read_schema = avro.schema.Parse(json.dumps(djdna_avro_schema))
    file_content = list()
    files = sorted(os.listdir(path))
    for avro_file in files:
        if (os.path.isfile(os.path.join(path, avro_file)) and
                avro_file.split('.')[-1] == 'avro'):
            if verbose:
                print('Reading file {} \r'.format(avro_file), end='')
            file_path = os.path.join(path, avro_file)
            reader = DataFileReader(
                open(file_path, 'rb'), DatumReader(read_schema))
            # new_schema = reader.GetMeta('avro.schema')
            users = []
            for user in reader:
                users.append(user)
            file_content.append(users)
            reader.close()
    data = [pd.DataFrame(content) for content in file_content]
    data = pd.concat(data, ignore_index=True)
    return data

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import pandas as pd
from tqdm import tqdm

es = Elasticsearch(hosts=['http://localhost:9200'], timeout=100)

schema = {
    "mappings": {
        "properties": {
            "product_name": {"type": "text"},
            "ingredient": {"type": "text"},
            "feature": {"type": "text"},
            "skin_type": {"type": "text"},
            "capacity": {"type": "text"},
            "design": {"type": "text"},
            "brand": {"type": "text"},
            "expiry": {"type": "text"},
            "origin": {"type": "text"},
            "product_id": {"type": "text"},
            "shop_id": {"type": "text"},
            "type": {"type": "text"},
            "skin_kind": {"type": "text"},
            "is_5_star": {"type": "float"},
            "num_sold_time": {"type": "float"}
        }
    }
}
es.indices.delete(index='ner_shopee')
es.indices.create(index='ner_shopee', body=schema)

df = pd.read_csv('/dataset/attribute_text_filtering.csv')
df['index'] = df['product_id']
df.fillna('', inplace=True)

def gen_data():
    for i, row in tqdm(df.iterrows(), total=len(df)):
        data = row.to_dict()
        data.pop('index', None)
        yield {
            "_index": 'ner_shopee',
            "_id": row['index'],
            "_source": data
        }


bulk(es, gen_data())

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import pandas as pd
from tqdm import tqdm

es = Elasticsearch(hosts=['http://localhost:9200'], timeout=100)

schema = {
    "mappings": {
        "properties": {
            "product_name": {"type": "dense_vector", "dims": 128,
                             "index": True, "similarity": "cosine"
                             },
            "ingredient": {"type": "dense_vector", "dims": 128,
                           "index": True, "similarity": "cosine"
                           },
            "feature": {"type": "dense_vector", "dims": 128,
                        "index": True, "similarity": "cosine"
                        },
            "skin_type": {"type": "dense_vector", "dims": 64,
                          "index": True, "similarity": "cosine"
                          },
            "capacity": {"type": "dense_vector", "dims": 64,
                         "index": True, "similarity": "cosine"
                         },
            "design": {"type": "dense_vector", "dims": 64,
                       "index": True, "similarity": "cosine"
                       },
            "brand": {"type": "dense_vector", "dims": 64,
                      "index": True, "similarity": "cosine"
                      },
            "expiry": {"type": "dense_vector", "dims": 64,
                       "index": True, "similarity": "cosine"
                       },
            "origin": {"type": "dense_vector", "dims": 64,
                       "index": True, "similarity": "cosine"
                       },
            "product_id": {"type": "text"},
            "shop_id": {"type": "text"},
            "type": {"type": "text"},
            "skin_kind": {"type": "text"},
            "is_5_star": {"type": "float"},
            "num_sold_time": {"type": "float"}
        }
    }
}
es.indices.delete(index='ner_shopee_embedding')
es.indices.create(index='ner_shopee_embedding', body=schema)

df = pd.read_json('/dataset/attribute_attribute_filtering.json',
                  orient='index')
df['index'] = df['product_id']
df.fillna('', inplace=True)

def gen_data():
    for i, row in tqdm(df.iterrows(), total=len(df)):
        data = row.to_dict()
        print(data)
        data.pop('index', None)
        yield {
            "_index": 'ner_shopee_embedding',
            "_id": row['index'],
            "_source": data
        }


bulk(es, gen_data())

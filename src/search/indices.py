"""Elasticsearch index mappings for products and categories."""

PRODUCTS_INDEX = "products"
CATEGORIES_INDEX = "categories"

PRODUCTS_MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20,
                },
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer",
                        "autocomplete_filter",
                    ],
                },
                "autocomplete_search": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                },
            },
        },
    },
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "name": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search",
                "fields": {"keyword": {"type": "keyword"}},
            },
            "name_ru": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search",
            },
            "name_kk": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search",
            },
            "description": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "description_ru": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "description_kk": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "slug": {"type": "keyword"},
            "price": {"type": "integer"},
            "category_id": {"type": "integer"},
            "category_slug": {"type": "keyword"},
            "category_name": {"type": "text"},
        },
    },
}

CATEGORIES_MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20,
                },
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer",
                        "autocomplete_filter",
                    ],
                },
                "autocomplete_search": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                },
            },
        },
    },
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "name": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search",
                "fields": {"keyword": {"type": "keyword"}},
            },
            "name_ru": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search",
            },
            "name_kk": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "autocomplete_search",
            },
            "slug": {"type": "keyword"},
        },
    },
}

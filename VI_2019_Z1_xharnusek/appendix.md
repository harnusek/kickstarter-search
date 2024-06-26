# Mapping
```
PUT http://localhost:9200/kick
{
    "settings":{
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
   "mappings":{
      "properties":{
         "url":{
            "type":"keyword"
         },
         "title":{
            "type":"text",
            "analyzer": "english"
         },
         "description":{
            "type":"text",
            "analyzer": "english"
         },
         "state":{
            "type":"keyword"
         },
         "createdAt":{
            "type":"date",
            "format":"yyyy-MM-dd HH:mm:ss"
         },
         "deadlineAt":{
            "type":"date",
            "format":"yyyy-MM-dd HH:mm:ss"
         },
         "backersCount":{
            "type":"integer"
         },
         "currency":{
            "type":"keyword"
         },
         "pledged":{
            "type":"double"
         },
         "pledgedUSD":{
            "type":"double"
         },
         "goal":{
            "type":"double"
         },
         "location":{
            "type":"keyword"
         },
         "country":{
            "type":"keyword"
         },
         "creator":{
            "type":"keyword"
         },
         "category":{
            "type":"nested",
            "properties":{
               "name":{
                  "type":"keyword"
               }
            }
         },
         "about":{
            "type":"text",
            "analyzer": "english"
         },
         "risksAndChallenges":{
            "type":"text",
            "analyzer": "english"
         }
      }
   }
}
```

---

# Queries
## 1. Chcem nájsť všetky projekty z kategórie keramiky, ktoré nie sú z USA 
- použitie nested
Request:
```
POST http://localhost:9200/kick/_search
{ 
    "query":{ 
        "bool":{ 
            "filter":{ 
                "term":{ 
                    "country":"US"
                }
            },
            "must":[ 
                { 
                    "nested":{ 
                        "path":"category",
                        "query":{ 
                            "bool":{ 
                                "filter":{ 
                                    "term":{ 
                                        "category.name":"pottery"
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
    }
}
```

## 2. Chcem nájsť prebiehajúce projekty. Ich skóre vypočítať podľa relatívneho prekročenia cieľa. Minimum je 1 násobné prekročenie.
- použitie boost_mode
Request: 
```
POST http://localhost:9200/kick/_search
{ 
    "min_score":1,
    "query":{ 
        "function_score":{ 
            "query":{ 
                "term":{ 
                    "state":"live"
                }
            },
            "boost_mode":"replace",
            "script_score":{ 
                "script":"(((doc['pledged'].value - doc['goal'].value) + Math.abs(doc['pledged'].value - doc['goal'].value))/2)/doc['goal'].value"
            }
        }
    }
}
```

## 3. Chcem nájsť početnosť ukončených projektov z kategórie comics pre každý stav projektu.
Request: 
- použitie nested, aggs
```
POST http://localhost:9200/kick/_search?size=0
{ 
    "query":{ 
        "bool":{ 
            "must":[ 
                { 
                    "nested":{ 
                        "path":"category",
                        "query":{ 
                            "bool":{ 
                                "filter":{ 
                                    "term":{ 
                                        "category.name":"comics"
                                    }
                                }
                            }
                        }
                    }
                }
            ],
            "must_not":{ 
                "term":{ 
                    "state":"live"
                }
            }
        }
    },
    "aggs":{ 
        "states":{ 
            "terms":{ 
                "field":"state"
            }
        }
    }
}
```

## 4. Chcem nájsť prebiehajúce projekty z V. Británie, ktoré majú v texte slová "queen Victoria". Nech sú zoradené podľa najsneskôr vytvorených.
- použitie multi_match
Request: 
```
POST http://localhost:9200/kick/_search
{ 
    "query":{ 
        "bool":{ 
            "must":{ 
                "multi_match":{ 
                    "query":"queen Victoria",
                    "type":"cross_fields",
                    "fields":[ 
                        "title",
                        "description",
                        "about",
                        "risksAndChallenges"
                    ],
                    "operator":"and"
                }
            },
            "filter":[ 
                { 
                    "term":{ 
                        "state":"live"
                    }
                },
                { 
                    "term":{ 
                        "country":"GB"
                    }
                }
            ]
        }
    },
    "sort":{ 
        "createdAt":{ 
            "order":"desc"
        }
    }
}
```

## 5. Chcem nájsť priemernú vyzbieranú sumu prebiehajúcich projektov, ktoré budú končiť za 1 deň.
Request: 
- použitie range, aggs
```
POST http://localhost:9200/kick/_search?size=0
{ 
    "query":{ 
        "range":{ 
            "deadlineAt":{ 
                "gte":"now",
                "lt":"now+1d/d"
            }
        }
    },
    "aggs":{ 
        "pledgedAverage":{ 
            "avg":{ 
                "field":"pledgedUSD"
            }
        }
    }
}
```

## 6. Chcem nájsť počet úspešných projektov z V. Británie a roka 2019. Počet nech je aspoň 10.
Request: 
- použitie range, aggs
```
POST http://localhost:9200/kick/_search?size=0
{ 
    "query":{ 
        "bool":{ 
            "must":{ 
                "range":{ 
                    "createdAt":{ 
                        "gte":"2019-01-01 00:00:00"
                    }
                }
            },
            "filter":[ 
                { 
                    "term":{ 
                        "country":"GB"
                    }
                },
                { 
                    "term":{ 
                        "state":"successful"
                    }
                }
            ]
        }
    },
    "aggs":{ 
        "tags":{ 
            "terms":{ 
                "field":"location",
                "min_doc_count":10
            }
        }
    }
}
```
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
## 1. Nájdi všetky projekty z kategórie keramiky, ktoré nie sú z USA 
- použitie nested
Request:
```
POST http://localhost:9200/kick/_search
{ 
    "query":{ 
        "bool":{ 
            "filter":{ 
                "bool":{ 
                    "filter":{ 
                        "term":{ 
                            "country":"US"
                        }
                    }
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

## 2. Nájdi prebiehajúce projekty. Ich skóre vypočítaj podľa relatívneho prekročenia cieľa. Minimum je 1 násobné prekročenie.
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

## 3. 
Request: Nájdi početnosť projektov z kategórie comics pre každý stav projektu okrem prebiehajúceho.
- použitie nested, aggregations
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
    "aggregations":{ 
        "states":{ 
            "terms":{ 
                "field":"state"
            }
        }
    }
}
```

## 4. Nájdi prebiehajúce projekty z GB, v ktoré majú v texte slová "queen Victoria". Nech sú zoradené podľa najsneskôr vytvorených.
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

## 5. 
Request: Nájdi priemernú vyzbieranú sumu prebiehajúcich projektov, ktoré končia za 1 deň.
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

## 6. 
Request: Nájdi
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
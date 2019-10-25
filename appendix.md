# Mapping
```
PUT http://localhost:9200/kickstarter
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
## 1. Find projects not from US and with category=pottery
Request:
```
POST http://localhost:9200/kickstarter/_search
{ 
    "query":{ 
        "bool":{ 
            "filter":{ 
                "bool":{ 
                    "must_not":[ 
                        { 
                            "term":{ 
                                "country":"US"
                            }
                        }
                    ]
                }
            },
            "must":[ 
                { 
                    "nested":{ 
                        "path":"category",
                        "query":{ 
                            "bool":{ 
                                "must":[ 
                                    { 
                                        "term":{ 
                                            "category.name":"pottery"
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        }
    }
}
```

## 2. Find projects with state=live, ordered by how much times was goal fulfilled , minimum is 1
Request: 
```
POST http://localhost:9200/kickstarter/_search
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
Request:
```
POST http://localhost:9200/kickstarter/_search?size=0
{
    "aggs" : {
        "grades_stats" : { "stats" : { "field" : "pledgedUSD" } }
    }
}
```

## 4. 
Request:
```
POST http://localhost:9200/kickstarter/_search
```

## 5. 
Request:
```
POST http://localhost:9200/kickstarter/_search
```

## 6. 
Request:
```
POST http://localhost:9200/kickstarter/_search
```
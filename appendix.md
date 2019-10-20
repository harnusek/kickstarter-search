# Mapping
```
PUT http://localhost:9200/kickstarter
{
   "mappings":{
      "properties":{
         "url":{
            "type":"keyword"
         },
         "title":{
            "type":"text"
         },
         "description":{
            "type":"text"
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
            "type":"text"
         },
         "risksAndChallenges":{
            "type":"text"
         }
      }
   }
}
```

---

#Queries

Request: `GET http://localhost:9200/_cat/indices/kickstarter?format=json&pretty`
Response: 
```
[
  {
    "health": "yellow",
    "status": "open",
    "index": "kickstarter",
    "uuid": "kd30qWLUTjG2m2mbGm1EvA",
    "pri": "1",
    "rep": "1",
    "docs.count": "170493",
    "docs.deleted": "1",
    "store.size": "252.4mb",
    "pri.store.size": "252.4mb"
  }
]
```


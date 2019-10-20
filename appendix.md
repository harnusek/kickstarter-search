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

# Queries
## 1. Find projects not from US and with category=pottery
Request:
```
POST http://localhost:9200/kickstarter/_search
{
  "query": {
    "bool": {
      "filter": {
        "bool": {
          "must_not": [{
            "term": {
              "country": "US"
            }
          }]
        }
      },
      "must": [
        {
          "nested": {
            "path": "category",
            "query": {
              "bool": {
                "must": [{
                  "term": {
                    "category.name": "pottery"
                  }
                }]
              }
            }
          }
        }
      ]
    }
  }
}
```

## 2. Find projects with state=live, ordered boosted by how much times was goal fulfilled , minimum is 1
Request: 
```
POST http://localhost:9200/kickstarter/_search
{
  "min_score": 1,
  "query": { 
    "function_score": {
      "query": { 
        "match": {"state": "live" }
      },
      "boost_mode": "replace", 
      "script_score": {
        "script": "(((doc['pledged'].value - doc['goal'].value) + Math.abs(doc['pledged'].value - doc['goal'].value))/2)/doc['goal'].value" 
      }
    }
  }
}
```

## 3. 
Request:
```
POST http://localhost:9200/kickstarter/_search
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
# flask-mysql-jaeger
Jaeger Example with Python Flask and SQLAlchemy with MySQL

## Usage

Boot the stack:

```
$ docker-compose up --build -d
```

Make a request:

```
$ curl -s http://app.localdns.xyz/ | jq .
{
  "inventory": [
    {
      "id": 1,
      "name": "oakley",
      "category": "sunglasses"
    },
    {
      "id": 2,
      "name": "hurley",
      "category": "clothing"
    },
    {
      "id": 3,
      "name": "havianas",
      "category": "footwear"
    }
  ]
}
```

Head over to http://jaeger.localdns.xyz and view your traceid:

![image](https://user-images.githubusercontent.com/567298/113983729-90d7dd80-984a-11eb-9d51-3ba8e779e3cf.png)

You can also view the trace graph:

![image](https://user-images.githubusercontent.com/567298/113983849-b238c980-984a-11eb-8a9e-df5811a6097b.png)

As well as the trace statistics:

![image](https://user-images.githubusercontent.com/567298/113983898-c67cc680-984a-11eb-8525-facc4d120780.png)

Linking Loki: when you link the tag names in the Jaeger datasource config, in my case I set the `appname` label for my logs and tags in Jaeger, therefore I chose `appname` as a tag, then you can link your traces to logs:

![image](https://user-images.githubusercontent.com/567298/113983575-58d09a80-984a-11eb-8f12-6f00df3b9174.png)

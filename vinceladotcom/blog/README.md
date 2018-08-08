# /blog/

| URL Endpoint     | Method | Auth Required? | Description                            |
| ---------------- | ------ | -------------- | -------------------------------------- |
| `/blog/`         | GET    | N              | List the entire collection of articles |
|                  | POST   | Y              | Create an article                      |
| `/blog/new       | GET    | Y              | New page creator                       |
| `/blog/<int:id>` | GET    | Y              | Article editor                         |
|                  | PUT    | Y              | Update an article                      |
|                  | DELETE | Y              | Delete an article                      |
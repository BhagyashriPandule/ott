Project Name: Sugar Box
Application Name: ott


*API URL's:
1.Movie search:
http://127.0.0.1:8000/api/movie/<movie_name>
eg:
http://127.0.0.1:8000/api/movie/ABCD

2.User Movie Search :
http://127.0.0.1:8000/api/user/<userid>

3.Add Rating to Movie:
http://127.0.0.1:8000/api/rate/
POST DATA:
{
  "user": "1",
  "movie": "ABCD",
  "rate": 5
}

4.Add Comment to Movie:
http://127.0.0.1:8000/api/comment/
POST DATA:
{
  "user": "1",
  "movie": "ABCD",
  "comment": "great movie"
}

*Datbase dump of sqllite3 included in project with test data

*API directory in project:
sugarbox/ott/api/
# CPSC-449-Assignment-1

### Run code with: python3 gamestore.py

### Examples of CRUD commands

### Create (POST)

 - http POST http://127.0.0.1:5000/api/games title="Silent Hill" publisher="Konami" platform="PlayStation" cost=120.00 year=1999 game_id=1

### Read (GET)

 - Get all games: http GET http://127.0.0.1:5000/api/games

 - Get single game based on game_id: http GET http://127.0.0.1:5000/api/games/1

### Update (PUT)

 - http PUT http://127.0.0.1:5000/api/games/1 title="Silent Hill 2" publisher="Konami"  platform="PlayStation 2" cost=145.00 year=2001

### Delete (DELETE)

 - http DELETE http://127.0.0.1:5000/api/games/1

from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kicacho@123'
app.config['MYSQL_DB'] = 'videogamestore'

# Initialize MySQL
mysql = MySQL(app)

# Create videogames table if not exists
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABlE IF NOT EXISTS videogames (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            publisher VARCHAR(255) NOT NULL,
            platform VARCHAR(255) NOT NULL,
            cost DECIMAL(10, 2) NOT NULL,
            year INT NOT NULL,
            game_id INT NOT NULL
        )
    """)
    mysql.connection.commit()


# Insert games into the videogames table if not exists
def setup_db():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM videogames")
    num_games = cur.fetchone()[0]
    if num_games == 0: # If there are no games in the database, insert some
        initial_games = [
            ('Resident Evil 2', 'Capcom', 'PlayStation', 12.00, 1998, 22222222),
            ('Super Smash Bros. Melee', 'Nintendo', 'GameCube', 14.00, 2001, 33333333),
            ('Burnout 3: Takedown', 'EA Games', 'PlayStation 2', 16.00, 2004, 44444444)
        ]
        cur.executemany("INSERT INTO videogames (title, publisher, platform, cost, year, game_id) VALUES (%s, %s, %s, %s, %s, %s)", initial_games)
        mysql.connection.commit()
    cur.close()


# home page
@app.route('/')
def home():
    return render_template('home.html')


# redirect user to add_game.html
@app.route('/add-game', methods=['GET'])
def add_game_page():
    return render_template('add-game.html')


# redirect user to get_game.html
@app.route('/get-game', methods=['GET'])
def get_game_page():
    return render_template('get-game.html')


# redirect user to update_game.html
@app.route('/update-game', methods=['GET'])
def update_game_page():
    return render_template('update-game.html')


# redirect user to delete_game.html
@app.route('/delete-game', methods=['GET'])
def delete_game_page():
    return render_template('delete-game.html')


# Read in all of the games, return as JSON
@app.route('/api/games', methods=['GET'])
def get_games_json():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videogames")
    games = cur.fetchall()
    cur.close()
    return jsonify(games)


# Read in all of the games, render objects in browser
@app.route('/games/', methods=['GET'])
def get_games_render():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videogames")
    games = cur.fetchall()
    cur.close()
    return render_template('games.html', games=games)


# Create a game
@app.route('/api/games', methods=['POST'])
def add_game_api():
    if request.headers['Content-Type'] == 'application/json':
        # Handle data in JSON format
        data = request.json
        title = data.get('title')
        publisher = data.get('publisher')
        platform = data.get('platform')
        cost = data.get('cost')
        year = data.get('year')
        game_id = data.get('game_id')
    else:
        # handle form data
        data = request.form
        title = data.get('title')
        publisher = data.get('publisher')
        platform = data.get('platform')
        cost = data.get('cost')
        year = data.get('year')
        game_id = data.get('game_id')

    if title and publisher and platform and cost and year and game_id:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO videogames (title, publisher, platform, cost, year, game_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (title, publisher, platform, cost, year, game_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Video Game added successfully'}), 201
    else:
        return jsonify({'error': 'Required fields missing'}), 400


# Read in one game based on the game_id, return as JSON
@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game_api(game_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videogames WHERE game_id = %s", (game_id,))
    game = cur.fetchone()
    cur.close()
    if game:
        return jsonify(game)
    else:
        return jsonify({'error': 'Video Game not found'}), 404


# Read in one game based on the game_id which was obtained through a form, render in browser
@app.route('/games', methods=['GET'])
def get_game_form():
    game_id = request.args.get('game_id')

    print("TEST:",game_id)

    if game_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM videogames WHERE game_id = %s", (game_id,))
        game = cur.fetchone()
        cur.close()
        if game:
            return render_template('games.html', games=[game])
        else:
            return jsonify({'error': 'Video Game not found'}), 404
    else:
        return jsonify({'error': 'No game_id was passed'}), 400
    

# Update a game with api
@app.route('/api/games/<int:game_id>', methods=['PUT'])
#@app.route('/api/update-game/<int:game_id>', methods=['PUT'])
def update_game_api(game_id):
    data = request.json
    title = data.get('title')
    publisher = data.get('publisher')
    platform = data.get('platform')
    cost = data.get('cost')
    year = data.get('year')

    # Check if there is a game with the specified game_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videogames WHERE game_id = %s", (game_id,))
    game = cur.fetchone()
    cur.close()

    if not game:
     return jsonify({'error': f'Video Game with ID: {game_id} Does Not Exist'}), 404
    
    if title and publisher and platform and cost and year:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE videogames SET title = %s, publisher = %s, platform = %s, cost = %s, year = %s WHERE game_id = %s",
                    (title, publisher, platform, cost, year, game_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Video Game updated successfully'}), 200
    else:
        return jsonify({'error': 'Required Fields are Missing'}), 400


# Update a game with form 
@app.route('/update-game', methods=['POST'])
def update_game_form():
    data = request.form
    game_id = data.get('game_id')

    if game_id:
        title = data.get('title')
        publisher = data.get('publisher')
        platform = data.get('platform')
        cost = data.get('cost')
        year = data.get('year')

        # Check if there is a game with the specified game_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM videogames WHERE game_id = %s", (game_id,))
        game = cur.fetchone()
        cur.close()

        if game:
            if title and publisher and platform and cost and year:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE videogames SET title = %s, publisher = %s, platform = %s, cost = %s, year = %s WHERE game_id = %s",
                            (title, publisher, platform, cost, year, game_id))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message': f'Video Game with ID: {game_id}, Updated Successfully'}), 200
            else:
                return jsonify({'error': 'Required Fields are Missing'}), 400
        else:
            return jsonify({'error': f'Video Game with ID: {game_id} Does Not Exist'}), 400
    else:
        return jsonify({'error': 'Missing Game ID'}), 400


# Remove a game with api
@app.route('/api/games/<int:game_id>', methods=['DELETE'])
def delete_game_api(game_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videogames WHERE game_id = %s", (game_id,))
    game = cur.fetchone()
    cur.close()

    if game is None:
        return jsonify({'error': 'Video Game Not Found'}), 404

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM videogames WHERE game_id = %s",(game_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Video Game deleted successfully'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500


# Remove a game with form
@app.route('/delete-game', methods=['POST'])
def delete_game_form():
    data = request.form
    game_id = data.get('game_id')

    if game_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM videogames WHERE game_id = %s", (game_id,))
        game = cur.fetchone()
        cur.close()

        if game is None:
            return jsonify({'error': 'Video Game Not Found'}), 404

        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM videogames WHERE game_id = %s",(game_id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Video Game deleted successfully'}), 200
        except Exception as err:
            return jsonify({'error': str(err)}), 500
    else:
        return render_template('delete-game.html')


if __name__ == '__main__':
    with app.app_context():
        setup_db()
    app.run(debug=True)

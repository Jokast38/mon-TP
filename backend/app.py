from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import random
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)  # Activer CORS

bcrypt = Bcrypt(app)

# Configuration de la base de données
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'event_reservation'

mysql = MySQL(app)

@app.route('/evenements', methods=['GET'])
def get_evenements():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nom, date, lieu FROM evenements")
        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        results = [dict(zip(columns, row)) for row in rows]
        cur.close()
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Erreur lors de la récupération des événements : {e}")
        return jsonify({"error": "Erreur lors de la récupération des événements"}), 500

@app.route('/evenements', methods=['POST'])
def create_evenement():
    data = request.json
    cur = mysql.connection.cursor()
    try:
        # Récupérer le nombre de places, par défaut 10 si non fourni
        nombre_places = int(data.get('nombre_places', 10))
        # Créer l'événement
        cur.execute("INSERT INTO evenements (nom, date, lieu) VALUES (%s, %s, %s)",
                    (data['nom'], data['date'], data['lieu']))
        evenement_id = cur.lastrowid
        # Créer les places associées à l'événement
        for _ in range(nombre_places):
            cur.execute("INSERT INTO places (evenement_id, statut) VALUES (%s, 'libre')", (evenement_id,))
        mysql.connection.commit()
        return jsonify({"message": f"Événement créé avec succès avec {nombre_places} places"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    app.logger.info(f"Données reçues pour l'inscription : {data}")  # Debugging log

    # Validation des données
    if not data.get('nom') or not data.get('email') or not data.get('password'):
        app.logger.error("Données manquantes ou invalides")  # Debugging log
        return jsonify({"error": "Données manquantes ou invalides"}), 400

    cur = mysql.connection.cursor()
    try:
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        app.logger.info(f"Mot de passe haché : {hashed_password}")  # Debugging log

        # Insert the user into the database
        query = "INSERT INTO utilisateurs (nom, email, password) VALUES (%s, %s, %s)"
        app.logger.info(f"Requête SQL : {query} avec valeurs ({data['nom']}, {data['email']}, [hashed_password])")  # Debugging log
        cur.execute(query, (data['nom'], data['email'], hashed_password))
        mysql.connection.commit()
        app.logger.info("Utilisateur enregistré avec succès")  # Debugging log
        return jsonify({"message": "Utilisateur enregistré avec succès"}), 201
    except Exception as e:
        app.logger.error(f"Erreur lors de l'inscription : {e}")  # Debugging log
        return jsonify({"error": "Une erreur est survenue lors de l'inscription. Veuillez vérifier vos informations."}), 400
    finally:
        cur.close()

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    app.logger.info(f"Données reçues pour la connexion : {data}")  # Debugging log
    cur = mysql.connection.cursor()
    try:
        # Fetch the user by email
        cur.execute("SELECT id, password FROM utilisateurs WHERE email = %s", (data['email'],))
        user = cur.fetchone()

        if not user:
            app.logger.warning("Utilisateur introuvable")  # Debugging log
            return jsonify({"error": "Utilisateur introuvable"}), 404

        user_id, hashed_password = user

        # Verify the password
        if not bcrypt.check_password_hash(hashed_password, data['password']):
            app.logger.warning("Mot de passe incorrect")  # Debugging log
            return jsonify({"error": "Mot de passe incorrect"}), 401

        app.logger.info("Connexion réussie")  # Debugging log
        return jsonify({"message": "Connexion réussie", "user_id": user_id}), 200
    except Exception as e:
        app.logger.error(f"Erreur lors de la connexion : {e}")  # Debugging log
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    app.logger.info(f"Données reçues pour la réservation : {data}")  # Debugging log
    app.logger.info(f"Données reçues pour la réservation : utilisateur_id={data.get('utilisateur_id')}, evenement_id={data.get('evenement_id')}")

    # Vérification des données reçues
    if not data.get('utilisateur_id') or not data.get('evenement_id'):
        app.logger.error("Données manquantes ou invalides pour la réservation")  # Debugging log
        return jsonify({"error": "Données manquantes ou invalides pour la réservation"}), 400

    cur = mysql.connection.cursor()
    try:
        # Trouver une place libre pour l'événement donné
        query_find_place = "SELECT id FROM places WHERE evenement_id = %s AND statut = 'libre' LIMIT 1"
        app.logger.info(f"Requête SQL : {query_find_place} avec valeur ({data['evenement_id']})")  # Debugging log
        cur.execute(query_find_place, (data['evenement_id'],))
        place = cur.fetchone()

        # Log the result of the query to debug
        app.logger.info(f"Résultat de la requête pour les places libres : {place}")

        if not place:
            app.logger.warning("Aucune place libre disponible pour cet événement.")  # Debugging log
            return jsonify({"error": "Aucune place libre disponible pour cet événement."}), 400

        place_id = place[0]

        # Attribuer un numéro de place aléatoire entre 1 et 100
        random_numero_place = random.randint(1, 100)
        query_update_place = "UPDATE places SET statut = 'reserve', numero_place = %s WHERE id = %s"
        app.logger.info(f"Requête SQL : {query_update_place} avec valeurs ({random_numero_place}, {place_id})")  # Debugging log
        cur.execute(query_update_place, (random_numero_place, place_id))

        # Créer la réservation
        query_create_reservation = "INSERT INTO reservations (utilisateur_id, evenement_id, place_id) VALUES (%s, %s, %s)"
        app.logger.info(f"Requête SQL : {query_create_reservation} avec valeurs ({data['utilisateur_id']}, {data['evenement_id']}, {place_id})")  # Debugging log
        cur.execute(query_create_reservation, (data['utilisateur_id'], data['evenement_id'], place_id))
        mysql.connection.commit()

        app.logger.info("Réservation créée avec succès")  # Debugging log
        return jsonify({"message": "Réservation créée avec succès", "place_id": place_id, "numero_place": random_numero_place}), 201
    except Exception as e:
        app.logger.error(f"Erreur lors de la création de la réservation : {e}")  # Debugging log
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation_details(reservation_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT r.id AS reservation_id, r.utilisateur_id, r.evenement_id, p.id AS place_id, p.numero_place, p.statut
            FROM reservations r
            JOIN places p ON r.place_id = p.id
            WHERE r.id = %s
        """, (reservation_id,))
        reservation = cur.fetchone()

        if not reservation:
            return jsonify({"error": "Réservation introuvable"}), 404

        columns = [col[0] for col in cur.description]
        result = dict(zip(columns, reservation))

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@app.route('/evenements/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id, nom, date, lieu FROM evenements WHERE id = %s", (event_id,))
        event = cur.fetchone()

        if not event:
            return jsonify({"error": "Événement introuvable"}), 404

        columns = [col[0] for col in cur.description]
        result = dict(zip(columns, event))

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@app.route('/test-connexion', methods=['GET'])
def test_connexion():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return jsonify({"message": "Connexion à la base de données réussie"}), 200
    except Exception as e:
        return jsonify({"error": f"Erreur de connexion à la base de données : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
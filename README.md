# 🎟️ Event Ticket Reservation System

## 📌 Présentation

**Event Ticket Reservation System** est une application complète permettant de gérer la réservation de billets pour divers événements tels que des concerts, conférences et expositions. Ce projet met l'accent sur une expérience utilisateur fluide et une gestion efficace des ressources.

---

## 🚀 Fonctionnalités Principales

* 🎫 Réservation de billets en ligne avec attribution automatique de places
* 🪑 Gestion des places disponibles (libres/réservées)
* 🔒 Authentification sécurisée des utilisateurs avec hachage des mots de passe
* 📅 Gestion des événements (création, consultation)
* 📈 Tarification dynamique (à venir)

---

## 🏗️ Architecture du Projet

L'application est divisée en deux parties principales :

### Backend (Flask)

* API RESTful pour gérer les utilisateurs, événements et réservations
* Base de données MariaDB pour stocker les informations
* Sécurisation des mots de passe avec `bcrypt`

### Frontend (React)

* Interface utilisateur moderne et réactive
* Pages dédiées pour l'inscription, la connexion et la réservation
* Intégration avec l'API backend pour les opérations en temps réel

---

## 📁 Structure du Projet

```
backend/
├── app.py          # Application Flask avec les endpoints
├── requirements.txt # Dépendances Python
frontend/
├── src/
│   ├── pages/      # Pages React (Inscription, Connexion, etc.)
│   ├── components/ # Composants réutilisables
│   └── services/   # Gestion des appels API
```

---

## ⚙️ Installation & Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-utilisateur>/<nom-du-repo>.git
cd event-ticket-reservation
```

### 2. Installer les dépendances

#### Backend

```bash
cd backend
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

### 3. Lancer les serveurs

#### Backend

```bash
cd backend
flask run
```

#### Frontend

```bash
cd frontend
npm start
```

---

## 📊 Roadmap

* Intégration des paiements en ligne
* Génération de billets électroniques avec QR codes
* Tableau de bord analytique pour les organisateurs

---

## 🧪 Qualité du Code

* Tests unitaires pour les fonctionnalités critiques
* Respect des bonnes pratiques de développement

---

## 🪪 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de l'utiliser et de le modifier.

---

## 🙌 Contributeurs

Réalisé par : **Jokast Kassa**

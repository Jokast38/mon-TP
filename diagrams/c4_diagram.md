# Diagramme C4 - Event Ticket Reservation System

```mermaid
graph TD
    subgraph Frontend
        A[React Application]
    end

    subgraph Backend
        B[Flask API]
        B -->|Handles API Requests| DB[(MariaDB)]
    end

    subgraph Database
        DB[(MariaDB)]
        DB -->|Stores| Tables[Tables: utilisateurs, evenements, places, reservations]
    end

    A -->|Sends Requests| B
    B -->|Fetches Data| DB
```

## Description
- **Frontend** : Une application React qui gère l'interface utilisateur.
- **Backend** : Une API Flask qui gère la logique métier et les interactions avec la base de données.
- **Database** : Une base de données MariaDB qui stocke les informations des utilisateurs, événements, places et réservations.

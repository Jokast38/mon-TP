# Diagramme de Classes - Event Ticket Reservation System

```mermaid
classDiagram
    class Evenement {
        +int id
        +string nom
        +date date
        +string lieu
    }

    class Place {
        +int id
        +int numero
        +string statut
        +int evenementId
    }

    class Reservation {
        +int id
        +int utilisateurId
        +int evenementId
        +int placeId
    }

    class Utilisateur {
        +int id
        +string nom
        +string email
        +string password
    }

    Evenement "1" --> "*" Place
    Place "1" --> "1" Reservation
    Utilisateur "1" --> "*" Reservation
```

## Description
- **Evenement** : Représente un événement avec un nom, une date et un lieu.
- **Place** : Représente une place associée à un événement, avec un numéro et un statut (libre/réservée).
- **Reservation** : Représente une réservation effectuée par un utilisateur pour une place dans un événement.
- **Utilisateur** : Représente un utilisateur avec un nom, un email et un mot de passe haché.

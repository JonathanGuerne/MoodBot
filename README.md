# MoodBot
Le MoodBot est un bot discord analysant les messages envoyés sur les channels d'un serveur Discord
dans le but de trouver l'émotion de son émetteur.

Le MoodBot suit aussi l'évolution de la conversation de manière à detecter si la conversation devient tendue.
Si elle le devient, il envoi le message `Voici un clown pour détendre l'atmosphère : 🤡`.

Le MoodBot, se basant sur une librairie utilisant le machine learning, a la possibilité d'apprendre en se basant sur les réactions aux messages sur le channel.

## Analyse des messages

Pour pouvoir analyser les messages le bot utilise la librairie python `textblob`.
Cette librairie permet de créer des classifier pour d'autre langue (le français par exemple).

## Installation

1. Installer les bibliothèques necessaire (voir section Requirement).
2. Créer un fichier token contenant le token pour la connexion avec Discord.
3. Mettre les fichiers contenant les phrases.

### Requirement

| Bibliothéque | Nom du paquet | Version |
|--------------|---------------|---------|
|Discord       |`discord`      |>3.10|
|TextBlob      |`textblob`     |>3.10|


## Utilisation

### Commandes

* Voir l'émotion des utilisateurs :
`!show`
* Activer l'envoi des données de debug :
`!rate on`
* Desactiver l'envoi des données de debug :
`!rate off`
* Apprendre un phrase au bot :
`!teach phrase,pos/neg`
Par exemple : `!teach j'ai passé une bonne soirée,pos`

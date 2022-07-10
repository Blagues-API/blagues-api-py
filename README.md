# BlaguesAPI Python

Ce paquet Python fournit une interface simple pour intéragir avec [Blagues API](https://www.blagues-api.fr/).  
**Important :** Ce paquet ne fournit que des méthodes **asynchrones**.

## Installation

Vous pouvez simplement ajouter la dépendance à votre projet depuis PyPI :
```
pip install blagues-api
```

## Utilisation

Pour utiliser l'API, vous devez obtenir une clé gratuite sur le site officiel : https://www.blagues-api.fr/. Vous pourrez ensuite construire un objet `BlaguesAPI` :

```py
from blagues_api import BlaguesAPI

blagues = BlaguesAPI("VOTRE_TOKEN_ICI")
```

Toutes les méthodes excepté count renverront un objet `Blague`, qui permet d'accéder aux différentes propriétés renvoyées par l'API : `id`, `type`, `joke`, `answer`. En cas d'erreur, vous recevrez une erreur du type [`aiohttp.ClientResponseError`](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponseError).

Les différents types de blagues peuvent être représentés au choix sous forme d'un string ou d'un objet `BlagueType` (exemple: `BlagueType.GENERAL`). La liste des types disponibles est notée dans sur le site officiel.

### Blague aléatoire

```py
await blagues.random()
# Blague(id=108, type=<BlagueType.GLOBAL: 'global'>, joke="C'est l'histoire d'un poil. Avant, il était bien.", answer='Maintenant, il est pubien.')
```

Il est possible de spécifier des catégories à exclure :
```py
await blagues.random(disallow=[BlagueType.LIMIT, BlagueType.BEAUF])

# Avec des strings
await blagues.random(disallow=["limit", "beauf"])
```

### Blague aléatoire catégorisée

```py
await blagues.random_categorized(BlagueType.DEV)
# Blague(id=430, type=<BlagueType.DEV: 'dev'>, joke='De quelle couleur sont tes yeux ?', answer='#1292f4 et toi ?')

# Avec des strings
await blagues.random_categorized("dev")
```

### Blague par identifiant

```py
await blagues.from_id(20)
# Blague(id=20, type=<BlagueType.GLOBAL: 'global'>, joke="Qu'est-ce qu'un chou au milieu de l'océan ?", answer='Un chou marin.')
```

### Nombre de blagues

```py
await blagues.count()
# CountJoke(count=1730)
```

La méthode ci-dessus renverra un objet `CountJoke`, qui permet d'accéder a la propriété renvoyée par l'API : `count`. En cas d'erreur, vous recevrez une erreur du type [`aiohttp.ClientResponseError`](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponseError).

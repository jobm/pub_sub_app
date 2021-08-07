## SIMPLE PUB SUB APP

This is a simple pub sub app that wraps an algorithm that optimises routes based on
data provided. The app takes coordinates in an inbound queue and publishes optimised
route data into to an outbound queue.

### APP STRUCTURE

The app is divided into two scripts, one that publishes random long lats to an in bound queue, this app is
added in a package called `pub`. The consumer is `app.py`.

```
.
|──── pub/
|─────── __init__.py
|─────── Dockerfile
|─────── pub_coordinates.py
|──── app.py
|──── docker-compose.yml
|──── Dockerfile
|──── extensions.py
|──── ortools_utils.py
|──── tests/
|──── pytest.ini
|──── requirements.txt
```

### COMMANDS
This app can be started by simply running:
```
docker-compose up --build
```

To stop the app:
```
docker-compose down
```


### Changelog

Version 0.0.1 : initial setup
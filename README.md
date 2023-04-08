# social_network

# Docker

To run project in docker simply run:

```sh
docker-compose up -d --build
```

And then to apply migrations:

```sh
docker-compose exec main-api /bin/sh -c "python manage.py migrate"
```

Optionaly create superuser:

```sh
docker-compose exec main-api /bin/sh
python manage.py createsuperuser
<Ctrl + D>
```

To see logs:

```sh
docker-compose logs -f
```

# Run localy

Create virtual environment.

```sh
python3 -m venv venv
```

Activate it:

```sh
source venv/bin/activate
```

Install requirements:

```sh
pip install -r requirements.txt
```

Apply migrations:

```sh
cd social_network
```

```sh
python manage.py migrate
```

Run server:

```sh
python manage.py runserver
```

Optionaly create superuser:

```sh
python manage.py createsuperuser
```


# My Simple Car

## Проект в разработке

### Описание

Веб-приложение, где реализован абстрактный гараж пользователя, в который он
может добавить личный авто и информацию о нём (его характеристики), введя
VIN код авто, либо вручную, и получить помощь в его обслуживании.

Также пользователь может заполнить данные о пройденном ТО, авто документах и
подключить напоминания (на почту или в telegram) о
приближающейся дате экспирации документов или необходимом ТО.

Главный помощник в приложении – Ассистент в поиске необходимых запчастей для
выбранного авто. С его помощью есть возможность упростить мониторинг авто
форумов по теме замены/ремонта указанной пользователем запчасти для его
автомобиля, осуществить лёгкий поиск артикула и определиться с выбором
поставщика путём сравнения цен в основных маркетплейсах.

Дополнительно: после совершения покупки имеется возможность отслеживания даты
доставки, путём создания трекера, который может отслеживать статус посылки.
Сервис также может осуществить поиск ближайших к пользователю автосервисов и их
контактных данных.

Основные сайты для получения данных: Drive2.ru, Exist.ru

### Технологии

> Python3.10, FastApi, PostgreSQL, SqlAlchemy, Alembic, Beautiful Soup,
> Aiohttp, AsyncIO, Celery, Redis, Docker
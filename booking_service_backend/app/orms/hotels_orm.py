from app.models.hotel import Hotels, Rooms
from app.utils.hotel_validators import HotelsSchema, RoomsSchema, rooms_adapter, hotels_adapter
from app.settings.database import async_session_factory, async_engine
from app.orms.base_orm import BaseOrm
from sqlalchemy import select
import asyncio
from faker import Faker
import random

fake = Faker('en_US')

BANNED_COUNTRIES = [
    'Russia', 'Russian Federation', 
    'Belarus', 'Republic of Belarus'
]

class HotelsOrm(BaseOrm):

    @staticmethod
    async def new_hotel(incoming_data: dict):
        async with async_session_factory() as session:
            validated_data = HotelsSchema.model_validate(incoming_data)
            hotel = Hotels(**validated_data.model_dump())

            session.add(hotel)
            await session.commit()

    
    @staticmethod
    async def new_room(incoming_data: dict):
        async with async_session_factory() as session:
            validated_data = RoomsSchema.model_validate(incoming_data)
            room = Rooms(**validated_data.model_dump())

            session.add(room)
            await session.commit()


    @staticmethod
    async def new_hotels(incoming_data_list: list[dict]):
        async with async_session_factory() as session:
            validated_data_list = hotels_adapter.validate_python(incoming_data_list)

            hotels = [
                Hotels(**hotel.model_dump()) for hotel in validated_data_list
            ]

            session.add_all(hotels)
            await session.commit()
    

    @staticmethod
    async def new_rooms(incoming_data_list: list[dict]):
        async with async_session_factory() as session:
            validated_data_list = rooms_adapter.validate_python(incoming_data_list)

            rooms = [
                Rooms(**room.model_dump()) for room in validated_data_list
            ]

            session.add_all(rooms)
            await session.commit()



    @staticmethod
    async def generate_hotels(hotels_count: int = 500):
        hotels_data = []
        POPULAR_LOCATIONS = {
            "United States": ["New York", "Los Angeles", "Chicago", "Miami", "Las Vegas", "San Francisco", "Honolulu"],
            "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Mallorca", "Ibiza"],
            "France": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux", "Cannes"],
            "Italy": ["Rome", "Milan", "Venice", "Florence", "Naples", "Como"],
            "United Kingdom": ["London", "Edinburgh", "Manchester", "Birmingham", "Bath"],
            "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne"],
            "Japan": ["Tokyo", "Osaka", "Kyoto", "Sapporo", "Fukuoka"],
            "Turkey": ["Istanbul", "Antalya", "Ankara", "Izmir", "Cappadocia"],
            "Greece": ["Athens", "Thessaloniki", "Santorini", "Mykonos", "Rhodes"],
            "Thailand": ["Bangkok", "Phuket", "Chiang Mai", "Pattaya", "Krabi"],
            "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah"],
            "Egypt": ["Cairo", "Sharm El-Sheikh", "Hurghada", "Luxor"],
            "Portugal": ["Lisbon", "Porto", "Faro", "Sintra", "Madeira"],
            "Switzerland": ["Zurich", "Geneva", "Lucerne", "Interlaken", "Zermatt"],
            "Iceland": ["Reykjavik", "Akureyri", "Vik", "Hofn"],
            "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Gold Coast"],
            "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Quebec City"],
            "Brazil": ["Rio de Janeiro", "Sao Paulo", "Salvador"],
            "Mexico": ["Cancun", "Mexico City", "Tulum", "Guadalajara"],
            "India": ["New Delhi", "Mumbai", "Goa", "Jaipur"],
            "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen"],
            "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht"],
            "Austria": ["Vienna", "Salzburg", "Innsbruck"],
            "Sweden": ["Stockholm", "Gothenburg", "Malmo"],
            "Norway": ["Oslo", "Bergen", "Tromso"],
            "Poland": ["Warsaw", "Krakow", "Gdansk", "Wroclaw"],
            "Czech Republic": ["Prague", "Brno", "Karlovy Vary"],
            "Hungary": ["Budapest", "Debrecen"],
            "Croatia": ["Dubrovnik", "Split", "Zagreb"],
            "Vietnam": ["Ho Chi Minh City", "Hanoi", "Da Nang"],
            "Indonesia": ["Bali", "Jakarta", "Yogyakarta"]
        }

        HOTEL_TYPES = ["Hotel", "Resort", "Suites", "Inn", "Boutique", "Lodge", "Spa & Resort"]
        available_countries = list(POPULAR_LOCATIONS.keys())
        
        for _ in range(hotels_count):
            country = random.choice(available_countries)
            city = random.choice(POPULAR_LOCATIONS[country])
            
            hotel_name = f"{fake.last_name()} {random.choice(HOTEL_TYPES)}"
            
            hotels_data.append({
                "name": hotel_name,
                "country": country,
                "city": city,
                "rating": random.randint(1, 5)
            })
            
        await HotelsOrm.new_hotels(hotels_data)




    @staticmethod
    async def generate_rooms(hotel_ids: list[int], rooms_per_hotel: int = 100):
        """Генерує кімнати з реальною логікою цін, місткості та пропорцій у готелі."""
        rooms_data = []

        # 1. Задаємо реалістичний розподіл категорій на 100 кімнат
        categories_distribution = (
            ['standart'] * 60 +     # 60% фонду — стандарти
            ['superior'] * 25 +     # 25% — покращені
            ['lux'] * 12 +          # 12% — люкси
            ['presidental'] * 3     # 3% — президентські
        )

        # 2. Налаштовуємо правила для кожної категорії
        category_settings = {
            'standart': {
                'price_range': (1000, 3000),
                # Ймовірність місткості: 1 місце (30%), 2 місця (70%), 3 місця (0%)
                'capacity_weights': [0.3, 0.7, 0.0] 
            },
            'superior': {
                'price_range': (3500, 6500),
                # 1 місце (10%), 2 місця (70%), 3 місця (20%)
                'capacity_weights': [0.1, 0.7, 0.2]
            },
            'lux': {
                'price_range': (7500, 15000),
                # 1 місце (0%), 2 місця (60%), 3 місця (40%)
                'capacity_weights': [0.0, 0.6, 0.4]
            },
            'presidental': {
                'price_range': (20000, 50000),
                # Завжди просторі: 2 місця (70%), 3 місця (30%)
                'capacity_weights': [0.0, 0.7, 0.3]
            }
        }

        for hotel_id in hotel_ids:
            for category in categories_distribution:
                settings = category_settings[category]
                
                # Генеруємо ціну в рамках дозволеного діапазону для цієї категорії
                min_p, max_p = settings['price_range']
                raw_price = random.randint(min_p, max_p)
                
                # Округлюємо ціну до 50 (наприклад: 1234 -> 1250, 4112 -> 4100)
                price = round(raw_price / 50) * 50

                # Вибираємо місткість (від 1 до 3) з урахуванням заданих ймовірностей
                capacity = random.choices(
                    population=[1, 2, 3], 
                    weights=settings['capacity_weights'], 
                    k=1
                )[0]

                rooms_data.append({
                    "hotel_id": hotel_id,
                    "category": category,
                    "capacity": capacity,
                    "price_per_night": price
                })

        await HotelsOrm.new_rooms(rooms_data)
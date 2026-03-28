from app.models.booking import Bookings
from app.schemas.bookings_schemas import BookingsResponseSchema

from app.models.user import Users
from app.schemas.users_schemas import UsersResponseSchema

from app.models.hotel import Hotels, Rooms
from app.schemas.hotels_schemas import HotelsResponseSchema
from app.schemas.rooms_schemas import RoomsResponseSchema, RoomCategory

def create_booking_response(booking_obj: Bookings) -> BookingsResponseSchema:
    return BookingsResponseSchema(
        id=booking_obj.id,
        room_id=booking_obj.room_id,
        check_in=booking_obj.check_in,
        check_out=booking_obj.check_out,
        created_at=booking_obj.created_at,
        user_id=booking_obj.user_id,
        total_price=booking_obj.total_price
    )


def create_user_response(user_obj: Users) -> UsersResponseSchema:
    return UsersResponseSchema(
        id=user_obj.id, 
        full_name=user_obj.full_name, 
        phone_number=user_obj.phone_number, 
        email=user_obj.email
    )


def create_hotel_response(hotel_obj: Hotels) -> HotelsResponseSchema:
    return HotelsResponseSchema(
        id=hotel_obj.id, 
        name=hotel_obj.name, 
        country=hotel_obj.country, 
        city=hotel_obj.city, 
        rating=hotel_obj.rating
    )


def create_room_response(room_obj: Rooms) -> RoomsResponseSchema:
    return RoomsResponseSchema(
            id=room_obj.id,
            hotel_id=room_obj.hotel_id,
            capacity=room_obj.capacity,
            price_per_night=room_obj.price_per_night,
            category=RoomCategory(room_obj.category),
        )

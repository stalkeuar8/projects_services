import aiosmtplib
from email.message import EmailMessage

from app.repo.bookings_repo import AdminBookingsRepo
from app.models.booking import Bookings
from app.models.user import Users
from app.repo.users_repo import AdminUsersRepo
from app.settings.database import async_session_factory


async def send_approving_email(result: bool, booking_id: int) -> None:

    async with async_session_factory.begin() as session:
        booking: Bookings | None = await AdminBookingsRepo.admin_find_by_id(session=session, booking_id=booking_id)

        if booking:

            user: Users | None = await AdminUsersRepo.admin_find_by_id(session=session, id_to_find=booking.user_id)

            if user:
                user_email = user.email

            else:
                return
    
        else:
            return
        

    message = EmailMessage()
    message['From'] = email_settings.EMAIL
    message['To'] = user_email
    message['Subject'] = f"Booking Request Results 🏡"

    if result:
        message.set_content(f"Your booking request (№{booking_id}) has been approved! ✅\n\nWe are waiting for you! ⌛")

    else:
        message.set_content(f"Your booking request (№{booking_id}) has been rejected! ❌\n\nReason: Hotel personal reasons. Please, try later. ⌛")


    try:

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=465,
            use_tls=True,
            username=email_settings.EMAIL,
            password=email_settings.PASSWORD
        )

    except Exception as e:
        print(f"Email sending error: {e}")
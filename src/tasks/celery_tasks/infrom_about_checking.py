import asyncio
from src.api.dependencies import get_db_manager_null_pull
from src.tasks.celery_app import celery_instance


async def get_users_w_today_checkin():
    async with get_db_manager_null_pull() as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_email_to_user_w_today_checkin():
    asyncio.run(get_users_w_today_checkin())

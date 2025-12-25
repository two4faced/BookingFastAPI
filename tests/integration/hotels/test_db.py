from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title='Отель 5 звёзд', location='г. Краснодар, ул. Красная, д. 134')
    await db.hotels.add(hotel_data)
    await db.commit()

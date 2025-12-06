from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from starlette import status

from logger import logger
from .schemas import PhoneAddress, UpdatePhoneAddress
from services.redis_client import get_redis

router = APIRouter(
    prefix="/api/v1/phones",
    tags=["phones"]
)


@router.get("/{phone_number}", response_model=PhoneAddress)
async def get_phone(
        phone_number: str,
        redis: Redis = Depends(get_redis),
):
    address = await redis.get(phone_number)

    if not address:
        logger.warning(f"GET: Phone {phone_number} not found")
        raise HTTPException(status_code=404, detail="Phone not found")

    decoded_address = address.decode()
    logger.info(f"GET: Phone {phone_number} found with address {decoded_address}")
    return PhoneAddress(
        phone=phone_number,
        address=decoded_address,
    )


@router.post("/", response_model=PhoneAddress, status_code=201)
async def create_phone(
    data: PhoneAddress,
    redis: Redis = Depends(get_redis),
):
    phone_number = data.phone

    address = await redis.get(phone_number)
    if address:
        logger.warning(f"POST: Phone {phone_number} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone already exists"
        )

    await redis.set(phone_number, data.address)
    logger.info(f"POST: Created phone {phone_number} with address {data.address}")
    return data


@router.put("/{phone_number}", response_model=PhoneAddress)
async def update_phone(
        phone_number: str,
        data: UpdatePhoneAddress,
        redis: Redis = Depends(get_redis),
):
    address = await redis.get(phone_number)
    if not address:
        logger.warning(f"PUT: Phone {phone_number} not found for update")
        raise HTTPException(status_code=404, detail="Phone not found")

    await redis.set(phone_number, data.address)
    logger.info(f"PUT: Updated phone {phone_number} to address {data.address}")
    return PhoneAddress(
        phone=phone_number,
        address=data.address,
    )


@router.delete("/{phone_number}", status_code=204)
async def delete_phone(
        phone_number: str,
        redis: Redis = Depends(get_redis),
):
    address = await redis.get(phone_number)
    if not address:
        logger.warning(f"DELETE: Phone {phone_number} not found")
        raise HTTPException(status_code=404, detail="Phone not found")

    await redis.delete(phone_number)
    logger.info(f"DELETE: Phone {phone_number} deleted")
    return

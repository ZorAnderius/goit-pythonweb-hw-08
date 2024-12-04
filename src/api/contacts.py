from typing import List
from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactsResponse, UpdateContactModel, ContactsModel
from src.services.contacts import ContactsServices

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ContactsResponse], response_description="List of all contacts")
async def get_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> List[ContactsResponse]:
    contacts_service = ContactsServices(db)
    contacts = await contacts_service.get_contacts(skip, limit)
    return contacts

@router.get("/{contact_id}", response_model=ContactsResponse, response_description="Get contact by id")
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)) -> ContactsResponse:
    contacts_service = ContactsServices(db)
    contact = await contacts_service.get_contact_by_id(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactsResponse,
             status_code=status.HTTP_201_CREATED,
             response_description="Create a new contact")
async def create_contact(body: ContactsModel, db: AsyncSession = Depends(get_db)) -> Contact:
    contacts_service = ContactsServices(db)
    contact = await contacts_service.create_contact(body)
    return contact

@router.patch("/{contact_id}", response_model=ContactsResponse, response_description="Update contact by id")
async def update_contact(contact_id: int, body: UpdateContactModel, db: AsyncSession = Depends(get_db)) -> Contact:
    contacts_service = ContactsServices(db)
    contact = await contacts_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactsResponse, response_description="Delete contact by id")
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contacts_service = ContactsServices(db)
    contact = await contacts_service.delete_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
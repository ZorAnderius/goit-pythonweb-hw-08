from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactsModel


class ContactsRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_contacts(self, skip: int = 0, limit: int = 10) -> List[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        contacts = await self.session.execute(query)
        return list(contacts.scalars().all())

    async def get_contact_by_id(self, contact_id: int) -> Contact:
        query = select(Contact).where(Contact.id == contact_id)
        contact = await self.session.execute(query)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactsModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def update_contact(self, contact_id: int, body: ContactsModel) -> Contact:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int):
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.session.delete(contact)
            await self.session.commit()
        return contact
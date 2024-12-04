from typing import List, Optional
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.sql import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactsModel


class ContactsRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_contacts(self,
                           skip: Optional[int] = 0,
                           limit: Optional[int] = 10,
                           first_name: Optional[str] = None,
                           last_name: Optional[str] = None,
                           email: Optional[str] = None) -> List[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        if first_name:
            query = query.where(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.where(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.where(Contact.email.ilike(f"%{email}%"))

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

    async def get_contacts_for_weekly_birthday(self):
        today = date.today()
        next_week = today + timedelta(days=7)
        query = select(Contact).where(and_(Contact.dob >= today, Contact.dob <= next_week))
        contacts = await self.session.execute(query)
        return contacts.scalars().all()


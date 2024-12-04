from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.repository.contacts import ContactsRepository
from src.schemas import ContactsModel, UpdateContactModel


class ContactsServices:
    def __init__(self, db: AsyncSession):
        self.repository = ContactsRepository(db)

    async def get_contacts(self, skip: int = 0, limit: int = 10):
        return await self.repository.get_contacts(skip, limit)

    async def get_contact_by_id(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def create_contact(self, body: ContactsModel) -> Contact:
        return await self.repository.create_contact(body)

    async def update_contact(self, contact_id: int, body: UpdateContactModel) -> Contact:
        return await self.repository.update_contact(contact_id, body)

    async def delete_contact(self, contact_id: int):
        return await self.repository.delete_contact(contact_id)
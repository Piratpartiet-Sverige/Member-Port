import tornado.web

from app.web.handlers.base import BaseHandler
from app.database.dao.organizations import OrganizationsDao
from app.models import organization_to_json
from uuid import UUID


class APIOrganizationHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self, id: str):
        org_id = self.check_uuid(id)
        if id is None:
            return self.respond("ORGANIZATION UUID IS MISSING", 400)

        organization = await OrganizationsDao(self.db).get_organization_by_id(org_id)
        return self.respond("RETRIEVED ORGANIZATION", 200, organization_to_json(organization))

    @tornado.web.authenticated
    async def post(self):
        name = self.get_argument("name")
        description = self.get_argument("description")
        active = self.get_argument("active", False)
        active = active == 'true'

        organization = await OrganizationsDao(self.db).create_organization(name, description, active)
        return self.respond("ORGANIZATION CREATED", 200, organization_to_json(organization))

    @tornado.web.authenticated
    async def put(self, id: UUID = None):
        if id is None:
            return self.respond("ORGANIZATION UUID IS MISSING", 400)

        name = self.get_argument("name", None)
        description = self.get_argument("description", None)
        active = self.get_argument("active", False)
        active = active == 'true'

        if name is None:
            return self.respond("name property is missing", 422)
        if description is None:
            return self.respond("description property is missing", 422)

        organization = await OrganizationsDao(self.db).update_organization(id, name, description, active)
        return self.respond("ORGANIZATION CREATED", 200, organization_to_json(organization))

    @tornado.web.authenticated
    async def delete(self, id: UUID = None):
        if id is None:
            return self.respond("ORGANIZATION UUID IS MISSING", 400)
        if not await OrganizationsDao(self.db).delete_organization(id):
            return self.respond("INTERNAL SERVER ERROR", 500)
        return self.respond("ORGANIZATION DELETED", 203)

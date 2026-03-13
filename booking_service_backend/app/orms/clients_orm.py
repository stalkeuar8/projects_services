from app.models.booking import Clients
from app.orms.base_orm import BaseOrm


class ClientsOrm(BaseOrm[Clients]):

    model = Clients


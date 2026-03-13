from app.models.hotel import Hotels
from app.orms.base_orm import BaseOrm



class HotelsOrm(BaseOrm[Hotels]):

    model = Hotels

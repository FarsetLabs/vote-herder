from ninja import NinjaAPI
from counts.api import router as counts_router

api = NinjaAPI()

api.add_router("counts/", counts_router)
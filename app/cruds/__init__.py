from app.cruds.hub_cruds import HubCrud
from app.cruds.api_cruds import ApiCrud
from app.cruds.site_intent_cruds import SiteIntentCrud
from app.cruds.ppod_intent_cruds import PpodIntentCrud
from app.cruds.order_cruds import OrderCrud
from app.cruds.transaction_cruds import TransactionCrud

hub_cruds = HubCrud()
api_cruds = ApiCrud()
site_intent_cruds = SiteIntentCrud()
ppod_intent_cruds = PpodIntentCrud()
order_cruds = OrderCrud()
transaction_cruds = TransactionCrud()

from gasistafelice.base.models import Person, Resource
from gasistafelice.supplier.models import Supplier, Product, ProductCategory
from gasistafelice.gas.models import GAS, GASMember, GASSupplierOrder, GASSupplierSolidalPact, Delivery, Withdrawal
from gasistafelice.des.models import DES
from gasistafelice.bank.models import Account

type_model_d = {
	'site' : DES,
	'gas' : GAS,
	'gasmember' : GASMember,
	'person' : Person,
	'supplier' : Supplier,
	'product' : Product,
	'category' : ProductCategory,
	'order' : GASSupplierOrder,
	'pact' : GASSupplierSolidalPact,
	'delivery' : Delivery,
	'withdrawal' : Withdrawal,
	'account' : Account,
	'user' : Resource,
}

RESOURCE_LIST = type_model_d.keys()

#TODO fero TOCHECK
#from reports.models import PeriodicReport
#from users.models import UserContainer
#type_model_d.update( { 'periodicreport': PeriodicReport } )
#type_model_d.update( { 'usercontainer' : UserContainer } )



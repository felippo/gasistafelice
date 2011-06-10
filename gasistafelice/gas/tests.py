from django.test import TestCase
from django.contrib.auth.models import User

from gasistafelice.base.models import Person
from gasistafelice.gas.models import GAS, GASMember, GASSupplierStock, GASSupplierSolidalPact, GASMemberOrder, GASSupplierOrder, GASSupplierOrderProduct
from gasistafelice.supplier.models import Supplier, SupplierStock, Product, ProductCategory

from datetime import time, date

class GASSupplierStockTest(TestCase):
    '''Test behaviour of managed attributes of GASSupplierStock'''
    
    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')        
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.category = ProductCategory.objects.create(name='food') 
        self.product = Product.objects.create(name='carrots', category=self.category, producer=self.supplier)
        self.stock = SupplierStock.objects.create(supplier=self.supplier, product=self.product, price=100)
        
    def testSupplier(self):
        '''Verify if supplier is retrieved correctly'''
        gss = GASSupplierStock.objects.create(pact=self.pact, supplier_stock=self.stock)
        self.assertEqual(gss.supplier, self.supplier)
                
    def testPrice(self):
        '''Verify if price is computed correctly'''
        pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        gss = GASSupplierStock.objects.create(pact=pact, supplier_stock=self.stock)
        pact.order_price_percent_update = 0.05
        pact.save()
        self.assertEqual(gss.price, 105)

class GASMemberOrderTest(TestCase):
    '''Test behaviour of managed attributes of GASMemberOrder'''
    
    def setUp(self):
        self.now = date.today()
        user = User.objects.create(username='Foo') 
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')        
        self.person = Person.objects.create(name='John', surname='Smith', user=user)
        self.member = GASMember.objects.create(person=self.person, gas=self.gas)
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.category = ProductCategory.objects.create(name='food') 
        self.product = Product.objects.create(name='carrots', category=self.category, producer=self.supplier)
        self.stock = SupplierStock.objects.create(supplier=self.supplier, product=self.product, price=100)
        self.gas_stock = GASSupplierStock.objects.create(pact=self.pact, supplier_stock=self.stock)
        self.order = GASSupplierOrder.objects.create(pact=self.pact, date_start=self.now)
        self.order_product = GASSupplierOrderProduct.objects.create(order=self.order, stock=self.gas_stock)
        
    def testActualPrice(self):
        '''Verify if actual price is computed correctly'''
        self.order_product.delivered_price = 115
        self.order_product.save()
        gmo = GASMemberOrder.objects.create(purchaser=self.member, product=self.order_product, ordered_amount=1)
        self.assertEqual(gmo.actual_price, 115)
        
    def testOrder(self):
        '''Verify if SupplierOrder is computed correctly'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, product=self.order_product, ordered_amount=1)
        self.assertEqual(gmo.order, self.order)
        
    def testGAS(self):
        '''Verify if GAS is computed correctly'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, product=self.order_product, ordered_amount=1)
        self.assertEqual(gmo.gas, self.gas)
        
class GASSupplierOrderProductTest(TestCase):
    '''Test behaviour of managed attributes of GASSupplierOrderProduct'''
    
    def setUp(self):
        
        self.now = date.today()
        
        user1 = User.objects.create(username='Foo')
        user2 = User.objects.create(username='Bar')
        user3 = User.objects.create(username='Baz')
         
        self.person_1 = Person.objects.create(name='John', surname='Smith', user=user1)
        self.person_2 = Person.objects.create(name='Mary', surname='White', user=user2)
        self.person_3 = Person.objects.create(name='Paul', surname='Black', user=user3)
        
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_2 = GAS.objects.create(name='RiGAS', id_in_des='2')        
        
        self.supplier_1 = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        self.pact_3 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_1)
        
        self.member_1 = GASMember.objects.create(person=self.person_1, gas=self.gas_1)
        self.member_2 = GASMember.objects.create(person=self.person_2, gas=self.gas_1)
        self.member_3 = GASMember.objects.create(person=self.person_3, gas=self.gas_2)
        
        self.category = ProductCategory.objects.create(name='food') 
        
        self.product_1 = Product.objects.create(name='carrots', category=self.category, producer=self.supplier_1)
        self.product_2 = Product.objects.create(name='beans', category=self.category, producer=self.supplier_1)
        
        self.stock_1 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_1, price=100)
        self.stock_2 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_2, price=150)
        self.stock_3 = SupplierStock.objects.create(supplier=self.supplier_2, product=self.product_1, price=120)
        
        self.gas_stock_1 = GASSupplierStock.objects.create(pact=self.pact_1, supplier_stock=self.stock_1)
        self.gas_stock_2 = GASSupplierStock.objects.create(pact=self.pact_1, supplier_stock=self.stock_2)
        self.gas_stock_3 = GASSupplierStock.objects.create(pact=self.pact_2, supplier_stock=self.stock_3)
        self.gas_stock_4 = GASSupplierStock.objects.create(pact=self.pact_3, supplier_stock=self.stock_1)
        
        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_1, date_start=self.now)
        self.order_2 = GASSupplierOrder.objects.create(pact=self.pact_3, date_start=self.now)
        
        self.product_1 = GASSupplierOrderProduct.objects.create(order=self.order_1, stock=self.gas_stock_1)
        self.product_2 = GASSupplierOrderProduct.objects.create(order=self.order_1, stock=self.gas_stock_2)
        self.product_3 = GASSupplierOrderProduct.objects.create(order=self.order_2, stock=self.gas_stock_1)
                       
        
    def testOrderedAmount(self):
        '''Verify if ordered amount is computed correctly'''
        # FIXME: perhaps a fixture would be a better way to initialize the environment 
        
        GASMemberOrder.objects.create(purchaser=self.member_1, product=self.product_1, ordered_amount=1)
        GASMemberOrder.objects.create(purchaser=self.member_1, product=self.product_2, ordered_amount=2)
        GASMemberOrder.objects.create(purchaser=self.member_2, product=self.product_1, ordered_amount=4)
        # In a real world scenario, this order shouldn't be allowed 
        # (i.e. a GAS member issuing an GASMemberOrder against a SupplierOrder opened by another GAS)
        GASMemberOrder.objects.create(purchaser=self.member_3, product=self.product_1, ordered_amount=8)
        GASMemberOrder.objects.create(purchaser=self.member_3, product=self.product_3, ordered_amount=16)
        
        self.assertEqual(self.product_1.ordered_amount, 5)
        
    def testGas(self):
        '''Verify if gas attribute is computed correctly'''
        product = GASSupplierOrderProduct.objects.create(order=self.order_1, stock=self.gas_stock_1)
        self.assertEqual(product.gas, self.gas_1)
        
class GASSupplierOrderTest(TestCase):
    '''Tests GASSupplierOrder methods'''
    def setUp(self):
        self.now = date.today()
                       
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_2 = GAS.objects.create(name='RiGAS', id_in_des='2')        
        
        self.supplier_1 = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        self.pact_3 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_1)
        
        self.category = ProductCategory.objects.create(name='food') 
        
        self.product_1 = Product.objects.create(name='carrots', category=self.category, producer=self.supplier_1)
        self.product_2 = Product.objects.create(name='beans', category=self.category, producer=self.supplier_1)
        
        self.stock_1 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_1, price=100)
        self.stock_2 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_2, price=150)
        self.stock_3 = SupplierStock.objects.create(supplier=self.supplier_2, product=self.product_1, price=120)
        
        self.gas_stock_1 = GASSupplierStock.objects.create(pact=self.pact_1, supplier_stock=self.stock_1)
        self.gas_stock_2 = GASSupplierStock.objects.create(pact=self.pact_1, supplier_stock=self.stock_2)
        self.gas_stock_3 = GASSupplierStock.objects.create(pact=self.pact_2, supplier_stock=self.stock_3)

        self.gas_stock_4 = GASSupplierStock.objects.create(pact=self.pact_3, supplier_stock=self.stock_1)
        
                
    def testDefaultProductSet(self):
        '''Verify that the default product set is correctly generated'''
        order = GASSupplierOrder.objects.create(pact=self.pact_1, date_start=self.now)
        order.set_default_product_set()
        self.assertEqual(set(order.products.all()), set((self.gas_stock_1, self.gas_stock_2)))
        


#__test__ = {"doctest": """
#
#>>> from gasistafelice.gas.models.base import *
#>>> from gasistafelice.supplier.models import *
#>>> g1 = GAS.objects.all()[0]
#>>> gname = g1.name
#>>> gname
#u'Gas1'
#>>> gname
#u'Gas1sdfasgasga'
#
##>>> from gasistafelice.supplier.models import *
#>>> prod = Product.objects.all()[1000]
#>>> sellers = SupplierStock.objects.filter(product=prod)
#>>> len(sellers)
#1
#>>> prod = Product.objects.all()[0]
#>>> sellers = SupplierStock.objects.filter(product=prod)
#>>> len(sellers)
#2
#
#
#
#"""}
#
#class SupplierStockTest(TestCase):
#    fixtures = ['test_data.json']
#
#    def multiple_supplier_per_product(self):
#        """
#        Tests that product from id [1 .. 127] that is to say SupplierStock [1874 .. 2000] have 2 supplier.
#        This test require fixtures
#        """
#        prod_multiple = Product.objects.all()[0]
#        prod_unique = Product.objects.all()[1000]
#        seller = SupplierStock.objects.filter(product=prod_unique)
#        sellers = SupplierStock.objects.filter(product=prod_multiple)
#        self.assertTrue(len(seller) < len(sellers))
#        self.assertEqual(seller.supplier, sellers.supplier)

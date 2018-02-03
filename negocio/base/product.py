
from osv import fields, osv
import decimal_precision as dp

#------------------------------------
# Product base
#----------------------------------


class df_sicpt_product(osv.osv):
    
    _name= 'df.sicpt.product'  
    _inherits = {'product.product': "product_id"} 
    _description = 'Product df' 
    _columns = {
           'product_id': fields.many2one('product.product', 'Product', ondelete='cascade', required=True),     
           'parent_id': fields.many2one('product.product','Parent Product'),   
           'siglas': fields.char('Siglas', size=20, required=True),  
           #====================================================================
           # 'list_price_mn': fields.float('Sale Price', digits_compute=dp.get_precision('Sale Price'), help="Base price for computing the customer price. Sometimes called the catalog price."),
           # 'standard_price_mn': fields.float('Cost Price', required=True, digits_compute=dp.get_precision('Purchase Price'), help="Product's cost for accounting stock valuation. It is the base price for the supplier price."),
           # 'cost_method_mn': fields.selection([('standard','Standard Price'), ('average','Average Price')], 'Costing Method', required=True,
           #                 help="Standard Price: the cost price is fixed and recomputed periodically (usually at the end of the year), Average Price: the cost price is recomputed at each reception of products."),
           #====================================================================
           #====================================================================
           # 'manufacture_line': fields.related('categ_id','manufacture_line',readonly=True ,type='selection',selection=[('sacrifice','Sacrifice'),('boneless','Boneless'),('packed','Packed')], string='Manufacture Line'),
           # 'manufacture_category': fields.related('categ_id','name',readonly=True ,type='selection', string='Manufacture Category'),        
           #====================================================================
    }
    
    _defaults = {
	     'uom_id': 2,
       'uom_po_id': 2,  
    }
    
    def onchange_uom(self, cursor, user, ids, uom_id,uom_po_id):
        if uom_id and uom_po_id:
            uom_obj=self.pool.get('product.uom')
            uom=uom_obj.browse(cursor,user,[uom_id])[0]
            uom_po=uom_obj.browse(cursor,user,[uom_po_id])[0]
            if uom.category_id.id != uom_po.category_id.id:
                return {'value': {'uom_po_id': uom_id}}
        return False   

df_sicpt_product()
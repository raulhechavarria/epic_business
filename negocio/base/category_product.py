from osv import fields, osv


class df_sicpt_category_product(osv.osv):
    
    _name= 'df.sicpt.product.category'  
    _inherits = {'product.category': "product_category_id"} 
           
    _description = 'Category Product' 
    _columns = {
            'product_category_id': fields.many2one('product.category', 'Product Category', ondelete='cascade', required=True),
            'manufacture_line': fields.selection([('sacrifice','Sacrifice'),('boneless','Boneless'),('packed','Packed')], 'Manufacture Line', required = True),
                    }
    
df_sicpt_category_product()

 
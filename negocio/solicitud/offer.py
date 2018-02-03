from osv import fields, osv

class offer(osv.osv):
    
    def _obtain_partner(self, cr, uid, ids, *args):
        res = {}
        for offer in self.browse(cr, uid, ids, context=None):
            partner = offer.contract_id.partner_id.name 
            res[offer.id] = partner  
        return res
    
    _name = 'offer'
    _description = 'Detalles de la oferta'
    _rec_name = 'no_contract'
    _columns = {
        'no_offer': fields.char('numero de oferta', size=10,  required=True),
        
        'suplement_id': fields.many2one('suplement', 'Suplemento', select=True),
        'contract_id': fields.many2one('contract', 'Contrato', select=True, required=False),
        'element_offer_ids':fields.one2many('element.offer', 'offer_id', 'oferta de elementos', required=False, ondelete='cascade'),
        'responsable': fields.many2one('hr.employee', 'confeccionado', select=True),
        'partner_contract_id': fields.function(_obtain_partner, string='Empresa', type='char',store=True),
        
        }
offer()

class element_offer(osv.osv):

    def _get_import(self, cr, uid, ids, name, args, context=None):
        res = {}
        for elem in self.browse(cr, uid, ids, context=None):
            results = elem.price * elem.count_to_offer
            res[elem.id] = results
        return res
    

    _name = 'element.offer'
    _description = 'Listado de elementos a ofertar'
    _columns = {
        'product_id': fields.many2one('product.product', 'Descripcion', select=True),
        'offer_id': fields.many2one('offer', 'Oferta', select=True),
        'count': fields.integer('Cantidad', size=11),
        'count_to_offer': fields.integer('Cantidad a ofertar', size=11),
        'description': fields.text('Nota'),
        'price': fields.float('Sale Price', help="precio acordado"),
        'import':fields.function(_get_import, string='Importe',type='float', store=True),
        
        }
element_offer()
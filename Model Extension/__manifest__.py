{
    'name': 'Extend Model',
    'summary': 'Extend Model - Inventory, Contacts',
    'version': '12',
    'category': 'Contacts',
    'author': 'Ascaldera',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
        'product',
        'base',
        'stock',
        'website',
        'crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/extend_models_contact.xml',
        'views/extend_models_inventory.xml',
        'views/extend_models_crm.xml',
        'views/hide_default.xml',
        'data/default_info.xml',        
    ],
    'installable': True,
}
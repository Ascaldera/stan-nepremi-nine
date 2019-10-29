{
    'name': 'Extend Model',
    'summary': 'Extend Model - Inventory, Contacts v2',
    'version': '12',
    'category': 'Contacts',
    'author': 'Luka Sekulic',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
        'product',
        'base',
        'stock',
        'website',
        'website_sale',
        'crm'
    ],
    'data': [
        'views/extend_models_contact.xml',
        'views/extend_models_inventory.xml',
        'views/extend_models_crm.xml',
        'views/hide_default.xml'
    ],
    'installable': True,
}


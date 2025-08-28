{
    'name': 'CardKnox POS Terminal Integration',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Integrates CardKnox payment terminals with the Point of Sale.',
    'author': 'Tech Craft Innovations',
    'license': 'OPL-1',
    'depends': [
        'point_of_sale',
        'cardknox_payment',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cardknox_payment_pos/static/src/js/pos_cardknox.js',
        ],
    },
    'data': [
        
    ],
    'installable': True,
    'auto_install': True,
}

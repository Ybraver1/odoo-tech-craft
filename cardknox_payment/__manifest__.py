{
    'name': 'CardKnox Payment Provider',
    'version': '1.0',
    'author': 'Yidel Braver',
    'category': 'Accounting/Payment',
    'summary': 'CardKnox Payment Gateway Integration',
    'depends': ['payment'],
    'assets': {
        'web.assets_backend':[
            'static/description/icon.png'
        ]
    },
    'data': [
         
        'views/payment_provider_views.xml',
        'views/payment_cardknox_templates.xml',
        
        'data/payment_cardknox_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
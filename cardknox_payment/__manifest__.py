{
    'name': 'CardKnox Payment Provider',
    'version': '1.0',
    'author': 'Yidel Braver',
    'category': 'Accounting/Payment',
    'summary': 'CardKnox Payment Gateway Integration with iFields',
    'depends': ['payment'],
    'assets': {
        'web.assets_backend': [
            'static/description/icon.png'
        ],
        'web.assets_frontend': [
            'cardknox_payment/static/src/css/payment_form.css',
            'cardknox_payment/static/src/js/payment_form.js',
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

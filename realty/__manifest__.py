# -*- coding: utf-8 -*-
{
    'name': "realty",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Tech Craft Innovations",
    'website': "https://www.techcraftinnovations.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'module_category_productivity',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','calendar','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/property_showing_views.xml',
        'views/property_views.xml',
        'views/templates.xml',
        'data/property_showing_stage.xml',
        'data/property_stage.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


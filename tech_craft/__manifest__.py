{
    'name': 'Tech Craft',
    'version': '1.0',
    'author': 'Yidel Braver',
    'category': 'Custom',
    'summary': 'Manage Projects, Customers, Tickets, and Tasks',
    'depends': ['base', 'project', 'contacts', 'helpdesk'],
    'data': [
        'views/menu_and_views.xml',
         'views/ticket_vies.xml'
    ],
    'installable': True,
    'application': True,
}
{
    'name': 'Service Model',
    'summary': 'Module to manage services',
    'version': '14.0.1.0.0',
    'category': 'Tools',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/service_view.xml',
        'data/service_data.xml',
    ],
}

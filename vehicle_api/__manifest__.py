{
    'name': "Vehicle API",
    'summary': "A module to access vehicle information using registration number",
    'description': "This module allows you to access vehicle information using registration number",
    'author': "Your Name",
    'category': 'Uncategorized',
    'version': '13.0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_information.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

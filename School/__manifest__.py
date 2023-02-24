{  
    'name': "School",
    'version':'1.1', 
    'author': 'Salih',
    'summary': "School Managment Software",
    'sequence': 1,
    'description':"This is a school management system software supported in "
        "odoo v14",
    'catageory':'School',
    'website':'https://test.com',
    'depends': ['base'],
    'data':[
        "security/ir.model.access.csv",
        "views/school_view.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False, 
   
}   
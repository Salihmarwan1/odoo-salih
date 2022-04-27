{
    'name': "hospital-dmitri",
    'depends': ['base', 'mail',],
    'data': [
        "security/ir.model.access.csv",
        "data/data.xml",
        "wizard/create_appointment_view.xml",
        "wizard/search_appointment_view.xml",
        "views/doctor_view.xml",
        "views/patient_view.xml",
        "views/patient_gender_view.xml",
        "views/kids_view.xml",
        "views/appointment_view.xml",
    ]
}

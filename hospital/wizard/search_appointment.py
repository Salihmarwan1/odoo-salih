import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)

class SearchAppointmentWizard(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = "Search appointment wizard"

    patient_id=fields.Many2one("hospital.patient", string="Patient")

    def action_search_appointment(self):
        action = self.env.ref("hospital.action_hospital_appointment").read()[0]
        action["domain"] = [("patient_id", "=", self.patient_id.id)]
        return action
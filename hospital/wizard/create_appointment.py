import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create appointment wizard"

    date_appointment = fields.Date(string="Date")
    patient_id=fields.Many2one("hospital.patient", string="Patient")

    def action_create_appointment(self):
        vals = {
            "patient_id": self.patient_id.id,
            "date_appointment": self.date_appointment
        }
        appointment_rec = self.env["hospital.appointment"].create(vals) 
        return {
            "name": _("Appointment"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.appointment",
            "res_id": appointment_rec.id,
            "target": "new"
        }
    
    def action_view_appointment(self):
        action = self.env.ref("hospital.action_hospital_appointment").read()[0]
        action["domain"] = [("patient_id", "=", self.patient_id.id)]
        return action
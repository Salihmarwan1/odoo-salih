from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital doctor"
    _rec_name = "doctor_name"

    doctor_name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True, copy=False)
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other")
    ], required=True, default="male", tracking=True)
    note = fields.Text(string="Description", tracking=True)
    image = fields.Binary(string="Patient image")

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get("doctor_name"):
            default["doctor_name"] = _("%s (Copy)", self.doctor_name)
        default["note"] = "Copied record"
        return super(HospitalDoctor, self).copy(default)
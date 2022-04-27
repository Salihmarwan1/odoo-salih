import logging
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital patient"

    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        #res["age"] = 18
        return res

    name = fields.Char(string="Name", required=True, tracking=True)
    reference = fields.Char(string="Order reference", tracking=True, required=True, copy=False, 
                            readonly=True, default=lambda self: _('New'))
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other")
    ], required=True, default="male", tracking=True)
    note = fields.Text(string="Description", tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], 
                                default="draft", string="Status", tracking=True)
    responsible_id = fields.Many2one("res.partner", string="Responsible")
    appointment_count = fields.Integer(string="Appointment count", compute="_compute_appointment_count")
    image = fields.Binary(string="Patient image")
    appointment_ids = fields.One2many("hospital.appointment", "patient_id", string="Appointments")


    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
 
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
    
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        _logger.warning("overrided create method")

        if not vals.get("note"): 
            vals["note"] = "New patient"

        if vals.get("reference", _("New")) == _("New"):
            vals["reference"] = self.env["ir.sequence"].next_by_code("hospital.patient" or _("New"))

        res = super(HospitalPatient, self).create(vals)
        return res

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env["hospital.appointment"].search_count([("patient_id", "=", rec.id)])
            rec.appointment_count = appointment_count

    @api.constrains("name")
    def check_name(self):
        for rec in self:
            patients = self.env["hospital.patient"].search([("name", "=", rec.name), ("id", "!=", rec.id)])
            if patients:
                raise ValidationError("Name already exists")

    @api.constrains("age")
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError("Age cannot = 0")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.reference + " " + rec.name
            result.append((rec.id, name))
        return result
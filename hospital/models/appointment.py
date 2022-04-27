import logging
from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital appointment"
    _order = "name asc"

    name = fields.Char(string="Name", required=True, copy=False, readonly=True, tracking=True, default=lambda self: _("New"))
    patient_id=fields.Many2one("hospital.patient", string="Patient", required=True)
    age = fields.Integer(string="Age", related="patient_id.age", tracking=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other")
    ], required=True, default="male", tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], 
                                default="draft", string="Status", tracking=True)
    note = fields.Text(string="Description", tracking=True)
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check up time")
    prescription = fields.Text(string="Prescription", tracking=True)
    prescription_line_ids = fields.One2many("appointment.prescription.lines", "appointment_id", string="Prescription lines")


    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'
 
    def action_draft(self):
        self.state = 'draft'
    
    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        _logger.warning("overrided create method")

        if not vals.get("note"): 
            vals["note"] = "New patient"

        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("hospital.appointment" or _("New"))

        res = super(HospitalAppointment, self).create(vals)
        return res

    @api.onchange("patient_id")
    def onchange_patient_id(self):
        _logger.warning("onchange triggered")

        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ""
            self.note = ""

    def unlink(self):
        if self.state == "done":
            raise ValidationError("Cant delete done state")
        return super(HospitalAppointment, self).unlink()

    @api.model
    def message_post_test(self, *args):   
        #_logger.error(f"{self=}")
        # _logger.error(f"{self.name=}")
        for arg in args:
            _logger.error(f"{arg=}")
            if (channel:=self.env["mail.channel"].browse(arg.get('id'))):
                #_logger.error(f"{channel=}")
                new_arg = {a:arg[a] for a in arg}

                #_logger.error(f"{new_arg=}")
                #_logger.error(f"{arg=}")
                #_logger.error("before message_post")
                return channel.message_post(**arg)
                #_logger.error(f"message_post_test {ids=}")
        

    def test_lua(self, *args):
        return [[("author_id", "=", 3)]]

class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment prescription lines"

    name = fields.Char(string="Medicine")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")

class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        _logger.error(f"{self=}")
        _logger.error(f"{fields=}")

        keys = self.fields_get()
        for i, dom in enumerate(domain):
            field = dom[0]
            if 'many2one' in keys[field]["type"]:
                try:
                    possible_int = int(domain[i][2])
                except:
                    pass
                else: 
                    domain[i][2] = possible_int
        _logger.error(f"{domain=}")
        return super().search_read(domain, fields, offset, limit, order)

class MailChannel(models.Model):
    _inherit = "mail.channel"

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        _logger.error(f"{self=}")
        _logger.error(f"{fields=}")

        keys = self.fields_get()
        for i, dom in enumerate(domain):
            field = dom[0]
            if 'many2many' in keys[field]["type"]:
                try:
                    possible_int = int(domain[i][2])
                except:
                    pass
                else: 
                    domain[i][2] = possible_int
        _logger.error(f"{domain=}")
        return super().search_read(domain, fields, offset, limit, order)

class TestSearchRead(models.Model):
    _inherit = "res.users"

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain, fields, offset, limit, order)
        return res 
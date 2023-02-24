import email
import logging
from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import requests

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
            #_logger.error(f"{arg=}")
            if (channel:=self.env["mail.channel"].browse(arg.get('id'))):
                _logger.error(f"{channel=}")
                new_arg = {a:arg[a] for a in arg}
                new_arg["prosody"] = True

                #_logger.error(f"{new_arg=}")
                #_logger.error(f"{arg=}")
                #_logger.error("before message_post")
                message_post = channel.message_post(**new_arg).id
                  
                return message_post
                #_logger.error(f"message_post_test {ids=}")

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
        #_logger.error(f"{self=}")
        #_logger.error(f"{fields=}")

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
            elif 'many2many' in keys[field]["type"]:
                try:
                    possible_int = int(domain[i][2])
                except:
                    pass
                else: 
                    domain[i][2] = possible_int
        #_logger.error(f"{domain=}")
        res = super().search_read(domain, fields, offset, limit, order)
        return res 

class TestSearchRead(models.Model):
    _inherit = "res.users"

    def search_read_custom(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain, fields, offset, limit, order)
        return res 

class ChannelSearchRead(models.Model):
    _inherit = "mail.channel"

    def search_read_custom(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain, fields, offset, limit, order)
        return res 

    @api.model
    def search_custom(self, *args, offset=0, limit=None, order=None, count=False):
        new_args =[]
        for arg in args:
            new_arg=[]
            for a in arg:
                new_arg.append(int(a) if a.isdigit() else a)
            new_args.append(new_arg)
        _logger.error(f"{new_args=}")
        res = super(ChannelSearchRead, self).search(new_args, offset, limit, order, count)
        return res.ids if res else 0

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_xmlid=None, subtype_id=False, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):

                    #_logger.error(f"{kwargs=}")

                    res = super().message_post(body=body, subject=subject, message_type=message_type,
                                                email_from=email_from, author_id=author_id, parent_id=parent_id,
                                                subtype_xmlid=subtype_xmlid, subtype_id=subtype_id, partner_ids=partner_ids,
                                                channel_ids=channel_ids, attachments=attachments, attachment_ids=attachment_ids,
                                                add_sign=add_sign, record_name=record_name, **kwargs)
                    #_logger.error(f"res {res=}")
                    if res.id and not kwargs.get("prosody"):
                        url = "https://hoary.vertel.se:5281/rest"
                        js = {'body': body, 'kind': 'message', 'to': 'dostoevsky@hoary.vertel.se', 
                              'type': 'chat', 'id': 'ODOOODOO' + str(res.id)}
                        headers = {'Content-type': 'application/json'}
                        request_post = requests.post(url, json=js, headers=headers, verify=False, auth=("admin", "admin"))
                    return res

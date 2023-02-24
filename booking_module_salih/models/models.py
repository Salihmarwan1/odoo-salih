from odoo import models, fields

class BookingModel(models.Model):
    _name = 'booking.model'
    _description = 'Booking Model'

    service_id = fields.Many2one('service.model', string='Service')
    appointment_time = fields.Datetime(string='Appointment Time')
    registration_number = fields.Char(string='Registration Number')
    contact_name = fields.Char(string='Contact Name')
    contact_email = fields.Char(string='Contact Email')
    contact_phone = fields.Char(string='Contact Phone')
    confirmation = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Confirmation', default='yes')

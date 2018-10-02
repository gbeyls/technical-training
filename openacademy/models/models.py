# -*- coding: utf-8 -*-

from odoo import api, fields, models
from openerp.exceptions import ValidationError

class Course(models.Model):
        _name = 'openacademy.course'
        name = fields.Char(string='Name')
        description = fields.Text(string='Description')
        responsible_id = fields.Many2one('res.partner',string='Responsible')

class Session(models.Model):
        _name = 'openacademy.session'
        name = fields.Char(string='Name')
        course_id = fields.Many2one('openacademy.course')
        start_date = fields.Datetime(string='Date start')
        end_date = fields.Datetime(string='Date end')        
        attendees = fields.Many2many('res.users',string='Attendees')
        status = fields.Selection([
        ('registration_open', 'Registration open'),
        ('finished', 'Finished'),
        ('delivering', 'Delivering')
        ], string='Status',compute='_compute_status',store='True')
        
        @api.onchange('start_date','end_date') 
        def _compute_status(self):
            if fields.Datetime.today() > self.end_date :
                self.status='finished'
            elif fields.Datetime.today() < self.start_date :
                self.status='registration_open'
            else :
                self.status='delivering'
                
        @api.constrains('start_date','end_date')
        def _check_timeline(self):
            if self.end_date < self.start_date :
                raise ValidationError("Start date must be before end date")
                
        

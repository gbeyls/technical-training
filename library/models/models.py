# -*- coding: utf-8 -*-

from odoo import api, fields, models
from openerp.exceptions import ValidationError

class Book(models.Model):
        _name = 'library.book'
        name = fields.Char(string='Name')
        editors = fields.Many2many('res.partner',string='Editors')
        authors = fields.Many2many('res.partner',string='Authors')
        summary = fields.Text(string='Summary')
        borrowing = fields.One2many('library.borrowing','book',string='Borrowing')
        status = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('available', 'Available')
        ], string='Status',compute='_compute_status',store='True',readonly='True')
        
        @api.depends('borrowing') 
        def _compute_status(self):
            self.status='available'
            if self.borrowing :
                last_borrowing=self.borrowing.sorted(key=lambda r: r.end_date)[0]
                if fields.Datetime.today() < last_borrowing.end_date :
                    self.status='borrowed'
                    
        
class Customer(models.Model):
        _name = 'library.customer'
        name = fields.Char(string='Name')
        user = fields.Many2one('res.users',string='Utilisateur')
        borrowed_books = fields.One2many('library.borrowing', 'customer', string='Borrowed book',readonly='True')

class Borrowing(models.Model):
        _name = 'library.borrowing'
        book = fields.Many2one('library.book')
        customer = fields.Many2one('library.customer')
        start_date = fields.Datetime(string='Date start')
        end_date = fields.Datetime(string='Date end')        
                
        @api.constrains('start_date','end_date')
        def _check_timeline(self):
            if self.end_date < self.start_date :
                raise ValidationError("Start date must be before end date")
                
class XXX(models.Model):
        _name = 'library.rent'
                
        

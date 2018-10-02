# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from openerp.exceptions import ValidationError 

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('library.partner', string='Customer',#default=
                                 )
    customer_address = fields.Text(string='Address', readonly=True)
    customer_email = fields.Char(string='Email', readonly=True)
    book_id = fields.Many2one('library.book', string='Book',#default='_compute_book_default_value'
                             )
    book_authors_ids = fields.Many2many(string="Authors", related='book_id.authors_ids', readonly=True)
    book_edition_date =  fields.Date(string='Edition date', related='book_id.edition_date', readonly=True)
    book_isbn = fields.Char(string='ISBN',related='book_id.isbn', readonly=True)
    book_publisher_id = fields.Many2one(string='Publisher',related='book_id.publisher_id', readonly=True)
    rental_date = fields.Date(string='Rental date')
    return_date = fields.Date(string='Return date')
    
    returned = fields.Boolean(string="Returned")
    
    @api.constrains('rental_date','return_date')
    def _check_timeline(self):
        if self.return_date < self.rental_date :
            raise ValidationError("Start date must be before end date.")
            
    @api.constrains('book_id')
    def _check_returned(self):
            if self.book_id.status :
                raise ValidationError("Book is not yet returned. Be patient.")
            
    def _compute_customer_default_value(self):

        return
    
    def _compute_book_default_value(self):

        return
        
    @api.onchange('customer_id')
    def onchange_customer_id(self):
            self.customer_address = self.customer_id.address
            self.customer_email = self.customer_id.email

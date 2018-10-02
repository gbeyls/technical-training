# -*- coding: utf-8 -*-
from odoo import api, models, fields

class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title')
    authors_ids = fields.Many2many('library.partner', string="Authors")
    edition_date =  fields.Date(string='Edition date',)
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')
    status = fields.Selection([
    ('borrowed', 'Borrowed'),
    ('available', 'Available')
    ], string='Status',compute='_compute_status',store='True',readonly='True')
    on_late = fields.Boolean(string='Late',compute='_compute_late',store='True',readonly='True')
        
    
    @api.depends('rental_ids') 
    def _compute_status(self):
        self.status='available'
        if self.rental_ids :
            last_rental=self.rental_ids.sorted(key=lambda r: r.return_date)[0]
            if not last_rental.returned :
                self.status='borrowed'
                
    @api.depends('rental_ids') 
    def _compute_late(self):
        self.on_late=False
        if self.rental_ids :
            last_rental=self.rental_ids.sorted(key=lambda r: r.return_date)[0]
            if fields.Date.today() > last_rental.return_date :
                self.on_late=True

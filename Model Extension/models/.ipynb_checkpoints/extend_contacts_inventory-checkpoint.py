# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models, tools

class ExtendContacts(models.Model):
    _inherit = ['res.partner']
    
    #OSNOVNI REQUIRED PODATKI
    tip_stranke = fields.Selection(selection=[('prodajalec', 'Prodajalec'),
                                              ('kupec', 'Kupec'),
                                              ('najemodajalec', 'Najemodajalec'),
                                              ('najemnik', 'Najemnik')])
    spol = fields.Selection(selection=[('moski', 'Moški'),('ženski', 'Ženski')])
    tretja_oseba = fields.Boolean(string = 'Tretja Oseba')
    #TODO: potrebno definirati novo tag formo za tag potrebe, nato spodnji field pretvoriti v many2many tag
    osebnostne_lastnosti = fields.Char(string = 'Osebnostne lastnosti')
    
    #PODATKI O NEPREMIČNINAH
    nepremicnine = fields.One2many(comodel_name='product.template', inverse_name="contact", string='Product ID')
    pridobitev = fields.Char(string = 'Način pridobitve')
    objava_kje = fields.Selection(string = 'Oglas / kje', selection = [('portal_1', 'Portal 1'), ('portal_2', 'Portal 2')])
    objava_kje_datum = fields.Date(string = 'Oglas / kdaj')
    objava_odziv = fields.Char(string = 'Oglas / odziv')
    objava_spremembe = fields.Char(string = 'Oglas / spremembe')
    objava_stevilo_ogledov = fields.Float(string = 'Oglas / število ogledov')
    stranka_odziv = fields.Char(string = 'Ogled / odziv stranke')
    povprasevanje = fields.Char(string = 'Povpraševanja')
    mnenje = fields.Char(string = 'Naše mnenje')
    
    #PODATKI O ISKANJU
    #kasneje tag
    isce_kaj = fields.Char(string = 'Kaj išče')
    isce_kje = fields.Char(string = 'Kje išče')
    isce_cena = fields.Float(string = 'Cena')
    isce_namen = fields.Char(string = 'Namen')
    isce_kontakt_dan = fields.Date(string = 'Nazadnje kontaktiral')
    isce_zgodovina = fields.Char(string = 'Že ogledano')
    isce_ok = fields.Char(string = 'Kaj jim je bilo všeč')
    isce_nok = fields.Char(string = 'Kaj jim ni bilo všeč')
    isce_kontaktiran = fields.Date(string = 'Nazadnje kontaktiran')
    isce_zivali = fields.Boolean(string = 'Živali')
    
    #PODATKI O PRODAJALCIH
    #create_uid - kdo je vnesel prodajalca
    prodajalec_koliko = fields.Float(string = 'Minimalna ponudba')
    prodajalec_ponudbe = fields.Boolean(string = 'Ponudbe')
    prodajalec_ponudbe_info = fields.Char(string = 'Kakšne ponudbe')
    prodajalec_procent = fields.Float(string = 'Procent od prodaje')
    prodajalec_datum_pogodbe = fields.Date(string = 'Posredniška pogodba / datum')
    prodajalec_komunikacija = fields.Char(string = 'Način komunikacije')
    
    #PODATKI O KUPCIH
    kupec_naronik = fields.Boolean(string = 'Naročnik')
    kupec_aktiven = fields.Boolean(string = 'Aktivni kupec')
    kupec_znizana_cena = fields.Boolean(string = 'Znižana cena po oddani ponudbi')
    kupec_obvescanje = fields.Char(string = 'Obveščanje za ponudbe')
    
    
    #PODATKI O NAJEMODAJALCIH
    kasneje tag
    najemodajalec_komu = fields.Char(string = 'Komu oddajajo')   
    najemodajalec_od = fields.Date(string = 'Od kdaj oddaja')
    najemodajalec_do = fields.Date(string = 'Do kdaj oddaja')
    najemodajalec_otroci = fields.Boolean(string = 'Otroci')
    najemodajalec_studenti = fields.Boolean(string = 'Študenti')
    
    
    #PODATKI O NAJEMNIKIH
    najemnik_koliko = fields.Integer(string = 'Koliko oseb')
    najemnik_dolzina = fields.Integer(string = 'Dolžina najema v mesecih')
    najemnik_zgodovina = fields.Char(string = 'Kje so živeli')
    najemnik_zaposlitev = fields.Char(string = 'Zaposlitev')
    najemnik_studenti = fields.Boolean(string = 'Študent')
        
    
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    contact=fields.Many2one(comodel_name="res.partner", string="Contact")
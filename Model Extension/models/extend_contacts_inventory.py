# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
from odoo import fields, api, models, tools
from odoo import exceptions
from dateutil.relativedelta import *


class ExtendContacts(models.Model):
    _inherit = ['res.partner']
    
    #OSNOVNI REQUIRED PODATKI
    tip_stranke = fields.Selection(selection=[('prodajalec', 'Prodajalec'),
                                              ('kupec', 'Kupec'),
                                              ('najemodajalec', 'Najemodajalec'),
                                              ('najemnik', 'Najemnik')])
    spol = fields.Selection(selection=[('moski', 'Moški'),('ženski', 'Ženski')])
    tretja_oseba = fields.Boolean(string = 'Tretja Oseba')
    zakaj_kupuje=fields.Char(string='Zakaj kupuje')
    
    #PODATKI O NEPREMIČNINAH
    nepremicnine = fields.One2many(comodel_name='product.template', inverse_name="contact", string='Product ID')
    pridobitev = fields.Char(string = 'Način pridobitve')
    objava_kje = fields.Selection(string = 'Oglas / kje', selection = [('portal_1', 'Portal 1'), ('portal_2', 'Portal 2')])
    objava_kje_datum = fields.Date(string = 'Oglas / kdaj')
    objava_odziv = fields.Char(string = 'Oglas / odziv')
    objava_spremembe = fields.Char(string = 'Oglas / spremembe')
    objava_stevilo_ogledov = fields.Integer(string = 'Oglas / število ogledov')
    stranka_odziv = fields.Char(string = 'Ogled / odziv stranke')
    povprasevanje = fields.Char(string = 'Zadnji klici, povpraševanja')
    mnenje = fields.Text(string = 'Naše mnenje')
    
    #PODATKI O ISKANJU
    poizvedba_nepremicnina=fields.Many2many(string="Kaj išče",
                              comodel_name="res.partner.category",
                              relation="contact_tag_nepremicnina_rel",
                              domain="[('tag_type','=','nepremicnina')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    poizvedba_kraj = fields.Many2many(string="Kje išče",
                              comodel_name="res.partner.category",
                              relation="contact_tag_kraj_rel",
                              domain="[('tag_type','=','lokacija')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    poizvedba_namen = fields.Many2many(string="S kakšnim namenom",
                              comodel_name="res.partner.category",
                              relation="contact_tag_namen_rel",
                              domain="[('tag_type','=','namen')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    poizvedba_cena = fields.Float(string = 'Cena') #EUR
    poizvedba_kontakt_dan = fields.Date(string = 'Nazadnje kontaktiral')
    poizvedba_zgodovina = fields.Char(string = 'Že ogledano')
    poizvedba_ok = fields.Char(string = 'Kaj jim je bilo všeč')
    poizvedba_nok = fields.Char(string = 'Kaj jim ni bilo všeč')
    poizvedba_kontaktiran = fields.Date(string = 'Nazadnje kontaktiran')
    poizvedba_balkon = fields.Boolean(string = 'Balkon')
    poizvedba_dvigalo = fields.Boolean(string = 'Dvigalo')
    poizvedba_vrt = fields.Boolean(string = 'Vrt')
    
    #PODATKI O PRODAJALCIH
    #create_uid - kdo je vnesel prodajalca
    prodajalec_ponudbe = fields.Boolean(string = 'Ponudbe')
    prodajalec_ponudbe_info = fields.Char(string = 'Kakšne ponudbe')
    prodajalec_komunikacija = fields.Char(string = 'Način komunikacije')
    
    #PODATKI O KUPCIH
    kupec_obvescanje = fields.Many2many(string="O kakšnih ponudbah ga obveščamo",
                              comodel_name="res.partner.category",
                              relation="contact_tag_ponudba_rel",
                              domain="[('tag_type','=','ponudba')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    kupec_narocnik = fields.Boolean(string = 'Naročnik')
    kupec_aktiven = fields.Boolean(string = 'Aktivni kupec')
    kupec_znizana_cena = fields.Boolean(string = 'Znižana cena po oddani ponudbi') 
    
    #PODATKI O NAJEMODAJALCIH
    najemodajalec_komu = fields.Many2many(string="Komu oddajajo",
                              comodel_name="res.partner.category",
                              relation="contact_tag_stranka_rel",
                              domain="[('tag_type','=','stranka')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    najemodajalec_od = fields.Date(string = 'Od kdaj oddaja')
    najemodajalec_do = fields.Date(string = 'Do kdaj oddaja')
    najemodajalec_otroci = fields.Boolean(string = 'Otroci')
    najemodajalec_studenti = fields.Boolean(string = 'Študenti')
    najemodajalec_zivali = fields.Boolean(string = 'Ima živali')
    
    
    #PODATKI O NAJEMNIKIH
    najemnik_osebe = fields.Selection(string = 'Koliko oseb', selection=[('1','1'),
                                                                         ('2','2'),
                                                                         ('3','3'),
                                                                         ('4','4'),
                                                                         ('5','5'),
                                                                         ('6','6'),
                                                                         ('7','7'),
                                                                         ('8','8'),
                                                                         ('9','9'),
                                                                         ('10','10')])
    najemnik_dolzina = fields.Integer(string = 'Dolžina najema v mesecih')
    najemnik_zgodovina = fields.Char(string = 'Kje so živeli')
    najemnik_zaposlitev = fields.Selection(string = 'Zaposlitev', selection=[('redno','Redna zaposlitev'), 
                                                                             ('pol','Polovični delovni čas'), 
                                                                             ('student','Študent'),
                                                                             ('redno','Samo zaposlitev')])
    najemnik_studenti = fields.Boolean(string = 'Študent')
    najemnik_zivali = fields.Boolean(string = 'Živali')
    
    #PODATKI O TRETJI OSEBI
    tretja_oseba_osebnost = fields.Many2many(string="Osebnostne lastnosti",
                              comodel_name="res.partner.category",
                              relation="contact_tretja_oseba_tag_osebnost_rel",
                              domain="[('tag_type','=','lastnosti')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    
    tretja_oseba_obvescanje = fields.Many2many(string="Obveščanje",
                                               comodel_name="res.partner.category",
                                               relation="contact_tretja_oseba_tag_ponudba_rel",
                                               domain="[('tag_type','=','ponudba')]",
                                               options="{'color_field': 'color', 'no_create_edit': True}",
                                               track_visibility='onchange')
    
    @api.onchange('email')
    def check_mail(self):
        if self.email:
            contact=self.env['res.partner'].search([('email','=',self.email)])
            if len(contact)==0:
                return {'warning':{'title':'Opozorilo!','message':"E-mail naslov je že v uporabi."}}
    
    @api.onchange('mobile','phone')
    def check_phone(self):
        mobile_contact=self.env['res.partner'].search([('mobile','=',self.mobile)])
        phone_contact=self.env['res.partner'].search([('phone','=',self.phone)])
        if self.mobile and self.phone:
            if len(mobile_contact)!=0 and len(phone_contact)!=0:
                return {'warning':{'title':'Opozorilo!','message':"Telefonska in mobilna številka sta že v uporabi."}}
        if self.mobile:
            if len(mobile_contact)!=0:
                return {'warning':{'title':'Opozorilo!','message':"Mobilna številka je že v uporabi."}}
        if self.phone:
            if len(phone_contact)!=0:
                return {'warning':{'title':'Opozorilo!','message':"Telefonska številka je že v uporabi."}}

    @api.onchange('tip_stranke','tretja_oseba')
    def erase(self):
        if self.tip_stranke!='prodajalec':
            self.objava_kje=[]
            self.objava_kje_datum=[]
            self.objava_odziv=""
            self.objava_spremembe=""
            self.objava_stevilo_ogledov=0
            self.prodajalec_ponudbe=False
            self.prodajalec_ponudbe_info=""
            self.prodajalec_komunikacija=""
        elif self.tip_stranke!='kupec':
            self.poizvedba_cena=0
            self.poizvedba_kontakt_dan=[]
            self.poizvedba_kontaktiran=[]
            self.poizvedba_nepremicnina=False         
            self.poizvedba_kraj=False
            self.poizvedba_namen=False
            self.poizvedba_zgodovina=""
            self.poizvedba_ok=""
            self.poizvedba_nok=""
            self.kupec_obvescanje=[]
            self.kupec_narocnik=False 
            self.kupec_aktiven=False
            self.kupec_znizana_cena=False
            self.kupec_obvescanje=False
        if self.tip_stranke!='najemodajalec':
            self.objava_kje=[]
            self.objava_kje_datum=[]
            self.objava_odziv=""
            self.objava_spremembe=""
            self.objava_stevilo_ogledov=0
            self.najemodajalec_komu=[]
            self.najemodajalec_od=[]
            self.najemodajalec_do=[]
            self.najemodajalec_otroci=False
            self.najemodajalec_studenti=False
            self.najemodajalec_zivali=False
        if self.tip_stranke!='najemnik':
            self.poizvedba_nepremicnina=False
            self.poizvedba_kraj=False
            self.poizvedba_namen=False
            self.poizvedba_cena=0
            self.poizvedba_kontakt_dan=[]
            self.poizvedba_zgodovina=""
            self.poizvedba_ok=""
            self.poizvedba_nok=""
            self.poizvedba_kontaktiran=[]
            self.najemnik_osebe=0
            self.najemnik_dolzina=0
            self.najemnik_zgodovina=""
            self.najemnik_zaposlitev=""
            self.najemnik_studenti=False
            self.najemnik_zivali=False
            self.poizvedba_balkon=False
            self.poizvedba_dvigalo=False
            self.poizvedba_vrt=False
        if self.tip_stranke!=False and self.tretja_oseba!=True:
            self.objava_kje=[]
            self.objava_kje_datum=[]
            self.objava_odziv=""
            self.objava_spremembe=""
            self.objava_stevilo_ogledov=0
            self.spol=[]
            self.prodajalec_ponudbe=False
            self.prodajalec_ponudbe_info=""
            self.prodajalec_komunikacija=""
            self.kupec_narocnik=False
            self.kupec_aktiven=False
            self.kupec_znizana_cena=False
            self.tretja_oseba_osebnost=[]
        if (self.tip_stranke!="kupec" and self.tretja_oseba!=False) or (self.tip_stranke!="najemnik" and self.tretja_oseba!=False) or (self.tip_stranke!=False and self.tretja_oseba!=False):
            self.pridobitev=""
            self.stranka_odziv=""
            self.povprasevanje=""
            self.mnenje=""
            self.nepremicnine=False
    
    @api.onchange('objava_kje','prodajalec_ponudbe')
    def izbris(self):
        if self.objava_kje==False:
            self.objava_kje_datum=[]
        if self.prodajalec_ponudbe==False:
            self.prodajalec_ponudbe_info=""
  
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    def _get_default_currency_id_2(self):
        return self.env.user.company_id.currency_id.id
    
    @api.multi
    def _compute_opportunity_count(self):
        for nep in self:
            nep.opportunity_count=self.env['crm.lead'].search_count([('nepremicnina','=',nep.id), ('type', '=', 'opportunity')])
    
    custom_currency_id_2 = fields.Many2one('res.currency', 'Custom Currency', default=_get_default_currency_id_2)
    opportunity_count = fields.Integer("Opportunity", compute='_compute_opportunity_count')
    
    #POSREDNIŠKA POGOBDA
    @api.onchange('nepremicnina_pogodba_datum')
    def calculate_field(self):
        if self.nepremicnina_pogodba_datum:
            self.nepremicnina_potek_datum = self.nepremicnina_pogodba_datum + relativedelta(months=+1) + relativedelta(days=-1)
    
    nepremicnina_pogodba_datum = fields.Date(string = 'Sklenitev pogodbe')
    nepremicnina_potek_datum = fields.Date(string = 'Potek pogodbe')

    #POSREDOVANJE
    nepremicnina_vrsta_posredovanja=fields.Selection(string="Vrsta posredovanja", 
                                                     selection=[('prodamo','Prodamo'),
                                                                ('oddamo','Oddamo')])
    nepremicnina_novogradnja=fields.Boolean(string="Novogradnja")
    nepremicnina_etaza=fields.Char(string="Etaža")
    nepremicnina_se_prodaja=fields.Char(string="Nepremičnina se prodaja")
    nepremicnina_moznost_vselitve=fields.Char(string="Možnost vselitve")
    nepremicnina_pogoji_prodaje=fields.Selection(string="Pogoji prodaje", selection = [('1', '1'),
                                                                                      ('2','2'),
                                                                                      ('3','3'),
                                                                                      ('4','4')])
    nepremicnina_pogoji_prodaje_opis=fields.Char(string="Opis pogojev prodaje")
    nepremicnina_za_investicijo=fields.Boolean(string="Za investicijo")
    nepremicnina_oznake_nepremicnin=fields.Many2many(string="Oznake nepremičnine",
                              comodel_name="res.partner.category",
                              relation="contact_tag_oznake_nepremicnin_rel",
                              domain="[('tag_type','=','oznake_nepremicnin')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    nepremicnina_opis=fields.Html(string="Opis")
    #-----------------------------------------------------------------------------------------
    
    #SISTEM
    datum_objave=fields.Date(string="Datum objave")
    
    #------------------------------------------------------------------------------------------
    
    #WEBSITE
    website_published=fields.Boolean()
    is_published=fields.Boolean()
    
    #SLIKE
    slike_ids = fields.One2many(comodel_name='custom.image',  inverse_name="product_tmpl_id", string='Dodaj', domain=lambda self:[('prikaz','=','splet')])
    slike_arhiv = fields.One2many(comodel_name='custom.image',  inverse_name="product_tmpl_id", string='Dodaj', domain=lambda self:[('prikaz','=','arhiv')])
    slike_attachments = fields.Many2many('ir.attachment', string='Dodaj več')
    slike_kanban = fields.One2many(comodel_name='custom.image',  inverse_name="product_tmpl_id", string='Dodaj')
    help_tekst = fields.Char(string='Debugg')
        
    @api.multi
    def write(self,values):
        if 'slike_attachments' in values:
            ids = values['slike_attachments'][0][2]
            for id in ids:
                record = self.env['ir.attachment'].browse(id)
                if 'image' in record.mimetype:
                    self.env['custom.image'].create({'name':record.name, 'image':record.datas, 'product_tmpl_id':self.id})
            values['help_tekst'] = ids
            values['slike_attachments'] = [(5,)]
        rec = super(ExtendInventory,self).write(values)
        return rec
    
    @api.model
    def create(self,values):
        rec = super(ExtendInventory,self).create(values)
        records = rec['slike_attachments']
        for record in records:
            if 'image' in record.mimetype:
                self.env['custom.image'].create({'name':record.name, 'image':record.datas, 'product_tmpl_id':rec.id})
        rec['help_tekst'] = records
        rec['slike_attachments'] = False
        return rec
        
    #OSNOVNI PODATKI
    contact = fields.Many2one(comodel_name='res.partner',string="Kdo prodaja")
    nepremicnina_posrednik = fields.Many2one('res.users',string="Posrednik",default=lambda self: self.env.user)
    nepremicnina_povrsina = fields.Float(string='Uporabna površina') #m2
    #nepremicnina_zemljisce_pod = fields.Float(string = 'Zemljišče pod stavbo') #m2
    nepremicnina_velikost = fields.Float(string = 'Površina dela stavbe') #m2
    nepremicnina_cena_min = fields.Float(string = 'Minimalna cena') #EUR
    nepremicnina_cena_dolgorocno = fields.Float(string = 'Cena / Najemnina') #EUR
    nepremicnina_cena_dolgorocno_valuta=fields.Selection(string="Valuta", selection=[('e','EUR'),('em2','EUR/m²')])
    
        
    nepremicnina_vrsta = fields.Selection(string = 'Vrsta nepremičnine', selection = [('stanovanje', 'Stanovanje'), 
                                                                                      ('hisa', 'Hiša'), 
                                                                                      ('poslovni', 'Poslovni prostor'),
                                                                                      ('posest','Posest'),
                                                                                      ('vikend','Vikend'),
                                                                                      ('kmetija','Kmetija'), 
                                                                                      ('garaza', 'Garaža'), 
                                                                                      ('drugo', 'Drugo'),])
    nepremicnina_vrsta_drugo = fields.Char(string = 'Druga vrsta')
    nepremicnina_tip=fields.Selection(string="Tip nepremičnine", selection=[('apartma','Apartma'),
                                                                                  ('soba','Soba'),
                                                                                  ('garsonjera', 'Garsonjera'),
                                                                                  ('soba1','1-sobno'),
                                                                                  ('soba1_5', '1,5-sobno'),
                                                                                  ('soba2','2-sobno'),
                                                                                  ('soba2_5','2,5-sobno'),
                                                                                  ('soba3','3-sobno'),
                                                                                  ('soba3_5','3,5-sobno'),
                                                                                  ('soba4','4-sobno'),
                                                                                  ('soba4_5','4,5-sobno'),
                                                                                  ('soba5','5 in večsobno'),
                                                                                  ('atrij','Atrij'),
                                                                                  ('dvojcek','Dvojcek'),
                                                                                  ('samostojna','Samostojna'),
                                                                                  ('delavnica','Delavnica'),
                                                                                  ('gostinskiLokal','Gostinski lokal'),
                                                                                  ('pisarna','Pisarna'),
                                                                                  ('prostorZaStoritve','Prostor za storitve'),
                                                                                  ('skladisce','Skladišče'),
                                                                                  ('vecjiPoslovniKompleks','Večji poslovni kompleks'),
                                                                                  ('drugo','Drugo')])
    nepremicnina_tip_1 = fields.Selection(string = 'Tip nepremičnine 1', selection=[('apartma','Apartma'),
                                                                                  ('soba','Soba'),
                                                                                  ('garsonjera', 'Garsonjera'),
                                                                                  ('soba1','1-sobno'),
                                                                                  ('soba1_5', '1,5-sobno'),
                                                                                  ('soba2','2-sobno'),
                                                                                  ('soba2_5','2,5-sobno'),
                                                                                  ('soba3','3-sobno'),
                                                                                  ('soba3_5','3,5-sobno'),
                                                                                  ('soba4','4-sobno'),
                                                                                  ('soba4_5','4,5-sobno'),
                                                                                  ('soba5','5 in večsobno'),
                                                                                  ('drugo','Drugo')])
    
    nepremicnina_tip_2 = fields.Selection(string = 'Tip nepremičnine 2', selection=[('atrij','Atrij'),
                                                                                  ('dvojcek','Dvojcek'),
                                                                                  ('samostojna','Samostojna'),
                                                                                  ('drugo','Drugo')])
    
    nepremicnina_tip_3 = fields.Selection(string = 'Tip nepremičnine 3', selection=[('delavnica','Delavnica'),
                                                                                  ('gostinskiLokal','Gostinski lokal'),
                                                                                  ('pisarna','Pisarna'),
                                                                                  ('prostorZaStoritve','Prostor za storitve'),
                                                                                  ('skladisce','Skladišče'),
                                                                                  ('vecjiPoslovniKompleks','Večji poslovni kompleks'),
                                                                                  ('drugo','Drugo')])
    
    @api.onchange('nepremicnina_vrsta','nepremicnina_tip_1','nepremicnina_tip_2','nepremicnina_tip_3')
    def prepis_vrednosti(self):
        if self.nepremicnina_vrsta=='stanovanje':
            self.nepremicnina_tip_2=[]
            self.nepremicnina_tip_3=[]
            if self.nepremicnina_tip_1==False:
                self.nepremicnina_tip=[]
        if self.nepremicnina_vrsta=='hisa':
            self.nepremicnina_tip_1=[]
            self.nepremicnina_tip_3=[]
            if self.nepremicnina_tip_2==False:
                self.nepremicnina_tip=[]
        if self.nepremicnina_vrsta=='poslovni':
            self.nepremicnina_tip_1=[]
            self.nepremicnina_tip_2=[]
            if self.nepremicnina_tip_3==False:
                self.nepremicnina_tip=[]
        if self.nepremicnina_vrsta not in ['stanovanje','hisa','poslovni']:
            self.nepremicnina_tip=[]
            self.nepremicnina_tip_1=[]
            self.nepremicnina_tip_2=[]
            self.nepremicnina_tip_3=[]
        if self.nepremicnina_vrsta != 'hisa':
            self.nepremicnina_etaza = ""
        if self.nepremicnina_vrsta not in ['stanovanje', 'poslovni']:              
            self.nepremicnina_nadstropje = 0
            self.nepremicnina_st_nadstropij = 0
        if self.nepremicnina_tip_1:
            self.nepremicnina_tip=self.nepremicnina_tip_1
        if self.nepremicnina_tip_2:
            self.nepremicnina_tip=self.nepremicnina_tip_2
        if self.nepremicnina_tip_3:
            self.nepremicnina_tip=self.nepremicnina_tip_3

    nepremicnina_tip_drugo=fields.Char(string = 'Drug tip')
    #PODATKI O LOKACIJI
    nepremicnina_drzava = fields.Many2one('res.country', string = 'Država')
    nepremicnina_obcina = fields.Char(string = 'Poštna številka')
    nepremicnina_zip = fields.Char(string = 'Občina', placeholder='Občina')
    nepremicnina_lokacija = fields.Char(string = 'Točna Lokacija')
    nepremicnina_lokacija_opombe = fields.Char(string = 'Lokacija/opombe')
    
    #DODATNO O REGIJI IN UPRAVNI ENOTI
    nepremicnina_upravna_enota_test=fields.Many2one('custom.location', string="Upravna enota - test")
    
    nepremicnina_regija=fields.Selection(string ="Regija",
                                         selection=[('dolenjska','Dolenjska'),
                                                    ('gorenjska','Gorenjska'),
                                                    ('juzna_primorska','Južna primorska'),
                                                    ('severna_primorska','Severna primorska'),
                                                    ('koroska','Koroška'),
                                                    ('lj_mesto','Lj-mesto'),
                                                    ('lj_okolica','Lj-okolica'),
                                                    ('notranjska','Notranjska'),
                                                    ('podravska','Podravska'),
                                                    ('pomurska','Pomurska'),
                                                    ('posavska','Posavska'),
                                                    ('savinjska','Savinjska'),
                                                    ('zasavska','Zasavska')])
    nepremicnina_upravna_enota=fields.Selection(string="Upravna enota",
                                                selection=[('crnomelj','Črnomelj'),
                                                           ('kocevje','Kočevje'),
                                                           ('metlika','Metlika'),
                                                           ('novo_mesto','Novo mesto'),
                                                           ('ribnica','Ribnica'),
                                                           ('trebnje','Trebnje'),
                                                           ('jesenice','Jesenice'),
                                                           ('kranj','Kranj'),
                                                           ('radovljica','Radovljica'),
                                                           ('skofja_loka','Škofja loka'),
                                                           ('trzic','Tržič'),
                                                           ('izola','Izola'),
                                                           ('koper','Koper'),
                                                           ('piran','Piran'),
                                                           ('sezana','Sežana'),
                                                           ('ajdovscina','Ajdovščina'),
                                                           ('idrija','Idrija'),
                                                           ('nova_gorica','Nova Gorica'),
                                                           ('tolmin','Tolmin'),
                                                           ('dravograd','Dravograd'),
                                                           ('radlje_ob_dravi','Radlje ob Dravi'),
                                                           ('ravne_na_koroskem','Ravne na Koroškem'),
                                                           ('slovenj_gradec','Slovenj Gradec'),
                                                           ('bezigrad','Lj. Bežigrad'),
                                                           ('center','Lj. Center'),
                                                           ('moste_polje','Lj. Moste-Polje'),
                                                           ('siska','Lj. Šiška'),
                                                           ('vic_rudnik','Lj. Vič-Rudnik'),
                                                           ('domzale','Domžale'),
                                                           ('grosuplje','Grosuplje'),
                                                           ('kamnik','Kamnik'),('litija','Litija'),
                                                           ('lj_j_z','Lj. J&Z (Vič, Rudnik)'),
                                                           ('lj_s_v','Lj. SV del (Bežigrad)'),
                                                           ('lj_s_z','Lj. SZ del (Šiška)'),
                                                           ('lj_v','Lj. V del (Moste-Polje)'),
                                                           ('logatec','Logatec'),
                                                           ('vrhnika','Vrhnika'),
                                                           ('cerknica','Cerknica'),
                                                           ('ilirska_bistrica','Ilirska Bistrica'),
                                                           ('postojna','Postojna'),
                                                           ('lenart','Lenart'),
                                                           ('maribor','Maribor'),
                                                           ('ormoz','Ormož'),
                                                           ('pesnica','Pesnica'),
                                                           ('ptuj','Ptuj'),
                                                           ('ruse','Ruše'),
                                                           ('slovenska_bistrica','Slovenska bistrica'),
                                                           ('gornja_radgona','Gornja Radgona'),
                                                           ('lendava','Lendava'),
                                                           ('ljutomer','Ljutomer'),
                                                           ('murska_sobota','Murska Sobota'),
                                                           ('brezice','Brežice'),
                                                           ('krsko','Krško'),
                                                           ('sevnica','Sevnica'),
                                                           ('celje','Celje'),
                                                           ('lasko','Laško'),
                                                           ('mozirje','Mozirje'),
                                                           ('slovenske_konjica','Slovenske Konjice'),
                                                           ('sentjur','Šentjur'),
                                                           ('smarje_pri_jelsah','Šmarje pri Jelšah'),
                                                           ('velenje','Velenje'),
                                                           ('zalec','Žalec'),
                                                           ('hrastnik','Hrastnik'),
                                                           ('trbovlje','Trbovlje'),
                                                           ('zagorje_ob_savi','Zagorje ob Savi')])
    nepremicnina_upravne_enote_1=fields.Selection(string="Upravna_enota_dolenjska", 
                                                  selection=[('crnomelj','Črnomelj'),
                                                             ('kocevje','Kočevje'),
                                                             ('metlika','Metlika'),
                                                             ('novo_mesto','Novo mesto'),
                                                             ('ribnica','Ribnica'),
                                                             ('trebnje','Trebnje')])
    nepremicnina_upravne_enote_2=fields.Selection(string="Upravna_enota_gorenjska", 
                                                  selection=[('jesenice','Jesenice'),
                                                             ('kranj','Kranj'),
                                                             ('radovljica','Radovljica'),
                                                             ('skofja_loka','Škofja loka'),
                                                             ('trzic','Tržič')])
    nepremicnina_upravne_enote_3=fields.Selection(string="Upravna_enota_juzna_primorska", 
                                                  selection=[('izola','Izola'),
                                                             ('koper','Koper'),
                                                             ('piran','Piran'),
                                                             ('sezana','Sežana')])
    nepremicnina_upravne_enote_4=fields.Selection(string="Upravna_enota_severna_primorska", 
                                                  selection=[('ajdovscina','Ajdovščina'),
                                                             ('idrija','Idrija'),
                                                             ('nova_gorica','Nova Gorica'),
                                                             ('tolmin','Tolmin')])
    nepremicnina_upravne_enote_5=fields.Selection(string="Upravna_enota_koroska", 
                                                  selection=[('dravograd','Dravograd'),
                                                             ('radlje_ob_dravi','Radlje ob Dravi'),
                                                             ('ravne_na_koroskem','Ravne na Koroškem'),
                                                             ('slovenj_gradec','Slovenj Gradec')])
    nepremicnina_upravne_enote_6=fields.Selection(string="Upravna_enota_lj_mesto", 
                                                  selection=[('bezigrad','Lj. Bežigrad'),
                                                             ('center','Lj. Center'),
                                                             ('moste_polje','Lj. Moste-Polje'),
                                                             ('siska','Lj. Šiška'),
                                                             ('vic_rudnik','Lj. Vič-Rudnik')])
    nepremicnina_upravne_enote_7=fields.Selection(string="Upravna_enota_lj_okolica", 
                                                  selection=[('domzale','Domžale'),
                                                             ('grosuplje','Grosuplje'),
                                                             ('kamnik','Kamnik'),
                                                             ('litija','Litija'),
                                                             ('lj_j_z','Lj. J&Z (Vič, Rudnik)'),
                                                             ('lj_s_v','Lj. SV del (Bežigrad)'),
                                                             ('lj_s_z','Lj. SZ del (Šiška)'),
                                                             ('lj_v','Lj. V del (Moste-Polje)'),
                                                             ('logatec','Logatec'),
                                                             ('vrhnika','Vrhnika')])
    nepremicnina_upravne_enote_8=fields.Selection(string="Upravna_enota_notranjska", 
                                                  selection=[('cerknica','Cerknica'),
                                                             ('ilirska_bistrica','Ilirska Bistrica'),
                                                             ('postojna','Postojna')])
    nepremicnina_upravne_enote_9=fields.Selection(string="Upravna_enota_podravska", 
                                                  selection=[('lenart','Lenart'),
                                                             ('maribor','Maribor'),
                                                             ('ormoz','Ormož'),
                                                             ('pesnica','Pesnica'),
                                                             ('ptuj','Ptuj'),
                                                             ('ruse','Ruše'),
                                                             ('slovenska_bistrica','Slovenska bistrica')])
    nepremicnina_upravne_enote_10=fields.Selection(string="Upravna_enota_pomurska", 
                                                   selection=[('gornja_radgona','Gornja Radgona'),
                                                              ('lendava','Lendava'),
                                                              ('ljutomer','Ljutomer'),
                                                              ('murska_sobota','Murska Sobota')])
    nepremicnina_upravne_enote_11=fields.Selection(string="Upravna_enota_posavska", 
                                                   selection=[('brezice','Brežice'),
                                                              ('krsko','Krško'),
                                                              ('sevnica','Sevnica')])
    nepremicnina_upravne_enote_12=fields.Selection(string="Upravna_enota_savinjska", 
                                                   selection=[('celje','Celje'),
                                                              ('lasko','Laško'),
                                                              ('mozirje','Mozirje'),
                                                              ('slovenske_konjica','Slovenske Konjice'),
                                                              ('sentjur','Šentjur'),
                                                              ('smarje_pri_jelsah','Šmarje pri Jelšah'),
                                                              ('velenje','Velenje'),
                                                              ('zalec','Žalec')])
    nepremicnina_upravne_enote_13=fields.Selection(string="Upravna_enota_zasavska", 
                                                   selection=[('hrastnik','Hrastnik'),
                                                              ('trbovlje','Trbovlje'),
                                                              ('zagorje_ob_savi','Zagorje ob Savi')])

    
    @api.onchange('nepremicnina_regija','nepremicnina_upravna_enota','nepremicnina_upravne_enote_1','nepremicnina_upravne_enote_2','nepremicnina_upravne_enote_3','nepremicnina_upravne_enote_4','nepremicnina_upravne_enote_5','nepremicnina_upravne_enote_6','nepremicnina_upravne_enote_7','nepremicnina_upravne_enote_8','nepremicnina_upravne_enote_9','nepremicnina_upravne_enote_10','nepremicnina_upravne_enote_11','nepremicnina_upravne_enote_12','nepremicnina_upravne_enote_13',)
    def upravna_enota_selection(self):
        if self.nepremicnina_regija=="dolenjska":
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_1==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="gorenjska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_2==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="juzna_primorska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_3==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="severna_primorska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_4==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="koroska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_5==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="lj_mesto":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_6==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="lj_okolica":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_7==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="notranjska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_8==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="podravska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_9==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="pomurska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_10==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="posavska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_12=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_11==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="savinjska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_13=[]
            if self.nepremicnina_upravne_enote_12==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_regija=="zasavska":
            self.nepremicnina_upravne_enote_1=[]
            self.nepremicnina_upravne_enote_2=[]
            self.nepremicnina_upravne_enote_3=[]
            self.nepremicnina_upravne_enote_4=[]
            self.nepremicnina_upravne_enote_5=[]
            self.nepremicnina_upravne_enote_6=[]
            self.nepremicnina_upravne_enote_7=[]
            self.nepremicnina_upravne_enote_8=[]
            self.nepremicnina_upravne_enote_9=[]
            self.nepremicnina_upravne_enote_10=[]
            self.nepremicnina_upravne_enote_11=[]
            self.nepremicnina_upravne_enote_12=[]
            if self.nepremicnina_upravne_enote_13==False:
                self.nepremicnina_upravna_enota=[]
        if self.nepremicnina_upravne_enote_1:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_1
        if self.nepremicnina_upravne_enote_2:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_2
        if self.nepremicnina_upravne_enote_3:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_3
        if self.nepremicnina_upravne_enote_4:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_4
        if self.nepremicnina_upravne_enote_5:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_5
        if self.nepremicnina_upravne_enote_6:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_6
        if self.nepremicnina_upravne_enote_7:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_7
        if self.nepremicnina_upravne_enote_8:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_8
        if self.nepremicnina_upravne_enote_9:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_9
        if self.nepremicnina_upravne_enote_10:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_10
        if self.nepremicnina_upravne_enote_11:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_11
        if self.nepremicnina_upravne_enote_12:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_12
        if self.nepremicnina_upravne_enote_13:
            self.nepremicnina_upravna_enota=self.nepremicnina_upravne_enote_13

    #PODATKI O NADSTROPJIH
    nepremicnina_nadstropje = fields.Integer(string = 'Nadstropje')
    nepremicnina_st_nadstropij = fields.Integer(string = 'Št. nadstropij')
    nepremicnina_razlog_prodaje = fields.Char(string = 'Razlog za prodajo')
    
    
    #OPIS NEPREMIČNINE
    nepremicnina_adaptacija = fields.Boolean(string = 'Obnovljeno/adaptacija')
    nepremicnina_leto_izgradnje = fields.Char(string = 'Leto izgradnje')
    nepremicnina_leto_adaptacija = fields.Char(string = 'Leto adaptacije')
    nepremicnina_adaptacija_info = fields.Many2many(string="Kaj je bilo obnovljeno",
                              comodel_name="res.partner.category",
                              relation="contact_tag_obnova_rel",
                              domain="[('tag_type','=','obnova')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    nepremicnina_streha = fields.Char(string = 'Vrsta kritine')
    nepremicnina_streha_obnova = fields.Char(string = 'Leto obnove strehe')
    nepremicnina_izolacija = fields.Char(string = 'Fasada/izolacija')
    nepremicnina_izolacija_obnova = fields.Char(string = 'Leto obnove fasade')
    nepremicnina_okna = fields.Selection(string = 'Tip oken', selection=[('lesena','Lesena'), 
                                                                         ('plasticna','Plastična'),
                                                                         ('pol','Pol-pol')])
    nepremicnina_okna_obnova = fields.Char(string = 'Leto obnove/inštalacije oken')
    nepremicnina_materiali = fields.Char(string = 'Materiali')
    nepremicnina_stroski_poleti = fields.Float(string = 'Stroški vzdrževanja poleti') #EUR
    nepremicnina_stroski_pozimi = fields.Float(string = 'Stroški vzdrževanja pozimi') #EUR
    nepremicnina_stroski_sklada = fields.Float(string = 'Stroški rezervnega sklada') #EUR
    nepremicnina_stanje_sklada = fields.Char(string = 'Stanje rezervnega sklada')
    nepremicnina_upravnik = fields.Char(string = 'Upravnik') #mogoče: many2one na contacts?
    nepremicnina_energetski_razred = fields.Selection(string = 'Energijski razred',
                                                      selection=[('v_izdelavi','V izdelavi'),
                                                                 ('a1','A1 (0 - 10 kWh/m2a)'),
                                                                 ('a2','A2 (10 - 15 kWh/m2a)'),
                                                                 ('b1','B1 (15 - 25 kWh/m2a)'),
                                                                 ('b2','B2 (25 - 35 kWh/m2a)'),
                                                                 ('c','C (35 - 60 kWh/m2a)'),
                                                                 ('d','D (60 - 105 kWh/m2a)'),
                                                                 ('e','E (105 - 150 kWh/m2a)'),
                                                                 ('f','F (150 - 210 kWh/m2a)'),
                                                                 ('g','G (210+ kWh/m2a)'),
                                                                 ('merjena','Merjena EI'),
                                                                 ('ni_potrebna','EI ni potrebna (334.člen EZ-1)'),
                                                                 ('ni_mogoc','EI: Izračun ni mogoč'),])
    
    #DODATKI
    nepremicnina_balkon = fields.Boolean(string = 'Balkon')
    nepremicnina_balkon_velikost = fields.Float(string = 'Velikost Balkona') #hide if balkon False
    nepremicnina_balkon_info = fields.Char(string = 'Več o balkonu')
    
    #------------------------------------------------------------------------------------------------------
    nepremicnina_terasa = fields.Boolean(string='Terasa')
    nepremicnina_terasa_velikost=fields.Float(string='Velikost terase')
    nepremicnina_terasa_info = fields.Char(string = 'Več o terasi')
    #------------------------------------------------------------------------------------------------------
    
    nepremicnina_atrij = fields.Boolean(string = 'Atrij')
    
    nepremicnina_klet = fields.Boolean(string = 'Klet') #hide if Klet False
    nepremicnina_klet_velikost = fields.Float(string = 'Velikost kleti')
    nepremicnina_klet_info = fields.Char(string = 'Več o kleti')
    
    nepremicnina_dvigalo = fields.Boolean(string = 'Dvigalo')
    nepremicnina_vrsta_ogrevanja = fields.Selection(string = 'Vrsta ogrevanja', selection=[('skupnaKurilnica','Skupna kurilnica'),
                                                                                           ('plinovod','Plinovod'),
                                                                                           ('toplovod','Toplovod'),
                                                                                           ('elektrika','Elektrika'),
                                                                                           ('centralnaKurjava','Centralna kurjava'),
                                                                                           ('crpalka','Toplotna Črpalka'), 
                                                                                           ('biomasa','Biomasa'),
                                                                                           ('klimatskaNaprava','Klimatska naprava')
                                                                                           ])
    nepremicnina_lega = fields.Char(string = 'Lega')
    nepremicnina_sanitarije = fields.Boolean(string = 'Sanitarije')
    nepremicnina_sanitarije_info = fields.Char(string = 'Več o sanitarijah')
    
    nepremicnina_hodnik = fields.Boolean(string = 'Hodnik')
    nepremicnina_hodnik_info = fields.Char(string = 'Več o hodniku')
    
    nepremicnina_spalnice = fields.Boolean(string = 'Spalnice')
    nepremicnina_spalnice_info = fields.Char(string = 'Več o spalnicah')
    
    nepremicnina_dnevna = fields.Boolean(string = 'Dnevne sobe')
    nepremicnina_dnevna_info = fields.Char(string = 'Več o dnevni sobi')
    
    nepremicnina_kuhinja = fields.Boolean(string = 'Kuhinja')
    nepremicnina_kuhinja_info = fields.Char(string = 'Več o kuhinji')
    
    nepremicnina_jedilnica = fields.Boolean(string = 'Jedilnica')
    nepremicnina_jedilnica_info = fields.Char(string = 'Več o jedilnici')
    
    nepremicnina_kopalnica = fields.Boolean(string = 'Kopalnica')
    nepremicnina_kopalnica_info = fields.Char(string = 'Več o kopalnici')
    
    nepremicnina_garderoba = fields.Boolean(string = 'Garderoba')
    nepremicnina_garderoba_info = fields.Char(string = 'Več o garderobi')
    
    nepremicnina_soba1 = fields.Boolean(string = 'Soba 1')
    nepremicnina_soba1_info = fields.Char(string = 'Več o sobi 1')
    
    nepremicnina_soba2 = fields.Boolean(string = 'Soba 2')
    nepremicnina_soba2_info = fields.Char(string = 'Več o sobi 2')
    
    nepremicnina_pritlicje = fields.Boolean(string = 'Pritličje')
    nepremicnina_pritlicje_info = fields.Char(string = 'Več o pritličju')
    
    nepremicnina_vrt = fields.Boolean(string = 'Vrt')
    nepremicnina_vrt_info = fields.Char(string = 'Več o vrtu')
    
    nepremicnina_bazen = fields.Boolean(string = 'Bazen')
    nepremicnina_kamin = fields.Boolean(string = 'Kamin') 
    nepremicnina_razgled = fields.Char(string = 'Razgled')
    nepremicnina_penthouse = fields.Boolean(string = 'Penthouse')
    nepremicnina_ljubljencki = fields.Boolean(string = 'Hišni ljubljenčki')
    nepremicnina_shramba = fields.Boolean(string = 'Shramba')
    nepremicnina_opremljeno = fields.Boolean(string = 'Opremljeno')
    nepremicnina_invalidi = fields.Boolean(string = 'Dostop za invalide')
    nepremicnina_pogled = fields.Char(string = 'Pogled na')
    nepremicnina_student = fields.Boolean(string = 'Primerno za študente')
    nepremicnina_parkiranje = fields.Boolean(string = 'Parkiranje')
    nepremicnina_parkiranje_vrsta = fields.Char(string = 'Vrsta parkiranja')
    nepremicnina_parkiranje_stevilo = fields.Integer(string = 'Število mest')
    nepremicnina_klima = fields.Boolean(string = 'Klima')
    nepremicnina_alarm = fields.Boolean(string = 'Alarm')
    nepremicnina_varovanje = fields.Boolean(string = 'Varovan objekt')
    nepremicnina_video_nadzor = fields.Boolean(string = 'Video Nadzor')
    nepremicnina_domofon = fields.Boolean(string = 'Domofon')
    nepremicnina_360_id = fields.Boolean(string = '360 View ID')
   
    #INFRASTRUKTURA
    infrastruktura_vrtec = fields.Boolean(string = 'Vrtec')
    infrastruktura_vrtec_info = fields.Char(string = 'Več o vrtcih')
  
    infrastruktura_sola = fields.Boolean(string = 'Šola')
    infrastruktura_sola_info = fields.Char(string = 'Več o šolah')
    
    infrastruktura_fakultete = fields.Boolean(string = 'Fakulteta')
    infrastruktura_fakultete_info = fields.Char(string = 'Več o fakultetah')
    
    infrastruktura_posta = fields.Boolean(string = 'Pošta')
    infrastruktura_posta_info = fields.Char(string = 'Več o poštah')
    
    infrastruktura_trgovina = fields.Boolean(string = 'Trgovina')
    infrastruktura_trgovina_info = fields.Char(string = 'Več o trgovinah')
    
    infrastruktura_banka = fields.Boolean(string = 'Banka')
    infrastruktura_banka_info = fields.Char(string = 'Več o bankah')
    
    infrastruktura_avtocesta = fields.Boolean(string = 'Avtocesta')
    infrastruktura_avtocesta_info = fields.Char(string = 'Več o avtocestah')
    
    infrastruktura_avtobus = fields.Boolean(string = 'Avtobus')
    infrastruktura_avtobus_info = fields.Char(string = 'Več o avtobusih')
    
    infrastruktura_vlak = fields.Boolean(string = 'Vlak')
    infrastruktura_vlak_info = fields.Char(string = 'Več o vlakih')
    
    infrastruktura_igrisce = fields.Boolean(string = 'Igrišče')
    infrastruktura_igrisce_info = fields.Char(string = 'Več o igriščih')
    
    infrastruktura_park = fields.Boolean(string = 'Park')
    infrastruktura_park_info = fields.Char(string = 'Več o parkih')
    
    infrastruktura_zd = fields.Boolean(string = 'Zdravstveni dom')
    infrastruktura_zd_info = fields.Char(string = 'Več o zdravstvenih domovih')
    
    #KOMUNIKACIJSKI PRIKLJUČKI
    komunikacija_telefon = fields.Boolean(string = 'Telefon')
    komunikacija_telefon_info = fields.Char(string = 'Informacije o ponudniku telefonije')
    
    komunikacija_kabel = fields.Boolean(string = 'Kabel')
    komunikacija_kabel_info = fields.Char(string = 'Informacije o kabelskem ponudniku')
    
    komunikacija_optika = fields.Boolean(string = 'Optika')
    komunikacija_optika_info = fields.Char(string = 'Informacije o ponudniku optike')
    
    komunikacija_internet = fields.Boolean(string = 'Internet')
    komunikacija_internet_info = fields.Char(string = 'Informacije o ponudniku interneta')
    
    #LASTNIŠTVO
    lastnistvo_podlaga = fields.Char(string = 'Lastništvo pridobljeno na podlagi')
    lastnistvo_dan = fields.Char(string = 'Dne:')
    lastnistvo_plombe = fields.Char(string = 'Plombe:')
    lastnistvo_hipoteke = fields.Char(string = 'Hipoteke:')
    lastnistvo_solastnina = fields.Char(string = 'Solastnina')
    lastnistvo_prepoved = fields.Char(string = 'Prepoved odtujitve/obremenitve')
    lastnistvo_predkupna_pravica = fields.Char(string = 'Predkupna pravica')
    lastnistvo_parcelne_st = fields.Char(string = 'Parcelne številke')
    lastnistvo_omejitve = fields.Char(string = 'Omejitve po ZKZ')
    
    #PREDKUPNE PRAVICE
    lastnistvo_potrdilo = fields.Char(string = 'Potrdilo o namenski rabi/lokacijska info')
    lastnistvo_pravica = fields.Char(string = 'Predkupna pravica občine ali drugega upravičenca')
    lastnistvo_soglasje = fields.Char(string = 'ARSO soglasje')
    lastnistvo_varstvo = fields.Char(string = 'Varstvo naravne ali kulturne dediščine')
    lastnistvo_prikljucek = fields.Char(string = 'Mestni priključek')
    lastnistvo_vrednost = fields.Char(string = 'GURS vrednost')
    
    @api.multi
    def word_count(self, opis):
        x=opis.count(' ')
        if x<100:
            return True
        else:
            return False
    
    @api.multi
    def check_publish_info(self):
        _errorMsg_start='Manjkajoči podatki: \n'
        _errorMsg=''
        _errorMsg_word_count=''
        _errorMsg_Full=''
        _error=False
        _errorMsg_word_count_error=False
        #gre iz true v false
        if self.website_published == True:
            self.website_published = False
        #gre iz false v true
        else:
            if self.nepremicnina_vrsta==False:
                _errorMsg=_errorMsg + " - Vrsta nepremičnine \n"
                _error=True
            if self.nepremicnina_povrsina==False:
                _errorMsg=_errorMsg + " - Uporabna površina \n"
                _error=True
            if self.nepremicnina_lokacija==False:
                _errorMsg=_errorMsg + " - Ulica \n"
                _error=True
            if self.nepremicnina_obcina==False:
                _errorMsg=_errorMsg + " - Občina \n"
                _error=True
            if self.nepremicnina_zip==False:
                _errorMsg=_errorMsg + " - Poštna številka \n"
                _error=True
            if self.nepremicnina_drzava==False:
                _errorMsg=_errorMsg + " - Država \n"
                _error=True
            if self.nepremicnina_regija==False:
                _errorMsg=_errorMsg + " - Regija \n"
                _error=True
            if self.nepremicnina_upravna_enota==False:
                _errorMsg=_errorMsg + " - Upravna enota \n"
                _error=True
            if self.nepremicnina_leto_izgradnje==False:
                _errorMsg=_errorMsg + " - Leto izgradnje \n"
                _error=True
            if self.nepremicnina_cena_dolgorocno==False:
                if self.nepremicnina_adaptacija==False:
                    _errorMsg=_errorMsg + " - Cena/najemnina \n"
                    _error=True
            if self.nepremicnina_opis==False:
                _errorMsg=_errorMsg + " - Opis \n"
                _error=True
            if self.nepremicnina_energetski_razred==False or self.nepremicnina_energetski_razred=='v_izdelavi':
                _errorMsg=_errorMsg + " - Energijski razred \n"
                _error=True
            if self.nepremicnina_adaptacija==True:
                if self.nepremicnina_leto_adaptacija==False:
                    _errorMsg=_errorMsg + " - Leto adaptacije \n"
                    _error=True
            if self.word_count(self.nepremicnina_opis)==True:
                _errorMsg_word_count="\nPrekratek opis. Prosim dopolni."
                _errorMsg_word_count_error=True
            if _error==True:
                if _errorMsg_word_count_error==True:
                    _errorMsg=_errorMsg+_errorMsg_word_count
                _errorMsg_Full=_errorMsg_start+_errorMsg
                raise exceptions.UserError(_errorMsg_Full)
            else:
                self.website_published = True
                
    @api.onchange('nepremicnina_adaptacija','nepremicnina_balkon','nepremicnina_terasa','nepremicnina_sanitarije','nepremicnina_klet','nepremicnina_vrt', 'nepremicnina_vrsta','nepremicnina_hodnik','nepremicnina_spalnice','nepremicnina_dnevna','nepremicnina_kuhinja','nepremicnina_jedilnica','nepremicnina_kopalnica','nepremicnina_garderoba','nepremicnina_soba1','nepremicnina_soba2','nepremicnina_pritlicje')
    def izbris_nepremicnina(self):
        if self.nepremicnina_adaptacija==False:
            self.nepremicnina_leto_adaptacija=""
            self.nepremicnina_adaptacija_info=[]
            self.nepremicnina_streha_obnova=""
            self.nepremicnina_izolacija_obnova=""
            self.nepremicnina_okna_obnova=""
        if self.nepremicnina_balkon==False:
            self.nepremicnina_balkon_velikost=0
            self.nepremicnina_balkon_info=""
        if self.nepremicnina_terasa==False:
            self.nepremicnina_terasa_velikost=0
            self.nepremicnina_terasa_info=""
        if self.nepremicnina_sanitarije==False:
            self.nepremicnina_sanitarije_info=""
        if self.nepremicnina_klet==False:
            self.nepremicnina_klet_velikost=0
            self.nepremicnina_klet_info=""
        if self.nepremicnina_vrt==False:
            self.nepremicnina_vrt_info=""
        if self.nepremicnina_hodnik==False:
            self.nepremicnina_hodnik_info=""
        if self.nepremicnina_spalnice==False:
            self.nepremicnina_spalnice_info=""
        if self.nepremicnina_dnevna==False:
            self.nepremicnina_dnevna_info=""
        if self.nepremicnina_kuhinja==False:
            self.nepremicnina_kuhinja_info=""
        if self.nepremicnina_jedilnica==False:
            self.nepremicnina_jedilnica_info=""
        if self.nepremicnina_kopalnica==False:
            self.nepremicnina_kopalnica_info=""
        if self.nepremicnina_garderoba==False:
            self.nepremicnina_garderoba_info=""
        if self.nepremicnina_soba1==False:
            self.nepremicnina_soba1_info=""
        if self.nepremicnina_soba2==False:
            self.nepremicnina_soba2_info=""
        if self.nepremicnina_pritlicje==False:
            self.nepremicnina_pritlicje_info=""
            
    @api.onchange('infrastruktura_vrtec','infrastruktura_fakultete','infrastruktura_trgovina','infrastruktura_avtocesta','infrastruktura_vlak','infrastruktura_park','infrastruktura_sola','infrastruktura_posta','infrastruktura_banka','infrastruktura_avtobus','infrastruktura_igrisce','infrastruktura_zd')
    def izbris_infrastruktura(self):
        if self.infrastruktura_vrtec==False:
            self.infrastruktura_vrtec_info=""        
        if self.infrastruktura_fakultete==False:
            self.infrastruktura_fakultete_info=""
        if self.infrastruktura_trgovina==False:
            self.infrastruktura_trgovina_info=""
        if self.infrastruktura_avtocesta==False:
            self.infrastruktura_avtocesta_info=""
        if self.infrastruktura_vlak==False:
            self.infrastruktura_vlak_info=""
        if self.infrastruktura_park==False:
            self.infrastruktura_park_info=""
        if self.infrastruktura_sola==False:
            self.infrastruktura_sola_info=""
        if self.infrastruktura_posta==False:
            self.infrastruktura_posta_info=""
        if self.infrastruktura_banka==False:
            self.infrastruktura_banka_info=""
        if self.infrastruktura_avtobus==False:
            self.infrastruktura_avtobus_info=""
        if self.infrastruktura_igrisce==False:
            self.infrastruktura_igrisce_info=""
        if self.infrastruktura_zd==False:
            self.infrastruktura_zd_info=""
    
    @api.onchange('komunikacija_telefon','komunikacija_kabel','komunikacija_optika','komunikacija_internet')
    def izbris_komunikacija(self):
        if self.komunikacija_telefon==False:
            self.komunikacija_telefon_info=""
        if self.komunikacija_kabel==False:
            self.komunikacija_kabel_info=""
        if self.komunikacija_optika==False:
            self.komunikacija_optika_info=""
        if self.komunikacija_internet==False:
            self.komunikacija_internet_info=""
            
    @api.multi
    def crm_link(self):
        ctx=dict(self._context)
        return {'view_type': 'kanban',
                "view_mode": 'kanban,list',
                'res_model': 'crm.lead',
                'name':"CRM",
                'type': 'ir.actions.act_window',
                'context': ctx,
                'domain':[('nepremicnina','=',self.id)]
               }
            
class ExtendContactTags(models.Model):   
    _inherit = 'res.partner.category'
    
    tag_type = fields.Selection(string='Type', selection=[('nepremicnina','Nepremičnina'), 
                                                          ('lokacija','Lokacija'),
                                                          ('namen', 'Namen'),
                                                          ('ponudba','Ponudba'), 
                                                          ('stranka', 'Stranka'), 
                                                          ('lastnosti','Osebnostne lastnosti'),
                                                          ('obnova', 'Obnova'),
                                                          ('oznake_nepremicnin','Oznake nepremičnin')])
    color = fields.Integer(compute='_compute_first',string='Color Index', store=True, readonly=True)
    
    @api.depends('tag_type')
    def _compute_first(self):
        for record in self:
            if record.tag_type == 'nepremicnina':
                record.color = 1
            elif record.tag_type == 'lokacija':
                record.color = 2
            elif record.tag_type == 'namen':
                record.color = 3
            elif record.tag_type == 'ponudba':
                record.color = 4
            elif record.tag_type == 'stranka':
                record.color = 5
            elif record.tag_type == 'lastnosti':
                record.color = 6
            elif record.tag_type == 'obnova':
                record.color = 1
            elif record.tag_type == 'oznake_nepremicnin':
                record.color = 3
            else:
                record.color = 0
                
class ExtendCrm(models.Model):   
    _inherit = 'crm.lead'
    
    nepremicnina = fields.Many2one(comodel_name="product.template", string="Nepremičnina")
    tip_priloznosti = fields.Selection(string="Tip priložnosti", 
                                       selection=[('navadno','Navadno'),
                                                  ('zasebno','Zasebno')],
                                       default='navadno')
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models, tools

class ExtendContacts(models.Model):
    _inherit = ['res.partner']
    
    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id
    
    #OSNOVNI REQUIRED PODATKI
    tip_stranke = fields.Selection(selection=[('prodajalec', 'Prodajalec'),
                                              ('kupec', 'Kupec'),
                                              ('najemodajalec', 'Najemodajalec'),
                                              ('najemnik', 'Najemnik')])
    spol = fields.Selection(selection=[('moski', 'Moški'),('ženski', 'Ženski')])
    tretja_oseba = fields.Boolean(string = 'Tretja Oseba')
    custom_currency_id = fields.Many2one('res.currency', 'Currency', default=_get_default_currency_id, required=True)
    
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
    poizvedba_namen = fields.Many2many(string="Namen",
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
    prodajalec_koliko = fields.Float(string = 'Minimalna ponudba') #EUR
    prodajalec_ponudbe = fields.Boolean(string = 'Ponudbe')
    prodajalec_ponudbe_info = fields.Char(string = 'Kakšne ponudbe')
    prodajalec_procent = fields.Float(string = 'Procent od prodaje')
    prodajalec_datum_pogodbe = fields.Date(string = 'Posredniška pogodba / datum')
    prodajalec_komunikacija = fields.Char(string = 'Način komunikacije')
    
    #PODATKI O KUPCIH
    kupec_obvescanje = fields.Many2many(string="Obveščanje za ponudbe",
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
    najemodajalec_zivali = fields.Boolean(string = 'Živali')
    
    
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
    
    tretja_oseba_obvescanje = fields.Many2many(string="Obveščanje test",
                                               comodel_name="res.partner.category",
                                               relation="contact_tretja_oseba_tag_ponudba_rel",
                                               domain="[('tag_type','=','ponudba')]",
                                               options="{'color_field': 'color', 'no_create_edit': True}",
                                               track_visibility='onchange')
    
    @api.onchange('tip_stranke','tretja_oseba')
    def erase_fields(self):
        if self.tip_stranke!='prodajalec':
            self.objava_kje=[]
            self.objava_kje_datum=[]
            self.objava_odziv=""
            self.objava_spremembe=""
            self.objava_stevilo_ogledov=0
            if self.tretja_oseba!=True:
                self.prodajalec_koliko=0
                self.prodajalec_ponudbe=False
                self.prodajalec_ponudbe_info=""
                self.prodajalec_procent=0
                self.prodajalec_datum_pogodbe=[]
                self.prodajalec_komunikacija=""
        elif self.tip_stranke!='kupec':
            self.poizvedba_nepremicnina=[]
            self.poizvedba_kraj=[]
            self.poizvedba_namen=[]
            self.poizvedba_cena=0
            self.poizvedba_kontakt_dan=[]
            self.poizvedba_zgodovina=""
            self.poizvedba_ok=""
            self.poizvedba_nok=""
            self.poizvedba_kontaktiran=[]
            self.kupec_obvescanje=[]
            self.kupec_narocnik=False
            self.kupec_aktiven=False
            self.kupec_znizana_cena=False
        elif self.tip_stranke!='najemodajalec':
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
        elif self.tip_stranke!='najemnik':
            self.poizvedba_nepremicnina=[]
            self.poizvedba_kraj=[]
            self.poizvedba_namen=[]
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
        elif self.tip_stranke==False:
            self.pridobitev=""
            self.stranka_odziv=""
            self.povprasevanje=""
            self.mnenje=""
            self.nepremicnine=[]
        if self.tretja_oseba!=True:
            self.objava_kje=[]
            self.objava_kje_datum=[]
            self.objava_odziv=""
            self.objava_spremembe=""
            self.objava_stevilo_ogledov=0
            self.spol=[]
            self.tretja_oseba_namen
            self.prodajalec_koliko=0
            self.prodajalec_ponudbe=False
            self.prodajalec_ponudbe_info=""
            self.prodajalec_procent=0
            self.prodajalec_datum_pogodbe=[]
            self.prodajalec_komunikacija=""
            self.kupec_narocnik=False
            self.kupec_aktiven=False
            self.kupec_znizana_cena=False
            self.tretja_oseba_osebnost=[]   
    
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    #OSNOVNI PODATKI
    contact = fields.Many2one(comodel_name="res.partner", string="Kdo prodaja")
    nepremicnina_povrsina = fields.Float(string='Neto površina') #m2
    nepremicnina_zemljisce_pod = fields.Float(string = 'Zemljišče pod stavbo') #m2
    nepremicnina_velikost = fields.Float(string = 'Velikost skupaj') #m2
    nepremicnina_cena_min = fields.Float(string = 'Minimalna cena') #EUR
    nepremicnina_cena_dolgorocno = fields.Float(string = 'Cena / dolgoročni najem') #EUR
    nepremicnina_vrsta = fields.Selection(string = 'Vrsta nepremičnine', selection = [('stanovanje', 'Stanovanje'), 
                                                                                      ('hisa', 'Hiša'), 
                                                                                      ('poslovni', 'Poslovni prostor'), 
                                                                                      ('garaza', 'Garaža'), 
                                                                                      ('drugo', 'Drugo')])
    nepremicnina_vrsta_tip_drugo = fields.Char(string = 'Drugo')
    nepremicnina_tip = fields.Selection(string = 'Tip nepremičnine', selection = [('apartma','Apartma'),('soba','Soba'), 
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
    #PODATKI O LOKACIJI
    nepremicnina_drzava = fields.Many2one('res.country', string = 'Država')
    nepremicnina_regija = fields.Char(string = 'Regija')
    nepremicnina_obcina = fields.Char(string = 'Poštna številka')
    nepremicnina_zip = fields.Char(string = 'Občina', placeholder='Občina')
    nepremicnina_soseska = fields.Char(string = 'Soseska', placeholder = 'Soseska')
    nepremicnina_lokacija = fields.Char(string = 'Točna Lokacija')
    nepremicnina_lokacija_opombe = fields.Char(string = 'Lokacija/opombe')
    
    #PODATKI O NADSTROPJIH
    nepremicnina_nadstropje = fields.Integer(string = 'Nadstropje')
    nepremicnina_st_nadstropij = fields.Integer(string = 'Št. nadstropij')
    nepremicnina_razlog_prodaje = fields.Char(string = 'Razlog za prodajo')
    nepremicnina_razlog_oddala = fields.Char(string = 'Razlog zakaj se ni oddala')
    nepremicnina_razlog_oddala = fields.Char(string = 'Opis nepremičnine')
    
    #OPIS NEPREMIČNINE
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
    nepremicnina_stroski = fields.Float(string = 'Stroški vzdrževanja') #EUR
    nepremicnina_stroski = fields.Float(string = 'Stroški rezervnega sklada') #EUR
    nepremicnina_upravnik = fields.Char(string = 'Upravnik') #mogoče: many2one na contacts?
    nepremicnina_energetska_izkaznica = fields.Char(string = 'Energetska izkaznica')
    nepremicnina_energetski_razred = fields.Char(string = 'Energijski razred')
    
    #DODATKI
    nepremicnina_balkon = fields.Boolean(string = 'Balkon')
    nepremicnina_balkon_velikost = fields.Float(string = 'Velikost Balkona') #hide if balkon False
    
    nepremicnina_atrij = fields.Boolean(string = 'Atrij')
    
    nepremicnina_klet = fields.Boolean(string = 'Klet') #hide if Klet False
    nepremicnina_klet_velikost = fields.Float(string = 'Velikost kleti')
    
    nepremicnina_dvigalo = fields.Boolean(string = 'Dvigalo')
    nepremicnina_vrsta_ogrevanja = fields.Selection(string = 'Vrsta ogrevanja', selection=[('plinovod','Plinovod'),
                                                                                           ('toplovod','Toplovod'),
                                                                                           ('crpalka','Toplotna Črpalka'), 
                                                                                           ('biomasa','Biomasa')])
    nepremicnina_lega = fields.Char(string = 'Lega')
    
    nepremicnina_sanitarije = fields.Boolean(string = 'Sanitarije')
    nepremicnina_sanitarije_info = fields.Char(string = 'Več o sanitarijah')
    
    nepremicnina_dnevna = fields.Char(string = 'Dnevne sobe')
    nepremicnina_spalnice = fields.Char(string = 'Spalnice')
    nepremicnina_bazen = fields.Boolean(string = 'Bazen')
    nepremicnina_kamin = fields.Boolean(string = 'Kamin') 
    
    nepremicnina_vrt = fields.Boolean(string = 'Vrt')
    nepremicnina_vrt_info = fields.Char(string = 'Več o vrtu')
    
    nepremicnina_razgled = fields.Char(string = 'Razgled')
    nepremicnina_penthouse = fields.Boolean(string = 'Penthouse')
    nepremicnina_ljubljencki = fields.Boolean(string = 'Hišni ljubljenčki')
    nepremicnina_shramba = fields.Boolean(string = 'Shramba')
    nepremicnina_opremljeno = fields.Boolean(string = 'Opremljeno')
    nepremicnina_invalidi = fields.Boolean(string = 'Dostop za invalide')
    nepremicnina_pogled = fields.Selection(string = 'Pogled na', selection=[('morje','Morje'),
                                                                            ('hribi','Hribi')])
    nepremicnina_student = fields.Boolean(string = 'Primerno za študente')
    nepremicnina_parkiranje = fields.Char(string = 'Parkiranje')
    nepremicnina_garaza = fields.Char(string = 'Garaža')
    nepremicnina_parkiranje_mesto = fields.Char(string = 'Parkirno mesto')
    nepremicnina_parkiranje_hisa = fields.Char(string = 'Parkirna hiša')
    nepremicnina_klima = fields.Char(string = 'Klima')
    nepremicnina_alarm = fields.Char(string = 'Alarm')
    nepremicnina_varovanje = fields.Char(string = 'Varovan objekt')
    nepremicnina_video_nadzor = fields.Char(string = 'Video Nadzor')
    nepremicnina_domofon = fields.Char(string = 'Domofon')
    nepremicnina_360_id = fields.Char(string = '360 View ID')
   
    #INFRASTRUKTURA
    infrastruktura_vrtec = fields.Boolean(string = 'Vrtec')
    infrastruktura_vrtec_info = fields.Char(string = 'Več o vrtcih')
  
    infrastruktura_sola = fields.Boolean(string = 'Šola')
    infrastruktura_sola_info = fields.Char(string = 'Več o šolah')
    
    infrastruktura_fakultete = fields.Boolean(string = 'Fakulteta')
    infrastruktura_vrtec_info = fields.Char(string = 'Več o fakultetah')
    
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
    
    #SEZNAM OPREME
    #kuhinja, dnevna soba, spalnica, otroška soba, hodnik, kopalnica
    oprema_seznam = fields.Many2many(string="Seznam opreme, ki je vključena v ceno",
                              comodel_name="res.partner.category",
                              relation="contact_tag_oprema_rel",
                              domain="[('tag_type','=','oprema')]",
                              options="{'color_field': 'color', 'no_create_edit': True}",
                              track_visibility='onchange')
    
    
class ExtendContactTags(models.Model):   
    _inherit = 'res.partner.category'
    
    tag_type = fields.Selection(string='Type', selection=[('nepremicnina','Nepremičnina'), 
                                                          ('lokacija','Lokacija'),
                                                          ('namen', 'Namen'),
                                                          ('ponudba','Ponudba'), 
                                                          ('stranka', 'Stranka'), 
                                                          ('lastnosti','Osebnostne lastnosti'),
                                                          ('obnova', 'Obnova')])
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
                record.color = 7
            else:
                record.color = 0
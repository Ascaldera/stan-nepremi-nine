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
    mnenje = fields.Char(string = 'Naše mnenje')
    
    #PODATKI O ISKANJU
    #poizvedba_nepremicnina = fields.Char(string = 'Kaj išče')
    #poizvedba_kraj = fields.Char(string = 'Kje išče')
    #poizvedba_namen = fields.Char(string = 'Namen')
    poizvedba_cena = fields.Float(string = 'Cena')
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
    prodajalec_koliko = fields.Float(string = 'Minimalna ponudba')
    prodajalec_ponudbe = fields.Boolean(string = 'Ponudbe')
    prodajalec_ponudbe_info = fields.Char(string = 'Kakšne ponudbe')
    prodajalec_procent = fields.Float(string = 'Procent od prodaje')
    prodajalec_datum_pogodbe = fields.Date(string = 'Posredniška pogodba / datum')
    prodajalec_komunikacija = fields.Char(string = 'Način komunikacije')
    
    #PODATKI O KUPCIH
    #kupec_obvescanje = fields.Char(string = 'Obveščanje za ponudbe')
    kupec_naronik = fields.Boolean(string = 'Naročnik')
    kupec_aktiven = fields.Boolean(string = 'Aktivni kupec')
    kupec_znizana_cena = fields.Boolean(string = 'Znižana cena po oddani ponudbi') 
    
    #PODATKI O NAJEMODAJALCIH
    #najemodajalec_komu = fields.Char(string = 'Komu oddajajo')
    najemodajalec_od = fields.Date(string = 'Od kdaj oddaja')
    najemodajalec_do = fields.Date(string = 'Do kdaj oddaja')
    najemodajalec_otroci = fields.Boolean(string = 'Otroci')
    najemodajalec_studenti = fields.Boolean(string = 'Študenti')
    najemodajalec_zivali = fields.Boolean(string = 'Živali')
    
    
    #PODATKI O NAJEMNIKIH
    najemnik_osebe = fields.Integer(string = 'Koliko oseb')
    najemnik_dolzina = fields.Integer(string = 'Dolžina najema v mesecih')
    najemnik_zgodovina = fields.Char(string = 'Kje so živeli')
    najemnik_zaposlitev = fields.Char(string = 'Zaposlitev')
    najemnik_studenti = fields.Boolean(string = 'Študent')
    najemnik_zivali = fields.Boolean(string = 'Živali')
    
    contact_tags = fields.Many2many('res.partner.category','res_partner_res_partner_category_rel','category_id','partner_id','Contact Tags')
        
    
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    contact = fields.Many2one(comodel_name="res.partner", string="Kdo prodaja")
    nepremicnina_povrsina = fields.Float(string='Neto površina')
    nepremicnina_zemljisce_pod = fields.Float(string = 'Zemljišče pod stavbo')
    nepremicnina_velikost = fields.Float(string = 'Velikost skupaj')
    nepremicnina_cena_min = fields.Float(string = 'Minimalna cena')
    nepremicnina_cena_dolgorocno = fields.Float(string = 'Cena / dolgoročni najem')
    nepremicnina_vrsta = fields.Selection(string = 'Vrsta nepremičnine', selection = [('stanovanje', 'Stanovanje'), 
                                                                                      ('hisa', 'Hiša'), 
                                                                                      ('poslovni', 'Poslovni prostor'), 
                                                                                      ('garaza', 'Garaža'), 
                                                                                      ('drugo', 'Drugo')])
    nepremicnina_vrsta_tip_drugo = fields.Char(string = 'Drugo')
    nepremicnina_vrsta = fields.Selection(string = 'Tip nepremičnine', selection = [('apartma','Apartma'),('soba','Soba'), 
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
    nepremicnina_drzava = fields.Char(string = 'Država')
    nepremicnina_regija = fields.Char(string = 'Regija')
    nepremicnina_obcina = fields.Char(string = 'Občina')
    nepremicnina_soseska = fields.Char(string = 'Soseska')
    nepremicnina_lokacija = fields.Char(string = 'Točna Lokacija')
    nepremicnina_lokacija_opombe = fields.Char(string = 'Lokacija/opombe')
    nepremicnina_nadstropje = fields.Integer(string = 'Nadstropje')
    nepremicnina_st_nadstropij = fields.Integer(string = 'Št. nadstropij')
    nepremicnina_razlog_prodaje = fields.Char(string = 'Razlog za prodajo')
    nepremicnina_razlog_oddala = fields.Char(string = 'Razlog zakaj se ni oddala')
    
class ExtendContactTags(models.Model):   
    _inherit = 'res.partner.category'
    
    tag_type = fields.Selection(string='Type', selection=[('nepremicnina','Nepremičnina'), 
                                                          ('lokacija','Lokacija'),
                                                          ('namen', 'Namen')
                                                          ('ponudba','Ponudba'), 
                                                          ('stranka', 'Stranka'), 
                                                          ('lastnosti','Osebnostne lastnosti')])
    color = fields.Integer(string='Color Index')
     


"""
Zakaj se ni oddala
opis nepremičnine
leto izgradnje
leto adaptacije
kaj je bilo obnovljeno
streha vrsta kritine
streha leto obnove/kritja
fasada/izolacija
leto obnove fasade
okna tip
leto obnove/inštalacije oken
materiali
stroški vzdrževanja
stroški rezervega sklada
upravnik
energetska izkaznica
energijski razred
Vrsta ogrevanja:
plinovod
toplovod
toplotna črpalka
biomasa
Dodatki:
balkon velikost
atrij
klet
dvigalo
ogrevanje
višina stroškov
lega
sanitarije
dnevne sobe
spalnice
bazen
kamin
vrt
razgled
penthouse
hišni ljubljenčki
shramba
klet
opremljeno
dostop za invalide
pogled na
primerno za študente
Parkiranje
garaža
parkino mesto
parkirna hiša
klima
alarm
varovan objekt
video nadzor
domofon
360 view ID
infrastruktura 
vrtec
osnovna šola
fakultete
pošta 
trgovina
banka
avtocesta
avtobus
vlak
igrišče
park
zdravstveni dom
Komunikacijski priključki
telefon
kabel
optika
internet
Lastništvo
lastništvo pridobljeno na podlagi:
Dne:
Plombe:
Hipoteke:
solastnina
prepoved odtujitve/obremenitve
predkupna pravica
parcelne številke:
omejitev po ZKZ
Predkupne pravice:
potrdilo o namenski rabi/lokacijska info
predkupna pravica občine oz drugega upra Vičenca
ARSO soglasje
Varstvo naravne ali kulturne dediščine
Mestni priključek
GURS vrednost
Seznam opreme, ki je vključena v ceno
kuhinja
dnevna soba
spalnica
otroška soba
hodnik
kopalnica
"""
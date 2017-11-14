# coding=UTF8
import pytest

from hybra import core

import datetime

class TestUM:

    def setup(self):
        self.data = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.listdata = list( self.data )

    def test_get_everything(self):

        assert len( self.listdata ) == 276

    def test_texts(self):

        text1 = 'Facebook patoaa valeuutisten tulvaa algoritmin muutoksella' + ' ' + 'Facebook patoaa valeuutisten tulvaa algoritmin muutoksella' + ' ' + """Yhtiön mukaan muutos vaikuttaa hyvin pieneen mutta äänekkääseen käyttäjäryhmään. Facebook aikoo vähentää uutissyötteissä näkyviä valeuutisia muuttamalla syötettä ohjaavaa algoritmia. Yhtiön mukaan muutos vaikuttaa niin sanottujen klikki-otsikkojuttujen, sensaatiohakuisten verkkosivujen ja valeuutisten näkyvyyteen. Muutos vaikuttaa vain linkkeihin. Kuvien ja muiden julkaisujen näkyvyyteen algoritmin muutos ei vaikuta. Facebook on tutkinut käyttäjiä, jotka julkaisevat esimerkiksi valeuutisia. Tutkimustensa perusteella Facebook arvioi, että muutos vaikuttaa hyvin pieneen joukkoon palvelun käyttäjiä, eli noin prosenttiyksikön kymmenykseen yli 50 julkaisua päivässä tekevistä käyttäjistä. Algoritmin muutos on vahva työkalu. Facebookilla on noin kaksi miljardia käyttäjää, ja yhtiön algoritmi määrittää, mitkä ystävien, mainostajien tai muiden lähteiden viestit näkyvät käyttäjien uutissyötteessä ja missä järjestyksessä. Sosiaalisen median jättiläinen on viime aikoina herännyt toimiin kitkeäkseen valeuutisia palvelustaan. Facebook sai uutta pontta Yhdysvaltojen presidentinvaalikampanjan aikana, kun palvelun avulla välitettiin suuri määrä sepitteellisiä uutisia. Tämän vuoden aikana myös EU-maat ovat koventaneet äänenpainoaan ja vaatineet Facebookilta rivakampia toimia esimerkiksi valeuutisten ja netin vihapuheen siistimiseksi."""

        ## TODO: fix unicode management in hybra core as whole and then check this
        ##assert self.listdata[0]['text_content'] == text1

    def test_dates(self):

        dates = [
            datetime.datetime(2017, 6, 30, 23, 13, 53),
            datetime.datetime(2017, 6, 30, 21, 17, 20),
        ]

        for i, j in enumerate( dates ):
            assert self.listdata[i]['timestamp'] == j

    def test_links(self):

	links = [ [], [u'http://www.longwarjournal.org/archives/2017/06/qassem-soleimani-spotted-near-the-syrian-border-with-iraqi-militias.php', u'https://www.theatlantic.com/magazine/archive/2016/04/the-obama-doctrine/471525/', u'http://abcnews.go.com/International/us-troops-syria-heres-theyre/story?id=46020582', u'https://yle.fi/uutiset/3-9650625'] ]

        for i, j in enumerate( links ):
            assert self.listdata[i]['links'] == j

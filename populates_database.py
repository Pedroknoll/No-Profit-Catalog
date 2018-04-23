#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pedro H Knoll
Udacity FullStack NanoDegree
Data population script
    - ver: 0.1  04/2018
"""

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from database_setup import (Base, Category, Organization, DATABASE)

engine = create_engine(URL(**DATABASE))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create some test Category objects
cat1 = Category(name="educação")
session.add(cat1)
session.commit()

cat2 = Category(name="saúde")
session.add(cat2)
session.commit()

cat3 = Category(name="meio ambiente")
session.add(cat3)
session.commit()

cat4 = Category(name="crianças e jovens")
session.add(cat4)
session.commit()

cat5 = Category(name="moradia")
session.add(cat5)
session.commit()

cat6 = Category(name="capacitação profissional e renda")
session.add(cat6)
session.commit()

cat7 = Category(name="proteção animal")
session.add(cat7)
session.commit()

cat8 = Category(name="combate a pobreza")
session.add(cat8)
session.commit()

cat8 = Category(name="idosos")
session.add(cat8)
session.commit()

cat9 = Category(name="cultura, esporte e lazer")
session.add(cat9)
session.commit()

# Add some items to Categories
organization1 = Organization(name="Associação Brazil Foundation",
             description=("""Mobilizar recursos para ideias e ações que
                            transformam o Brasil. Trabalhamos com líderes
                            e organizações sociais e uma rede global de
                            apoiadores para promover igualdade, justiça social
                            e oportunidade para todos os brasileiros"""),
             site="www.brazilfoundation.org",
             category_id=cat5.id)
session.add(organization1)
session.commit()

organization2 = Organization(name="ChildFund Brasil",
             description=("""Apoiar crianças em situação de privação,
                            exclusão e vulnerabilidade; mobilizar pessoas
                            e instituições para a valorização, proteção e
                            promoção dos direitos infantis e juvenis;
                            enriquecer a vida dos apoiadores por meio
                            da defesa a nossa causa"""),
             site="www.childfundbrasil.org.br",
             category_id=cat4.id)
session.add(organization2)
session.commit()

organization3 = Organization(name="Fundação Estudar",
             description=("""Criar oportunidades para gente boa sonhar grande
                            e transformar o Brasil"""),
             site="www.estudar.org.br",
             category_id=cat1.id)
session.add(organization3)
session.commit()

organization4 = Organization(name="Instituto do Câncer Infantil",
             description=("""Salvar vidas, assegurando a saúde da criança e
                            adolescente com câncer, por meio de parcerias,
                            assistência, capacitação, pesquisa e mobilização
                            social, visando à melhoria da qualidade de vida
                            e dignidade aos pacientes e seus familiares"""),
             site="www.ici-rs.org.br",
             category_id=cat2.id)
session.add(organization4)
session.commit()

organization5 = Organization(name="Instituto Socioambiental",
             description=("""Construir soluções sustentáveis que garantam
                            os direitos coletivos e difusos e valorizem
                            a diversidade socioambiental"""),
             site="www.socioambiental.org",
             category_id=cat3.id)
session.add(organization5)
session.commit()

organization6 = Organization(name="S.O.S Mata Atlântica",
             description=("Inspirar a sociedade na defesa da Mata Atlântica"),
             site="www.sosma.org.br",
             category_id=cat3.id)
session.add(organization6)
session.commit()

organization7 = Organization(name="Um Teto para o Meu País",
             description=("""Trabalhar com determinação nas comunidades
                            precárias para superar a pobreza por meio da
                            formação e ação conjunta dos moradores e
                            moradoras, jovens voluntários e voluntárias
                            e outros atores"""),
             site="www.teto.org.br",
             category_id=cat5.id)
session.add(organization7)
session.commit()

organization8 = Organization(name=("""Associação Brasileira de Linfoma
                                    e Leucemia"""),
             description=("""Oferecer ajuda e mobilizar parceiros para que
                            todas as pessoas com câncer do sangue no Brasil
                            tenham acesso ao melhor tratamento"""),
             site="www.abrale.org.br",
             category_id=cat2.id)
session.add(organization8)
session.commit()

organization9 = Organization(name="Amigos do Bem",
             description=("""Promover desenvolvimento local e inclusão
                            social capazes de combater a fome e a miséria
                            por meio de ações educacionais e projetos
                            autossustentáveis"""),
             site="www.amigosdobem.org",
             category_id=cat1.id)
session.add(organization9)
session.commit()

organization10 = Organization(name="Asssociação Santo Agostinho",
             description=("""Transformar ao educar e cuidar de crianças e
                            adolescentes, acolher e promover o bem-estar
                            oferecendo oportunidade de desenvolvimento
                            pessoal com respeito e dignidade"""),
             site="www.asa-santoagostinho.org.br",
             category_id=cat1.id)
session.add(organization10)
session.commit()

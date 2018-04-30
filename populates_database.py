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

from models import (Base, User, Category, Organization, DATABASE)

engine = create_engine(URL(**DATABASE))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a user
User1 = User(name="Robot Machine", email="robot.machine@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

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

cat9 = Category(name="idosos")
session.add(cat9)
session.commit()

cat10 = Category(name="cultura, esporte e lazer")
session.add(cat10)
session.commit()

# Add some items to Categories
organization1 = Organization(name="Fundação Lemann",
             description=("Trabalhamos por uma educação pública de qualidade"
                        " para todos e apoiamos pessoas e organizações que"
                        " dedicam suas vidas a solucionar os principais"
                        " desafios sociais do Brasil. Somos uma organização"
                        " familiar, sem fins lucrativos, e atuamos sempre em"
                        " parceria com Governos e outras entidades da"
                        " sociedade civil, de maneira plural, inclusiva e"
                        " buscando caminhos que funcionam na escala dos"
                        " desafios do Brasil."),
             site="www.fundacaolemann.org.br",
             category_id=cat1.id,
             user_id=1)
session.add(organization1)
session.commit()

organization2 = Organization(name="Fundação Estudar",
             description=("A Fundação Estudar é uma organização sem fins"
                        " lucrativos que acredita que o Brasil será um país"
                        " melhor se tivermos mais jovens determinados a seguir"
                        " uma trajetória de impacto."),
             site="www.estudar.org.br",
             category_id=cat1.id,
             user_id=1)
session.add(organization2)
session.commit()

organization3 = Organization(name="Hospital São Francisco de Assis",
             description=("Promover, resgatar, restaurar e defender a"
                        " dignidade da pessoa humana por meio de um"
                        " serviço de saúde"),
             site="www.hospitalsaofrancisco.org.br",
             category_id=cat2.id,
             user_id=1)
session.add(organization3)
session.commit()

organization4 = Organization(name="ABRACE",
             description=("Prestar assistência social a crianças e adolescentes"
                        " com câncer e hemopatias, e suas famílias, visando à"
                        " qualidade de vida e garantir o acesso a melhores"
                        " condições de tratamento"),
             site="www.abrace.com.br",
             category_id=cat2.id,
             user_id=1)
session.add(organization4)
session.commit()

organization5 = Organization(name="Doutores da Alegria",
             description=("Intervir na sociedade propondo a arte como mínimo"
                        " social para crianças, adolescentes e outros públicos"
                        " em situação de vulnerabilidade e risco social"
                        " privilegiando hospitais públicos e ambientes"
                        " adversos, tendo a linguagem do palhaço como"
                        " referência"),
             site="www.doutoresdaalegria.org.br",
             category_id=cat2.id,
             user_id=1)
session.add(organization5)
session.commit()

organization6 = Organization(name="S.O.S Mata Atlântica",
             description=("A Fundação SOS Mata Atlântica é uma organização"
                        " não-governamental criada em 1986. Trata-se de uma"
                        " entidade privada sem fins lucrativos, que tem como"
                        " missão promover a conservação da diversidade"
                        " biológica e cultural do Bioma Mata Atlântica e"
                        " ecossistemas sob sua influência, estimulando ações"
                        " para o desenvolvimento sustentável."),
             site="www.sosma.org.br",
             category_id=cat3.id,
             user_id=1)
session.add(organization6)
session.commit()

organization7 = Organization(name="ChildFund Brasil",
             description=("Apoiar crianças em situação de privação, exclusão"
                        " e vulnerabilidade; mobilizar pessoas e instituições"
                        " para a valorização, proteção e promoção dos direitos"
                        " infantis e juvenis; enriquecer a vida dos apoiadores"
                        " por meio da defesa a nossa causa"),
             site="www.childfundbrasil.org.br",
             category_id=cat4.id,
             user_id=1)
session.add(organization7)
session.commit()

organization8 = Organization(name="Associação Santo Agostinho",
             description=("Transformar ao educar e cuidar de crianças e"
                        " adolescentes, acolher e promover o bem-estar"
                        " oferecendo oportunidade de desenvolvimento pessoal"
                        " com respeito e dignidade"),
             site="www.asa-santoagostinho.org.br",
             category_id=cat4.id,
             user_id=1)
session.add(organization8)
session.commit()

organization9 = Organization(name="Fundação Abrinq",
             description=("Promover a defesa dos direitos e o exercício da"
                        " cidadania de crianças e adolescentes e para isso,"
                        " funcionamos como uma ponte entre quem quer ajudar"
                        " e quem precisa de ajuda. Doadores, voluntários,"
                        " organizações, empresas e municípios são nossos"
                        " grandes parceiros nesta missão."),
             site="www.fadc.org.br",
             category_id=cat4.id,
             user_id=1)
session.add(organization9)
session.commit()

organization10 = Organization(name="Um Teto para o meu país",
             description=("Trabalhar com determinação nas comunidades precárias"
                        " para superar a pobreza por meio da formação e ação"
                        " conjunta dos moradores e moradoras, jovens voluntários"
                        " e voluntárias e outros atores"),
             site="www.teto.org.br",
             category_id=cat5.id,
             user_id=1)
session.add(organization10)
session.commit()

organization11 = Organization(name="Sitawi - finanças do bem",
             description=("A SITAWI Finanças do Bem é uma organização social"
                        " de interesse público (OSCIP*) pioneira no"
                        " desenvolvimento de soluções financeiras para"
                        " impacto social e na análise da performance"
                        " socioambiental de empresas e instituições"
                        " financeiras."),
             site="www.sitawi.net",
             category_id=cat6.id,
             user_id=1)
session.add(organization11)
session.commit()

organization12 = Organization(name="Associação Aliança Empreendedora",
             description=("Unir forças e viabilizar acessos para que pessoas"
                        " e comunidades de baixa renda possam ser"
                        " empreendedoras, promovendo a inclusão e o"
                        " desenvolvimento econômico e social"),
             site="www.aliancaempreendedora.org.br",
             category_id=cat6.id,
             user_id=1)
session.add(organization12)
session.commit()

organization13 = Organization(name="Banco da Providência",
             description=("Contribuir coletivamente para a redução da"
                        " desigualdade social e promover o desenvolvimento"
                        " humano de famílias residentes nas comunidades"
                        " empobrecidas do Rio de Janeiro por meio do"
                        " acolhimento, da capacitação para o trabalho,"
                        " da geração de renda"),
             site="www.bancodaprovidencia.org.br",
             category_id=cat6.id,
             user_id=1)
session.add(organization13)
session.commit()

organization14 = Organization(name="Insituto Luisa Mell",
             description=("O Instituto Luisa Mell atua principalmente no"
                        " resgate de animais feridos ou em situação de risco,"
                        " recuperação e adoção. Mantemos um abrigo com cerca"
                        " de 300 animais, entre cães e gatos, todos resgatados"
                        " das ruas, onde eles são protegidos, alimentados e"
                        " aguardam pela chance de serem adotados"),
             site="www.ilm.org.br",
             category_id=cat7.id,
             user_id=1)
session.add(organization14)
session.commit()

organization15 = Organization(name="Litro de Luz",
             description=("Levamos luz até comunidades locais que, seja por"
                        " não terem acesso ou por não terem condições de"
                        " pagar, vivem sem luz em suas casas. Para fazer"
                        " isso, utilizamos uma tecnologia simples, econômica"
                        " e ecologicamente sustentável, composta por garrafas"
                        " plásticas, painéis solares e lâmpadas de LED."),
             site="www.litrodeluz.com",
             category_id=cat5.id,
             user_id=1)
session.add(organization15)
session.commit()

organization16 = Organization(name="Action Aid Brasil",
             description=("Somos uma organização internacional que trabalha"
                        " por justiça social, igualdade de gênero e pelo fim"
                        " da pobreza. Fomos fundados em 1972 e estamos"
                        " presentes em 45 países, alcançando mais de 15"
                        " milhões de pessoas no mundo. No Brasil desde 1999,"
                        " atuamos em mais de 2.4 mil comunidades e"
                        " beneficiamos mais de 300 mil pessoas. "),
             site="www.actionaid.org.br",
             category_id=cat8.id,
             user_id=1)
session.add(organization16)
session.commit()

organization17 = Organization(name="",
             description=("Acreditamos que toda pessoa, independente da idade,"
                        " tem o direito de sonhar. Temos como objetivo,"
                        " promover por meio de assistência e do desenvolvimento"
                        " social, da educação, do esporte, da cultura e do lazer,"
                        " a melhoria da qualidade de vida dos idosos, como"
                        " forma de resgatar a sua dignidade e auto-estima."),
             site="www.velhoamigo.org.br",
             category_id=cat9.id,
             user_id=1)
session.add(organization17)
session.commit()

organization18 = Organization(name="Instituto Reação",
             description=("Promover o desenvolvimento humano e a inclusão"
                        " social por meio do esporte e da educação, fomentando"
                        " o judô desde a iniciação esportiva, formando faixas"
                        " pretas dentro e fora do tatame"),
             site="www.institutoreacao.org.br",
             category_id=cat10.id,
             user_id=1)
session.add(organization18)
session.commit()

organization19 = Organization(name="Associação Luta pela Paz",
             description=("Utilizar boxe e artes marciais e desenvolvimento"
                        " pessoal combinados com educação, suporte social,"
                        " empregabilidade e liderança juvenil, para desenvolver"
                        " o potencial dos jovens em comunidades que sofrem com"
                        " crime e violência"),
             site="www.lutapelapaz.org",
             category_id=cat10.id,
             user_id=1)
session.add(organization19)
session.commit()

organization20 = Organization(name="Instituto Olg Kos Inclusão Cultural",
             description=("O Instituto Olga Kos de Inclusão Cultural (IOK)"
                        " é uma associação sem fins econômicos, que desenvolve"
                        " projetos artísticos e esportivos, aprovados em leis"
                        " de incentivo fiscal, para atender, prioritariamente,"
                        " crianças, jovens e adultos com deficiência"
                        " intelectual. "),
             site="www.institutoolgakos.org.br",
             category_id=cat10.id,
             user_id=1)
session.add(organization20)
session.commit()

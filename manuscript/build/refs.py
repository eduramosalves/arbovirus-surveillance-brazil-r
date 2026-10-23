"""Reference list: ASM-style entries of the draft -> NLM/AMA-style entries (numbered by first citation at build time).

REF_KEY_ORDER gives every reference a key: r1..r62 (original numbering) plus new keys.
MAX_AUTHORS: with more than 6 authors, list the first 3 and add 'et al' (AMA 11th ed.). UNVERIFIED for JMV.
"""
import re
from msbase import ORIG

MAX_AUTHORS = 6
SHOW_AUTHORS = 3

# Entries that are not 'Authors. Year. Title. *Journal* vol:pages.' (written by hand, same facts as the draft)
MANUAL = {
    9: "Schuler-Faccini L, Ribeiro EM, Feitosa IM, et al; Brazilian Medical Genetics Society–Zika Embryopathy Task Force. "
       "Possible association between Zika virus infection and microcephaly — Brazil, 2015. *MMWR Morb Mortal Wkly Rep*. 2016;65(3):59–62.",
    11: "Brasil. Ministério da Saúde, Secretaria de Vigilância em Saúde e Ambiente. Monitoramento das arboviroses urbanas: "
        "dengue, chikungunya e Zika — 2024. *Bol Epidemiol*. 2024;55(11):1–28.",
    23: "de Abreu RC, Fernandez IP, Mishra S, et al. The role of climate change in the expansion of dengue. *medRxiv*. Preprint. 2025. "
        "doi:10.1101/2025.10.06.25337235",
    51: "Pan American Health Organization. *Integrated Management Strategy for Arboviral Disease Prevention and Control in the Americas*. "
        "PAHO; 2019. https://iris.paho.org/handle/10665.2/52492",
    52: "Brasil. Ministério da Saúde, Secretaria de Vigilância em Saúde e Ambiente. *Guia de Vigilância em Saúde*. 6th ed, rev. "
        "Ministério da Saúde; 2024.",
    53: "Pan American Health Organization. *Guidelines for the Clinical Diagnosis and Treatment of Dengue, Chikungunya, and Zika*. "
        "PAHO; 2022. doi:10.37774/9789275124871",
    54: "Brasil. Ministério da Saúde. Portaria nº 204, de 17 de fevereiro de 2016. Define a Lista Nacional de Notificação "
        "Compulsória de doenças, agravos e eventos de saúde pública nos serviços de saúde públicos e privados em todo o "
        "território nacional. *Diário Oficial da União*. 2016.",
    58: "Kendall MG. *Rank Correlation Methods*. 4th ed. Charles Griffin; 1975.",
    62: "Hilbe JM. *Negative Binomial Regression*. 2nd ed. Cambridge University Press; 2011.",
}

NEW = {
    "liu2023": "Liu Z, Zhang Q, Li L, et al. The effect of temperature on dengue virus transmission by *Aedes* mosquitoes. "
               "*Front Cell Infect Microbiol*. 2023;13:1242173. doi:10.3389/fcimb.2023.1242173",
    "moura2020": "Moura MCBM, de Oliveira JV, Pedreira RM, et al. Spatio-temporal dynamics of *Aedes aegypti* and *Aedes albopictus* "
                 "oviposition in an urban area of northeastern Brazil. *Trop Med Int Health*. 2020;25(12):1510–1521. "
                 "doi:10.1111/tmi.13491",
    "lim2025": "Lim A, Shearer FM, Sewalk K, et al. The overlapping global distribution of dengue, chikungunya, Zika and yellow fever. "
               "*Nat Commun*. 2025;16(1):3418. doi:10.1038/s41467-025-58609-5",
    "delima2026": "de Lima STS, Claro IM, Hua X, et al. Transmission dynamics of dengue virus, Ceará State, Brazil, 2010–2025. "
                  "*Emerg Infect Dis*. 2026;32(11). Early release October 15, 2026. doi:10.3201/eid3211.260609",
    "ibge2024": "Instituto Brasileiro de Geografia e Estatística (IBGE). *Projeções da População, Revisão 2024*. IBGE; 2024. "
                "https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/",
    "ibgedou": "Instituto Brasileiro de Geografia e Estatística (IBGE). *Estimativas da População* (1 July, 2024–2026; published in the "
               "Diário Oficial da União). IBGE. https://ftp.ibge.gov.br/Estimativas_de_Populacao/",
    "inmet": "Instituto Nacional de Meteorologia (INMET). *Banco de Dados Históricos: dados horários das estações automáticas, "
             "2016–2026*. INMET. https://portal.inmet.gov.br/uploads/dadoshistoricos/",
    "esgov2021": "Governo do Espírito Santo. Espírito Santo registra mais de 2 mil casos de chikungunya em 2021. 2021. "
                 "https://www.es.gov.br/Noticia/espirito-santo-registra-mais-de-2-mil-casos-de-chikungunya-em-2021",
}

_PAGES = re.compile(r"^([A-Za-z]?)(\d+)–([A-Za-z]?)(\d+)$")


def _expand_pages(p):
    m = _PAGES.match(p)
    if not m:
        return p
    pa, a, pb, b = m.groups()
    if len(b) < len(a) and not pb:
        b = a[:len(a) - len(b)] + b
        pb = pa
    return "%s%s–%s%s" % (pa, a, pb or "", b)


def _fmt_authors(auth):
    names = [x.strip() for x in auth.split(",") if x.strip()]
    if len(names) > MAX_AUTHORS:
        names = names[:SHOW_AUTHORS] + ["et al"]
    return ", ".join(names)


def convert(i):
    """Original reference number i (1..62) -> NLM-style markup."""
    if i in MANUAL:
        return MANUAL[i]
    t = ORIG[95 + i]
    m = re.match(r"^%d\. (.+?)\. ((?:19|20)\d\d)\. (.+?)\. \*([^*]+)\*\s*(.*?)\.?$" % i, t)
    if not m:
        raise ValueError("cannot parse reference %d: %r" % (i, t[:100]))
    auth, year, title, journal, tail = m.groups()
    vol, _, pages = tail.partition(":")
    pages = _expand_pages(pages.strip().rstrip("."))
    return "%s. %s. *%s*. %s;%s:%s." % (_fmt_authors(auth), title, journal.strip(), year, vol.strip(), pages)


def all_entries():
    out = {"r%d" % i: convert(i) for i in range(1, 63)}
    out.update(NEW)
    return out


if __name__ == "__main__":
    for k, v in all_entries().items():
        print(k, "|", v)

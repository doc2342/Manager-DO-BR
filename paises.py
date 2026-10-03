# -*- coding: utf-8 -*-
"""Nacionalidades do Dugout: nome em inglês (páginas de elenco) e código (dataset do Fenômeno) -> nome em português + bandeira."""

PAISES = {  # inglês -> (português, bandeira)
    "Albania": ("Albânia", "🇦🇱"), "Algeria": ("Argélia", "🇩🇿"), "Argentina": ("Argentina", "🇦🇷"),
    "Australia": ("Austrália", "🇦🇺"), "Austria": ("Áustria", "🇦🇹"), "Bangladesh": ("Bangladesh", "🇧🇩"),
    "Belgium": ("Bélgica", "🇧🇪"), "Bolivia": ("Bolívia", "🇧🇴"), "Bosnia and Herzegovina": ("Bósnia", "🇧🇦"),
    "Brazil": ("Brasil", "🇧🇷"), "Bulgaria": ("Bulgária", "🇧🇬"), "Canada": ("Canadá", "🇨🇦"),
    "Chile": ("Chile", "🇨🇱"), "China": ("China", "🇨🇳"), "Colombia": ("Colômbia", "🇨🇴"),
    "Croatia": ("Croácia", "🇭🇷"), "Czech republic": ("Tchéquia", "🇨🇿"), "Denmark": ("Dinamarca", "🇩🇰"),
    "England": ("Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿"), "Estonia": ("Estônia", "🇪🇪"), "Finland": ("Finlândia", "🇫🇮"),
    "France": ("França", "🇫🇷"), "Germany": ("Alemanha", "🇩🇪"), "Greece": ("Grécia", "🇬🇷"),
    "Hungary": ("Hungria", "🇭🇺"), "Iceland": ("Islândia", "🇮🇸"), "India": ("Índia", "🇮🇳"),
    "Ireland": ("Irlanda", "🇮🇪"), "Israel": ("Israel", "🇮🇱"), "Italy": ("Itália", "🇮🇹"),
    "Japan": ("Japão", "🇯🇵"), "Latvia": ("Letônia", "🇱🇻"), "Lithuania": ("Lituânia", "🇱🇹"),
    "Malta": ("Malta", "🇲🇹"), "Mexico": ("México", "🇲🇽"), "Moldova": ("Moldávia", "🇲🇩"),
    "Netherlands": ("Holanda", "🇳🇱"), "New Zealand": ("Nova Zelândia", "🇳🇿"), "Norway": ("Noruega", "🇳🇴"),
    "Peru": ("Peru", "🇵🇪"), "Poland": ("Polônia", "🇵🇱"), "Portugal": ("Portugal", "🇵🇹"),
    "Rep. of Montenegro": ("Montenegro", "🇲🇪"), "Romania": ("Romênia", "🇷🇴"), "Russia": ("Rússia", "🇷🇺"),
    "Scotland": ("Escócia", "🏴󠁧󠁢󠁳󠁣󠁴󠁿"), "Serbia": ("Sérvia", "🇷🇸"), "Slovakia": ("Eslováquia", "🇸🇰"),
    "Slovenia": ("Eslovênia", "🇸🇮"), "South Africa": ("África do Sul", "🇿🇦"), "South Korea": ("Coreia do Sul", "🇰🇷"),
    "Spain": ("Espanha", "🇪🇸"), "Sweden": ("Suécia", "🇸🇪"), "Switzerland": ("Suíça", "🇨🇭"),
    "Thailand": ("Tailândia", "🇹🇭"), "Turkey": ("Turquia", "🇹🇷"), "United States of America": ("Estados Unidos", "🇺🇸"),
    "Uruguay": ("Uruguai", "🇺🇾"), "Venezuela": ("Venezuela", "🇻🇪"),
}

CODIGOS = {  # código do dataset do Fenômeno -> inglês
    "BRA": "Brazil", "ESL": "Slovenia", "ROM": "Romania", "TUR": "Turkey", "SER": "Serbia", "POL": "Poland",
    "HOL": "Netherlands", "POR": "Portugal", "FRA": "France", "EUA": "United States of America", "NOR": "Norway",
    "BOS": "Bosnia and Herzegovina", "ALG": "Algeria", "ITA": "Italy", "BOL": "Bolivia", "CRO": "Croatia",
    "SUI": "Switzerland", "ING": "England", "MNE": "Rep. of Montenegro", "DIN": "Denmark", "MOL": "Moldova",
    "TAI": "Thailand", "ARG": "Argentina", "ALE": "Germany", "BEL": "Belgium", "CHI": "Chile", "COL": "Colombia",
    "LET": "Latvia", "URU": "Uruguay", "PER": "Peru", "LIT": "Lithuania", "VEN": "Venezuela", "RUS": "Russia",
    "SUE": "Sweden", "COR": "South Korea", "FIN": "Finland", "IRL": "Ireland", "NZE": "New Zealand",
    "BUL": "Bulgaria", "AUT": "Austria", "HUN": "Hungary", "ISR": "Israel", "MEX": "Mexico", "AUS": "Australia",
    "JAP": "Japan", "BAN": "Bangladesh", "ESC": "Scotland", "TCH": "Czech republic", "ESP": "Spain", "MAL": "Malta",
    "AFS": "South Africa", "ALB": "Albania", "ISL": "Iceland", "CAN": "Canada", "IND": "India", "EST": "Estonia",
    "ESK": "Slovakia", "CHN": "China", "GRE": "Greece",
}


def pais_pt(valor):
    """Aceita código ('SER') ou nome em inglês ('Serbia'); devolve o nome em português (ou o próprio valor)."""
    ingles = CODIGOS.get(valor, valor)
    return PAISES.get(ingles, (valor, ""))[0]

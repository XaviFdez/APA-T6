"""
Xavi Fernandez Rodriguez

Normalización de expresiones horarias mediante expresiones regulares.
"""

import re


def normalizaHoras(ficText, ficNorm):
    """
    Lee un fichero de texto y escribe otro fichero con las expresiones
    horarias normalizadas al formato HH:MM.
    """

    with open(ficText, encoding='utf-8') as entrada:
        texto = entrada.read()

    # HH:MM válidas
    def formato_hhmm(match):
        h = int(match.group(1))
        m = int(match.group(2))

        if 0 <= h <= 23 and 0 <= m <= 59:
            return f'{h:02d}:{m:02d}'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2}):(\d{2})\b',
        formato_hhmm,
        texto
    )

    # HhMm
    def formato_hm(match):
        h = int(match.group(1))
        m = match.group(2)

        if m is None:
            m = 0
        else:
            m = int(m)

        if 0 <= h <= 23 and 0 <= m <= 59:
            return f'{h:02d}:{m:02d}'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})h(?:\s*(\d{1,2})m)?\b',
        formato_hm,
        texto
    )

    # H en punto
    def en_punto(match):
        h = int(match.group(1))

        if 1 <= h <= 12:
            h %= 12
            return f'{h:02d}:00'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+en\s+punto\b',
        en_punto,
        texto,
        flags=re.IGNORECASE
    )

    # y cuarto
    def y_cuarto(match):
        h = int(match.group(1))

        if 1 <= h <= 12:
            h %= 12
            return f'{h:02d}:15'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+y\s+cuarto\b',
        y_cuarto,
        texto,
        flags=re.IGNORECASE
    )

    # y media
    def y_media(match):
        h = int(match.group(1))

        if 1 <= h <= 12:
            h %= 12
            return f'{h:02d}:30'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+y\s+media\b',
        y_media,
        texto,
        flags=re.IGNORECASE
    )

    # menos cuarto
    def menos_cuarto(match):
        h = int(match.group(1))

        if 1 <= h <= 12:
            h = (h - 1) % 12
            return f'{h:02d}:45'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+menos\s+cuarto\b',
        menos_cuarto,
        texto,
        flags=re.IGNORECASE
    )

    # de la mañana
    def manana(match):
        h = int(match.group(1))

        if 4 <= h <= 12:
            if h == 12:
                h = 0

            return f'{h:02d}:00'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+de\s+la\s+mañana\b',
        manana,
        texto,
        flags=re.IGNORECASE
    )

    # del mediodía
    def mediodia(match):
        h = int(match.group(1))

        if h == 12:
            return '12:00'

        if 1 <= h <= 3:
            return f'{h + 12:02d}:00'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+del\s+mediod[ií]a\b',
        mediodia,
        texto,
        flags=re.IGNORECASE
    )

    # de la tarde
    def tarde(match):
        h = int(match.group(1))

        if 3 <= h <= 8:
            return f'{h + 12:02d}:00'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+de\s+la\s+tarde\b',
        tarde,
        texto,
        flags=re.IGNORECASE
    )

    # de la noche
    def noche(match):
        h = int(match.group(1))

        if h == 12:
            return '00:00'

        if 1 <= h <= 4:
            return f'{h:02d}:00'

        if 8 <= h <= 11:
            return f'{h + 12:02d}:00'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+de\s+la\s+noche\b',
        noche,
        texto,
        flags=re.IGNORECASE
    )

    # de la madrugada
    def madrugada(match):
        h = int(match.group(1))

        if 1 <= h <= 6:
            return f'{h:02d}:00'

        return match.group(0)

    texto = re.sub(
        r'\b(\d{1,2})\s+de\s+la\s+madrugada\b',
        madrugada,
        texto,
        flags=re.IGNORECASE
    )

    with open(ficNorm, 'w', encoding='utf-8') as salida:
        salida.write(texto)

"""
Xavi Fernandez Rodriguez
 
Normalización de expresiones horarias en texto mediante expresiones regulares.
Detecta múltiples formatos horarios en castellano y los convierte al formato
estándar HH:MM (24 horas, dos dígitos para hora y minuto).
"""
 
import re
 
 
def _hora_con_periodo(h, m, periodo):
    """
    Aplica el período del día a una hora en reloj de 12h (1-12).
    Devuelve (hora24, minuto) o None si la combinación es inválida.
    """
    if periodo == 'mañana':
        if 4 <= h <= 12:
            return (0 if h == 12 else h), m
    elif periodo == 'mediodía':
        if h == 12:
            return 12, m
        if 1 <= h <= 3:
            return h + 12, m
    elif periodo == 'tarde':
        if 3 <= h <= 8:
            return h + 12, m
    elif periodo == 'noche':
        if h == 12:
            return 0, m
        if 8 <= h <= 11:
            return h + 12, m
    elif periodo == 'madrugada':
        if 1 <= h <= 6:
            return h, m
    return None
 
 
def _aplicar_modificador(h, modificador):
    """
    Aplica 'en punto', 'y cuarto', 'y media' o 'menos cuarto' a una hora
    de reloj de 12h (1-12). Devuelve (hora, minuto) en reloj 12h o None si
    la hora está fuera del rango válido.
    """
    if not (1 <= h <= 12):
        return None
    mod = re.sub(r'\s+', ' ', modificador.strip().lower())
    if mod == 'en punto':
        return h, 0
    if mod == 'y cuarto':
        return h, 15
    if mod == 'y media':
        return h, 30
    if mod == 'menos cuarto':
        return (h - 1) if h > 1 else 12, 45
    return None
 
 
# ---------------------------------------------------------------------------
# Regex principal — la variante HH:MM va PRIMERO para evitar que el motor
# consuma el dígito de la hora antes de ver el ':'.
#
# Grupos variante B (HH:MM):  (1) hora  (2) minutos
# Grupos variante A (resto):  (3) hora  (4) 'h'  (5) minutos tras h
#                             (6) modificador  (7) período del día
# ---------------------------------------------------------------------------
_PATRON = re.compile(
    r'\b'
    r'(?:'
        # Variante B: HH:MM estándar — va primero
        r'(\d{1,2}):(\d{2})'
        r'|'
        # Variante A: Hh, HhMMm, H modificador, H período, combinaciones
        r'(\d{1,2})'
        r'(h)?'
        r'(?:\s*(\d{1,2})m)?'
        r'(?:\s+(en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto))?'
        r'(?:\s+(?:de\s+la\s+(mañana|tarde|noche|madrugada)|del\s+mediod[ií]a))?'
        r'(?=\b|$)'
    r')',
    re.IGNORECASE,
)
 
 
def _detectar_periodo(texto):
    """Normaliza el texto capturado del período a una clave interna."""
    t = texto.lower()
    if 'madrugada' in t:
        return 'madrugada'
    if 'tarde' in t:
        return 'tarde'
    if 'noche' in t:
        return 'noche'
    if 'mañana' in t:
        return 'mañana'
    if 'mediod' in t:
        return 'mediodía'
    return None
 
 
def _reemplazar(match):
    """Función de sustitución para cada match del patrón."""
 
    # --- Variante B: HH:MM ---
    if match.group(1) is not None:
        h = int(match.group(1))
        m = int(match.group(2))
        if 0 <= h <= 23 and 0 <= m <= 59:
            return f'{h:02d}:{m:02d}'
        return match.group(0)
 
    # --- Variante A ---
    h       = int(match.group(3))
    tiene_h = match.group(4) is not None
    m_str   = match.group(5)
    mod     = match.group(6)
    per_txt = match.group(7)
 
    m = int(m_str) if m_str is not None else None
    periodo = _detectar_periodo(per_txt) if per_txt else None
 
    # ----------------------------------------------------------------
    # Caso 1: formato con letra 'h' (8h, 10h30m, 17h5m…)
    # ----------------------------------------------------------------
    if tiene_h:
        minutos = m if m is not None else 0
        if not (0 <= h <= 23 and 0 <= minutos <= 59):
            return match.group(0)
        if periodo:
            resultado = _hora_con_periodo(h, minutos, periodo)
            if resultado is None:
                return match.group(0)
            h24, m24 = resultado
            return f'{h24:02d}:{m24:02d}'
        return f'{h:02d}:{minutos:02d}'
 
    # ----------------------------------------------------------------
    # Caso 2: número sin 'h' — solo válido con modificador o período
    # ----------------------------------------------------------------
    if mod is None and periodo is None:
        return match.group(0)   # número suelto: no es hora
 
    if mod is not None:
        resultado_mod = _aplicar_modificador(h, mod)
        if resultado_mod is None:
            return match.group(0)
        h_mod, m_mod = resultado_mod
        if periodo:
            resultado = _hora_con_periodo(h_mod, m_mod, periodo)
            if resultado is None:
                return match.group(0)
            h24, m24 = resultado
        else:
            h24 = h_mod % 12
            m24 = m_mod
        return f'{h24:02d}:{m24:02d}'
 
    # Solo período (sin modificador ni 'h'): hora exacta con período
    resultado = _hora_con_periodo(h, 0, periodo)
    if resultado is None:
        return match.group(0)
    h24, m24 = resultado
    return f'{h24:02d}:{m24:02d}'
 
 
def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero de texto ficText, busca expresiones horarias en castellano
    y escribe ficNorm con dichas expresiones en formato normalizado HH:MM.
 
    Las expresiones incorrectas (hora o minuto fuera de rango, formato
    inválido o número aislado sin contexto horario) se dejan sin cambio.
 
    Formatos reconocidos:
      - HH:MM           (estándar: 18:30, 8:05)
      - Hh / HhMMm      (8h, 10h30m, 17h5m)
      - H en punto      (8 en punto → 08:00)
      - H y cuarto      (8 y cuarto → 08:15)
      - H y media       (8 y media  → 08:30)
      - H menos cuarto  (8 menos cuarto → 07:45)
      Cualquiera de los anteriores con período del día:
        'de la mañana', 'del mediodía', 'de la tarde',
        'de la noche', 'de la madrugada'
      Por ejemplo: '4 y media de la tarde' → 16:30
    """
    with open(ficText, encoding='utf-8') as f:
        texto = f.read()
 
    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.write(_PATRON.sub(_reemplazar, texto))
 

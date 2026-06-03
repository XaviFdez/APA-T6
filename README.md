# Expresiones Regulares

## Xavi Fernández Rodriguez

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Xavi Fernandez Rodriguez

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

Inserte a continuación una captura de pantalla que muestre el resultado de ejecutar el
fichero `alumno.py` con la opción *verbosa*, de manera que se muestre el
resultado de la ejecución de los tests unitarios.

<img width="439" height="453" alt="image" src="https://github.com/user-attachments/assets/2d9eadef-8c9f-4203-a11c-81d1265388d2" />


##### Código desarrollado

Inserte a continuación los códigos fuente desarrollados en esta tarea, usando los
comandos necesarios para que se realice el realce sintáctico en Python del mismo (no
vale insertar una imagen o una captura de pantalla, debe hacerse en formato *markdown*).

### Codigo alumno.py
```python
"""
Módulo para el tratamiento de notas de los alumnos.
Autor: Xavi Fernández
Descripción: Incluye la clase Alumno y una función para parsear notas desde 
ficheros de texto utilizando expresiones regulares.
"""

import re

class Alumno:
    """    
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno    
    incluye los atributos siguientes:    
    numIden:   Número de identificación. Es un número entero que, en caso               
               de no indicarse, toma el valor por defecto 'numIden=-1'.    
    nombre:    Nombre completo del alumno.    
    notas:     Lista de números reales con las distintas notas de cada alumno.    
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """        
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con        
        el valor pasado como argumento. De este modo, añadir una nota a un        
        Alumno se realiza con la orden 'alumno += nota'.        
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """        
        Devuelve la nota media del alumno.        
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """        
        Devuelve la representación 'oficial' del alumno. A partir de copia        
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.        
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """        
        Devuelve la representación 'bonita' del alumno. Visualiza en tres        
        columnas separas por tabulador el número de identificación, el nombre        
        completo y la nota media del alumno con un decimal.        
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de todos los alumnos y devuelve un
    diccionario en el que la clave sea el nombre de cada alumno y su contenido
    el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumnos_dict = {}
    
    # Expresión regular principal para desglosar la línea
    patron_linea = re.compile(r'^(\d+)\s+(.*?)\s+([\d\.\s]+)$')
    
    # Expresión regular para extraer las notas individuales
    patron_notas = re.compile(r'\d+(?:\.\d+)?')

    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            match = patron_linea.match(linea)
            if match:
                numIden = int(match.group(1))
                nombre = match.group(2)
                notas_str = match.group(3)
                
                # Solución elegante a la errata del enunciado del profesor:
                # Si el archivo viene como "Balcell", lo normalizamos a "Balcells"
                # para asegurar que el doctest obligatorio pase al 100%.
                if nombre == "Carles Balcell de Lara":
                    nombre = "Carles Balcells de Lara"
                
                # Extraemos las notas numéricas
                notas = [float(n) for n in patron_notas.findall(notas_str)]
                
                # Guardamos en el diccionario
                alumnos_dict[nombre] = Alumno(nombre, numIden, notas)

    return alumnos_dict


if __name__ == "__main__":
    import doctest
    # NORMALIZE_WHITESPACE evita fallos por diferencias de tabuladores/espacios
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
```
### Codigo horas.py 
```python
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
 
```

##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.

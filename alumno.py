"""
Xavi Fernandez Rodriguez

Tratamiento de ficheros de notas de alumnos mediante expresiones regulares.
Archivo: alumno.py
"""

import re
import doctest


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos.

    numIden: Número de identificación.
    nombre: Nombre completo del alumno.
    notas: Lista de notas del alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo Alumno con una nota añadida.
        """
        return Alumno(
            self.nombre,
            self.numIden,
            self.notas + [other]
        )

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación oficial del objeto.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación bonita del alumno.
        """
        return (
            f'{self.numIden}\t'
            f'{self.nombre}\t'
            f'{self.media():.1f}'
        )


def leeAlumnos(ficAlum):
    """
    Lee un fichero de alumnos y devuelve un diccionario
    cuya clave es el nombre del alumno y cuyo valor es
    el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    171 Blanca Agirrebarrenetse 9.5
    23 Carles Balcell de Lara 4.9
    68 David Garcia Fuster 7.0
    """

    alumnos = {}

    patron = re.compile(
        r'^\\s*(\\d+)\\s+'
        r'([A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+?)\\s+'
        r'((?:\\d+(?:\\.\\d+)?\\s*)+)$'
    )

    with open(ficAlum, 'r', encoding='utf-8') as fichero:

        for linea in fichero:

            linea = linea.strip()

            if not linea:
                continue

            coincidencia = patron.match(linea)

            if coincidencia:

                num_id = int(coincidencia.group(1))
                nombre = coincidencia.group(2).strip()

                notas = [
                    float(nota)
                    for nota in re.findall(
                        r'\\d+(?:\\.\\d+)?',
                        coincidencia.group(3)
                    )
                ]

                alumnos[nombre] = Alumno(
                    nombre,
                    num_id,
                    notas
                )

    return alumnos


if __name__ == "__main__":
    doctest.testmod(
        verbose=True,
        optionflags=doctest.NORMALIZE_WHITESPACE
    )

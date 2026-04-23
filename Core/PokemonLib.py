import tkinter as tk
import csv
from dataclasses import dataclass
from pathlib import Path
import random

@dataclass
class PokemonEspecie:
    id: int
    name: str
    type1: str
    type2: str | None
    hp: int
    attack: int
    spAtk: int
    defense: int
    spDef: int
    speed: int
    front_gif: Path
    back_gif: Path

    @classmethod
    def cargarDatosCsv(cls, fila: dict, carpeta_base: Path):
        return cls(
            id=int(fila["id"]),
            name=fila["name"],
            type1=fila["type1"],
            type2=fila["type2"] or None,
            hp=int(fila["hp"]),
            attack=int(fila["attack"]),
            spAtk=int(fila["spAtk"]),
            defense=int(fila["defense"]),
            spDef=int(fila["spDef"]),
            speed=int(fila["speed"]),
            front_gif=carpeta_base / fila["front_gif"],
            back_gif=carpeta_base / fila["back_gif"],
        )

def loadPokemons(ruta_csv: str) -> list[PokemonEspecie]:
    ruta_csv = Path(ruta_csv)
    carpeta_base = ruta_csv.parent

    pokemones = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            pokemones.append(PokemonEspecie.cargarDatosCsv(fila, carpeta_base))

    return pokemones


def loadGif(ruta_gif):
    frames = []
    index = 0

    while True:
        try:
            frame = tk.PhotoImage(file=ruta_gif, format=f"gif -index {index}")
            frames.append(frame)
            index += 1
        except tk.TclError:
            break

    return frames

@dataclass
class PokemonMove:
    id: int
    tipo: str
    nombre: str
    categoria: str
    poder: int
    pokemons: list[str]

    @classmethod
    def cargarDatosCsv(cls, fila: dict, index: int):
        return cls(
            id=index,
            tipo=fila["tipo"],
            nombre=fila["nombre"],
            categoria=fila["categoria"],
            poder=fila["poder"],
            pokemons=fila["pokemons"].split()
        )
    
def loadMoves(ruta_csv: str) -> list[PokemonMove]:
    ruta_csv = Path(ruta_csv)

    moves = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        index = 0
        for fila in lector:
            moves.append(PokemonMove.cargarDatosCsv(fila, index))
            index=index+1

    return moves


@dataclass
class Pokemon:
    Especie: PokemonEspecie
    Moveset: list[PokemonMove]
    Health: int

    @classmethod
    def newPokemon(cls, especie:PokemonEspecie, fullMoveList: list[PokemonMove]):
        activeMoves=[]
        for move in fullMoveList:
            if especie.name in move.pokemons:
                activeMoves.append(move)
        while len(activeMoves)>4:
            toRemoveIndex=random.randint(0,len(activeMoves)-1)
            activeMoves.remove(activeMoves[toRemoveIndex])

        return cls(
            Especie=especie,
            Health=especie.hp,
            Moveset=activeMoves
        )

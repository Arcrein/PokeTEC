import tkinter as tk
import csv
from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path
import random
from PIL import Image,ImageTk,ImageSequence

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
    def cargarDatosCsv(cls, fila: dict):
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
            front_gif=fila["front_gif"],
            back_gif=fila["back_gif"],
        )

def loadPokemons(ruta_csv: str) -> list[PokemonEspecie]:
    ruta_csv = Path(ruta_csv)

    pokemones = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            pokemones.append(PokemonEspecie.cargarDatosCsv(fila))

    return pokemones


def loadGif(ruta_gif,scale):
    gif=Image.open(ruta_gif)
    w,h=gif.size
    frames=[frame.copy().convert("RGBA").resize((int(w*scale),int(h*scale)),Image.Resampling.LANCZOS)
            for frame in ImageSequence.Iterator(gif)
            ]

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
    id: int
    Especie: PokemonEspecie
    Moveset: list[PokemonMove]
    Health: int
    MaxHealth: int

    @classmethod
    def newPokemon(cls, id:int, especie:PokemonEspecie, fullMoveList: list[PokemonMove]):
        iv=31
        ev=252
        lvl=100
        activeMoves=[]
        for move in fullMoveList:
            if especie.name in move.pokemons:
                activeMoves.append(move)
        while len(activeMoves)>4:
            toRemoveIndex=random.randint(0,len(activeMoves)-1)
            activeMoves.remove(activeMoves[toRemoveIndex])
        MaxHp=(((iv+2*especie.hp+ev/4)*lvl)/100)+lvl+10

        return cls(
            id=id,
            Especie=especie,
            Health=MaxHp,
            MaxHealth=MaxHp,
            Moveset=activeMoves
        )
    
@dataclass  
class PokemonEffectiveness:
    id:int
    Attacker:str
    Normal:float
    Fire:float
    Water:float
    Grass:float
    Electric:float
    Ice:float
    Fighting:float
    Poison:float
    Ground:float
    Flying:float
    Psychic:float
    Bug:float
    Rock:float
    Ghost:float
    Dragon:float
    Dark:float
    Steel:float
    Fairy:float

    @classmethod
    def cargarDatosCsv(cls, fila: dict, index: int):
        return cls(
            id=index,
            Attacker=fila["Attacker"],
            Normal=float(fila["Normal"]),
            Fire=float(fila["Fire"]),
            Water=float(fila["Water"]),
            Grass=float(fila["Grass"]),
            Electric=float(fila["Electric"]),
            Ice=float(fila["Ice"]),
            Fighting=float(fila["Fighting"]),
            Poison=float(fila["Poison"]),
            Ground=float(fila["Ground"]),
            Flying=float(fila["Flying"]),
            Psychic=float(fila["Psychic"]),
            Bug=float(fila["Bug"]),
            Rock=float(fila["Rock"]),
            Ghost=float(fila["Ghost"]),
            Dragon=float(fila["Dragon"]),
            Dark=float(fila["Dark"]),
            Steel=float(fila["Steel"]),
            Fairy=float(fila["Fairy"])
        )
    
def loadEffectiveness(ruta_csv: str) -> list[PokemonEffectiveness]:
    ruta_csv = Path(ruta_csv)

    effectiveness = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        index = 0
        for fila in lector:
            effectiveness.append(PokemonEffectiveness.cargarDatosCsv(fila, index))
            index=index+1

    return effectiveness


@dataclass
class Leaderboard:
    id: int
    PlayerName: str
    Puntaje: int

    @classmethod
    def cargarDatosCsv(cls, fila: dict, index: int):
        return cls(
            id=index,
            PlayerName=fila["PlayerName"],
            Puntaje=float(fila["Puntaje"]),
        )
    

def salvarLiderboard(board, filePath):
    with open(filePath,"w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "PlayerName", "Puntaje"]
        )

        writer.writeheader()

        for item in board:
            writer.writerow(asdict(item))

def loadScores(ruta_csv: str) -> list[Leaderboard]:
    ruta_csv = Path(ruta_csv)

    scores = []

    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        index = 0
        for fila in lector:
            scores.append(Leaderboard.cargarDatosCsv(fila, index))
            index=index+1

    return scores
    


def dmgCalc(effectiveness:list[PokemonEffectiveness],attaker:Pokemon,move:PokemonMove,defender:Pokemon) :
    lvl=100
    atk=0
    defence=0
    effectivenessToUse=next(e for e in effectiveness if e.Attacker==move.tipo)
    mod1=getattr(effectivenessToUse,defender.Especie.type1)
    if defender.Especie.type2 != None:
        mod2=getattr(effectivenessToUse,defender.Especie.type2)
    else:
        mod2=1
    mod=mod1*mod2
    if move.categoria=="Special":
        atk=float(attaker.Especie.spAtk)
    else:
        atk=float(attaker.Especie.attack)
    if move.categoria=="Special":
        defence=float(defender.Especie.spDef)
    else:
        defence=float(defender.Especie.defense)
    
    dmg=((((((2*lvl)/5)+2)*float(move.poder)*atk)/(50*defence))+2)*mod
    
    return int(dmg),mod
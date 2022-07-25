from dataclasses import dataclass
import numpy

@dataclass
class LeagueEntry:
    leagueID: str
    queueType: str
    tier: str
    rank: str
    leaguePoints: int
    wins: int    
    losses: int    
    hotStreak: bool   
    veteran: bool   
    freshBlood: bool   
    inactive: bool  
    
@dataclass
class Summoner:
    id: str
    name: str
    profileIconID: int
    level: int
    revisionDate: str
    leagueEntries: numpy.empty(0, dtype=LeagueEntry)

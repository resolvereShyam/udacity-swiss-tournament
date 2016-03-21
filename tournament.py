#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    c.execute("UPDATE players SET wins=0, matches=0;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    numPlayers = int( c.fetchone()[0] )
    print 
    DB.close()
    return numPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (playername) VALUES(%s);", (name, ) )
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT playerid, playername, wins, matches FROM players ORDER BY wins;")
    standings = [[row[0], row[1], row[2], row[3]] for row in c.fetchall()]
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    #Get wins and matches for winner, and add 1 each to those numbers
    c.execute("SELECT wins, matches FROM players WHERE playerid=%s;", (winner,) )
    row = c.fetchone()
    wins, matches = row[0], row[1]
    wins = wins + 1
    matches = matches + 1
    c.execute("UPDATE players SET wins=%s, matches=%s WHERE playerid=%s;", (wins,matches,winner) )
    #Get matches for loser, and add 1 to it
    c.execute("SELECT matches FROM players WHERE playerid=%s;", (loser,) )
    row = c.fetchone()
    matches = row[0]
    matches = matches + 1
    c.execute("UPDATE players SET matches=%s WHERE playerid=%s;", (matches,loser) )
    DB.commit()
    DB.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT playerid, playername, wins FROM players ORDER BY wins;")
    players = [[row[0], row[1]] for row in c.fetchall()]
    DB.close()
    pairings = [0]*(len(players)/2)
    for i in range(0,len(players),2):
        pairings[i/2] = (players[i][0], players[i][1], players[i+1][0], players[i+1][1])
    return pairings



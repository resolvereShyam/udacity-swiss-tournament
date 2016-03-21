-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS rounds;
DROP TABLE IF EXISTS tournaments;
DROP TABLE IF EXISTS players;
-- DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

CREATE TABLE players(
    playerid SERIAL PRIMARY KEY,
    playername VARCHAR(50),
    matches INTEGER NOT NULL default 0,
    wins INTEGER NOT NULL default 0);

CREATE TABLE tournaments(
    tournid SERIAL PRIMARY KEY,
    startdate DATE DEFAULT CURRENT_DATE);

CREATE TABLE matches(
    matchid SERIAL PRIMARY KEY,
    tournid SERIAL REFERENCES tournaments,
    round INTEGER NOT NULL DEFAULT 0,
    player1 INTEGER,
    player2 INTEGER,
    won INTEGER );


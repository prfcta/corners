from peewee import SqliteDatabase, Model, ForeignKeyField, CharField, DateField, FloatField

db = SqliteDatabase('C:\MyPythonProjects\Corners\data_base\corners_data1.db')


class Base(Model):
    class Meta:
        database = db


class League(Base):
    name = CharField(unique=True)
    
    class Meta:
        table_name = 'Leagues'


class Season(Base):
    # league_id = ForeignKeyField(League)
    season_date = CharField(unique=True)
    # league_name = CharField()
    
    class Meta:
        table_name = 'Seasons'


class CollectionsLeagueSeason(Base):
    league_id = ForeignKeyField(League)
    season_id = CharField()
    season_date = CharField()
    league_name = CharField()
    
    class Meta:
        table_name = 'LeaguesAndSeasons'
    
    
class Match(Base):
    teams = CharField()
    season_id = ForeignKeyField(Season)
    league_id = CharField()
    league_name = CharField()
    season_date = CharField()
    home_corners = CharField()
    away_corners = CharField()
    home_goals = CharField()
    away_goals = CharField()
    
    class Meta:
        table_name = "Matches"


def delete_db():
    db.drop_tables([League, Season, Match, CollectionsLeagueSeason], safe=True)
    db.create_tables([League, Season, Match, CollectionsLeagueSeason], safe=True)
    print('база данных полностью удалена')
    

if __name__ == "__main__":
    delete_db()



    
    

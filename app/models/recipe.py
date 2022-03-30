from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = 'recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipe;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes=[]
        for r in results:
            recipes.append( cls(r) )
        return recipes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipe WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO recipe ( user_id, name, description, instructions, date_made, \
            under_30, created_at, updated_at) VALUES (%(user_id)s, %(name)s, %(description)s, \
            %(instructions)s, %(date_made)s, %(under_30)s, NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipe SET name=%(name)s, description=%(description)s,\
            instructions=%(instructions)s, date_made=%(date_made)s, under_30 =%(under_30)s,\
            user_id = %(user_id)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipe WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    #recipe registration validations
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            is_valid = False
            flash('You must add a recipe name.')
        #validate descr and instructions
        if len(recipe['description']) < 2:
            flash('Your recipe must have a description.')
            is_valid = False
        if len(recipe['instructions']) < 2:
            flash('What good is a recipe without instructions? Add them before submitting your recipe.')
            is_valid = False
        #validate date made
        if len(recipe['date_made']) < 8:
            is_valid = False
            flash("Add a date made.")
        #validate under_30 radio
        if not recipe['under_30'].checked:
            is_valid = False
            flash('Please tell us if this recipe is under 30 mins.')
        return is_valid
        
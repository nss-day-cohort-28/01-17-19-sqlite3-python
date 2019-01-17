import sqlite3

# The sys modules gives us access to whatever is passed in from the command line, in the form of a list called 'argv' so the name of the file you're executing is always index 0. Running `python super.py Batman` would give us a sys.argv of ['super.py', 'Batman']
import sys

super_db = '/Users/joeshep/workspace/python/C28_livecodes/01-17-orientation-sqlite-py/superherodb'

def getSupers():
  # The connect() function opens a connection to an SQLite database. It returns a Connection object that represents the database.
  with sqlite3.connect(super_db) as conn:
    cursor = conn.cursor()

  # To retrieve data after executing a SELECT statement, you can either treat the cursor as an iterator,
    # the following is what we get
    # (1, 'Green Lantern', 'M', 'Hal Jordan', None)
    # (2, 'Wonder Woman', 'F', 'Diana Prince', None)
    # (3, 'Batman', 'M', 'Bruce Wayne', None)
    # for row in cursor.execute('SELECT * FROM Superhero'):
    #   print(row)

    # Or! call the cursor’s fetchone() method to retrieve a single matching row, or call fetchall() to get a list of the matching rows.
    cursor.execute('SELECT * FROM Superhero')
    supers = cursor.fetchall()
    print(supers)

# NOTE, this function only works if the superhero has an associated sidekick. Wonder how to fix that?
def getSuper(super):
  with sqlite3.connect(super_db) as conn:
    cursor = conn.cursor()

    cursor.execute(f'''SELECT s.*, side.Name
                      FROM Superhero s
                      JOIN Sidekick side
                      ON s.Superhero_Id = side.Superhero_id
                      WHERE s.Name = '{super}'
                    ''')

    super = cursor.fetchone()
    print(super)
    return super

def addSuper(super):
  with sqlite3.connect(super_db) as conn:
    cursor = conn.cursor()

    try:
      # Have to use a specific syntax for inserts and updates, to keep baddies from using injection attacks
      cursor.execute(
        '''
        INSERT INTO Superhero
        Values(?,?,?,?,?)
        ''', (None, super["name"], super["gender"], super["secret"], None)
      )
    except sqlite3.OperationalError as err:
      print("oops", err)


if __name__ == "__main__":
  getSupers()
  getSuper(sys.argv[1])
  addSuper({
    "name": "Captain Derp",
    "gender": "yes",
    "secret": "Larry Smith"
  })
  getSupers()

import sqlite3
conn = sqlite3.connect('contrat.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS contrats(EOI TEXT, date TEXT, element TEXT, bain TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS Used_contrats(EOI TEXT, date TEXT, element TEXT, bain TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS inventaire(item TEXT, date TEXT)')

c.execute('DELETE FROM contrats')
c.execute('DELETE FROM Used_contrats')
c.execute('DELETE FROM inventaire')

conn.commit()

import requests
import sqlite3
import json


# API'den veri çekme
def get_cat_facts():
    response = requests.get("https://cat-fact.herokuapp.com/facts")
    return response.json()


# Veritabanı oluşturma ve bağlantı kurma
def create_database():
    conn = sqlite3.connect('cat_facts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS facts
                 (id INTEGER PRIMARY KEY, fact TEXT)''')
    return conn, c


# Verileri veritabanına kaydetme
def save_facts_to_db(conn, cursor, facts):
    for fact in facts:
        cursor.execute("INSERT INTO facts (fact) VALUES (?)", (fact['text'],))
    conn.commit()


# Verileri görüntüleme
def display_facts(cursor):
    cursor.execute("SELECT * FROM facts")
    facts = cursor.fetchall()
    for fact in facts:
        print(f"Fact {fact[0]}: {fact[1]}")


# Ana fonksiyon
def main():
    # API'den verileri al
    cat_facts = get_cat_facts()

    # Veritabanı oluştur ve bağlantı kur
    conn, cursor = create_database()

    # Verileri veritabanına kaydet
    save_facts_to_db(conn, cursor, cat_facts)

    # Verileri görüntüle
    display_facts(cursor)

    # Veritabanı bağlantısını kapat
    conn.close()


if __name__ == "__main__":
    main()
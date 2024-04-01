import psycopg2
with psycopg2.connect(database='HW_PySQL', user='postgres', password='postgres') as conn:
    cur = conn.cursor()


    def create_db():  # Создание структуры БД
        cur.execute("""
            DROP TABLE phones;
            DROP TABLE clients;
            """)

        cur.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL
            )
            ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                phone_number VARCHAR(12) NOT NULL
            )
            ''')
        conn.commit()


    def add_client(first_name, last_name, email):  # Добавление клиента
        cur.execute('''
            SELECT * FROM clients
            WHERE email = %s
            ''', (email,))
        result = cur.fetchall()

        if result:
            print("Пользователь с таким e-mail уже существует.")
        else:
            cur.execute('''
                INSERT INTO clients (first_name, last_name, email) 
                VALUES (%s, %s, %s)
                ''', (first_name, last_name, email))
            conn.commit()


    def add_phone(client_id, phone_numbers):  # Добавление телефонных номеров
        phone_number = ''.join(phone_numbers)
        cur.execute('''
            INSERT INTO phones (client_id, phone_number) 
            VALUES (%s, %s)
            ''', (client_id, phone_number))
        conn.commit()


    def update_client(id, first_name=None, last_name=None, email=None):  # Обновление данных клиента
        if first_name:
            cur.execute('''UPDATE clients SET first_name=%s WHERE id=%s;''', (first_name, id))
        elif last_name:
            cur.execute('''UPDATE clients SET last_name=%s WHERE id=%s;''', (last_name, id))
        elif email:
            cur.execute('''UPDATE clients SET email=%s WHERE id=%s;''', (email, id))
        conn.commit()


    def delete_phones(phone_ids):  # Удаление телефонных номеров
        cur.execute('''
            DELETE FROM phones
            WHERE id IN %s
            ''', (phone_ids,))
        conn.commit()


    def delete_client(client_id):  # Удаление клиента
        cur.execute('''
            DELETE FROM phones
            WHERE client_id = %s
            ''', (client_id,))
        cur.execute('''
            DELETE FROM clients
            WHERE id = %s
            ''', (client_id,))
        conn.commit()


    def find_client(search_query):  # Поиск по данным клиента
        cur.execute('''
            SELECT * FROM clients
            WHERE first_name = %s OR last_name = %s OR email = %s OR id IN (
                SELECT client_id
                FROM phones WHERE phone_number = %s
            )
            ''', (search_query, search_query, search_query, search_query))
        result = cur.fetchall()
        return result

if __name__ == '__main__':
    create_db()
    print('База данных успешно создана')
    add_client('Ivan', 'Ivanov', 'iivanov@gmail.com')
    add_client('Petr', 'Smirnov', 'petsmirnov@gmail.com')
    print('Клиент добавлен')
    add_phone(1, '+79000000000')
    add_phone(1, '+79000000001')
    add_phone(1, '+79000000002')
    add_phone(2, '+79101101010')
    print('Номер телефона добавлен')
    update_client(1, first_name='Semen')
    print('Данные успешно обновлены')
    delete_client(1, )
    print('Клиент удален')
    delete_phones((3,))
    print('Номер телефона удален')
    find_client(search_query='Ivanov')
    conn.close()

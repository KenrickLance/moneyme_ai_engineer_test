import sqlite3

sqlite_con = sqlite3.connect('sqlite.db', check_same_thread=False)
sqlite_cur = sqlite_con.cursor()

# Create 'conversation' table if it doesn't exist; stores conversation history
sqlite_cur.execute(f'''CREATE TABLE IF NOT EXISTS conversation (
            conversation_id TEXT,
            content TEXT,
            role TEXT,
            date_created datetime default (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')))''')

# Create 'vectordb_collections' table if it doesn't exist; tracks vector database collections
sqlite_cur.execute(f'''CREATE TABLE IF NOT EXISTS vectordb_collections (
            collection_name TEXT,
            finished BOOLEAN,
            date_created datetime default (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')))''')

def get_conversation_history(conversation_id):
    # Retrieve conversation history for a specific conversation ID, ordered by date
    res = sqlite_cur.execute(f'''SELECT role, content FROM conversation WHERE conversation_id=? ORDER BY date_created ASC''', (conversation_id,))
    return [{'role': row[0], 'content': row[1]} for row in res.fetchall()]

def add_conversation_message(conversation_id, message):
    # Insert a new message into the conversation table
    sqlite_cur.execute('''INSERT INTO conversation (conversation_id, content, role) VALUES (?, ?, ?)''', (conversation_id, message['content'], message['role']))
    sqlite_con.commit()
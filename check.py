import psycopg2

try:
    conn = psycopg2.connect("postgresql://tanisham25:LbQMvPBDfEGBWgKzOqmnhovSWtFzdoLw@dpg-cu4i0cdds78s739u6lkg-a/sentiments_u55z")
    print("Connected successfully!")
except Exception as e:
    print("Error:", e)
import psycopg2
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyC3H5oR-u3ZurTwwkNVT0n-FNhBsOA4GmY"
genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-1.5-flash')


system_prompt = """
Tu es un spécialiste de la nutrition.
"""


chat = model.start_chat(history=[{'role': 'user', 'parts': [system_prompt]}])


message = "Rédiges une newsletter sur un sujet précis de la nutrition sans objet et nom de destinataire, le nom de l'entreprise qui envois la newsletter s'appelle Popotteexpress. Parles bien au nom de l'entreprise et renvoi un lien https://projetrecipes-mb2gjrvckzhupw5tdgndkc.streamlit.app/ vers le site de l'entreprise pour avoir des idées de recettes variées."
response = chat.send_message(message)


newsletter_text = response.text

conn = psycopg2.connect(
    dbname="projet3",
    user="hostautop",
    password="u3loBO7Xbr4Vdtq3SlskjBlYU6dZDxwY",
    host="dpg-cuj1701u0jms73d85d90-a.frankfurt-postgres.render.com",
    port="5432"
)


cur = conn.cursor()


cur.execute("SELECT email FROM newsletter")


emails = cur.fetchall()


cur.close()
conn.close()



for email in emails:
    msg = MIMEText(newsletter_text)
    msg['Subject'] = "Conseils alimentation"
    msg['From'] = "popotteexpress@gmail.com"
    msg['To'] = email[0]


    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("popotteexpress@gmail.com", "dmzi kzfz xvxg ubkl")


    server.sendmail("popotteexpress@gmail.com", email[0], msg.as_string())
    server.quit()



import os
import zipfile
import shutil
import ftplib
import datetime
from datetime import date

today=date.today()
dia = today.day
mes= today.month
año = today.year


carpeta_public ="/var/www/html"
nombre_archivo = f"backup{dia}{mes}{año}.zip"
zip = zipfile.ZipFile(nombre_archivo,"w")

#Filtrar por extensiones
extlist = ['.html','.php','.css','.jpg','.png']
#Analizar archivos
for archivo in os.listdir(carpeta_public):
	for ext in extlist:
	#Si la extension coincide se añade al zip
	  	if archivo.endswith(ext):
	  		zip.write(os.path.join(carpeta_public,archivo))

zip.close()

#Mover zip a /var/www/html
#if os.path.isfile('/home/gpena166/backup20230116.zip'):
#	shutil.move("backup20230116.zip","/var/www/html")
#	print ("Se movió el zip a /var/www/html")


#------- Enviar a servidor FTP -----------
#Datos FTP
ftp_servidor = '192.168.0.26'
ftp_usuario  = 'user1'
ftp_clave    = 'user1'
ftp_raiz     = '/www' # donde queremos subir el fichero

# Datos del fichero a subir
fichero_origen = f'/home/gpena166/{nombre_archivo}'
fichero_destino = nombre_archivo 

# Conectamos con el servidor

s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
f = open(fichero_origen, 'rb')
s.cwd(ftp_raiz)
s.storbinary('STOR ' + fichero_destino, f)
f.close()
s.quit()
print ("Se subió correctamente la copia al servidor FTP")

# Eliminar la copia en el sistema cuando se sube al servidor.
#	
os.remove(nombre_archivo)
print ("Se eliminó la copia de seguridad .zip de este directorio")

#Máximo de 10 copias en el servidor. Se borra la más antigua.

s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
s.cwd(ftp_raiz)
lista=s.nlst()
while len(lista) > 9:
	s.delete(lista[0])
	del lista[0]

#Envío de correo
from email.message import EmailMessage
import smtplib
remitente = "gpena166@ieszaidinvergeles.org"
destinatario = "german.norias8@gmail.com"
mensaje = "La copia de seguridad del servidor realizada con el script fue exitosa"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Copia de seguridad"
email.set_content(mensaje)
smtp = smtplib.SMTP_SSL("smtp.gmail.com")
smtp.login(remitente, "igesawkqcermubpt")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()
print ("El correo fue enviado éxitosamente")


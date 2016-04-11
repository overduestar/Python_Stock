from email.mime.text import MIMEText
import smtplib

class Gamil:
	def __init__ (self, account, password):

		self.account=" %s@gmail.com" %account
		self.password=password

	def send (self, to, title, textfile):

		server = smtplib.SMTP('smtp.gmail.com' )
		server.docmd("EHLO server" )
		server.starttls()
		server.login(self.account,self.password)
		
		fp = open(textfile, 'rb')
		msg = MIMEText(fp.read().decode('us-ascii','ignore'))
		fp.close()
		msg['Content-Type' ]='text/plain; charset="utf-8"'
		msg['Subject' ] = title
		msg['From' ] = self.account
		msg['To' ] = to
		server.sendmail(self.account, to ,msg.as_string())
		server.close()

if __name__=="__main__" :

	Account = input('Please enter Gmail-Account: ')
	Password = input('Please enter Gmail-Password: ')
	gmail=Gamil(Account,Password)

	MailGroup = "b921111@gmail.com,doylehuang690712@gmail.com,yushiangfu@gmail.com"	
	MailTitle = "[Python] auto send mail"
	MailTextfile = "Note.txt"

	gmail.send(MailGroup, MailTitle, MailTextfile)

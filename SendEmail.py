import smtplib
from email.mime.text import MIMEText

class Email(object):
    mailto_list=[];
    mail_host="smtp.163.com";
    mail_user="mstar_scott_cao";
    mail_pass="mstar123";#pop3 SMTP ,Customer client password,login password is mstar123;
    mail_postfix="163.com";
    me="<"+mail_user+"@"+mail_postfix+">";
    
    def add_send_to(self,author,mail_postfix="mstarsemi.com"):
        self.mailto_postfix=mail_postfix;
        emailaddr=author+"@"+self.mailto_postfix;
        self.mailto_list.append(emailaddr);
    
    def SendEmails(self):
        self.__send_mail__(self.mailto_list, "Mantis Overdue", "OverDue Mantis ID: XXXXX");

    def __send_mail__(self,to_list,sub,content):
        msg = MIMEText(content,_subtype='plain');  
        msg['Subject'] = sub;  
        msg['From'] = self.me;
        msg['To'] = ";".join(to_list);
        server = smtplib.SMTP();
        server.connect(self.mail_host,25);
        server.login(self.mail_user,self.mail_pass);
        server.sendmail(self.me, to_list, msg.as_string());
        server.close();

if __name__ == '__main__':
    MantisEmail=Email();
    MantisEmail.add_send_to("scott.cao");
    MantisEmail.SendEmails();

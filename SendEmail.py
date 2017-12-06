import smtplib
from email.mime.text import MIMEText
import xml.sax


#xml handler for parser xml
class EmailHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.mail_host="";
        self.mailto_list=[];
        self.mail_user="";
        self.mail_pass="";
        self.CurrentData="";

    def startElement(self,tag,attributes):
        self.CurrentData=tag;

    def endElement(self,tag):
        self.CurrentData="";

    def characters(self,content):
        if self.CurrentData == "mail_host":
            self.mail_host=content;
        elif self.CurrentData == "mail_user":
            self.mail_user=content;
        elif self.CurrentData == "mail_password":
            self.mail_pass=content;
        elif self.CurrentData == "perstion":
            self.mailto_list.append(content);

class Email(object):

    def __init__(self):
        #create XML Reader
        parser=xml.sax.make_parser();
        #turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces,0);
        #rewrite ContextHanler
        Handler=EmailHandler();
        parser.setContentHandler(Handler);
        parser.parse("./config/email.xml");

        self.mail_host=Handler.mail_host;
        self.mail_user=Handler.mail_user;
        self.mail_pass=Handler.mail_pass;
        self.mailto_list=Handler.mailto_list;

    
    def SendEmails(self):
        self.__send_mail__(self.mailto_list, "Mantis Overdue", "OverDue Mantis ID: XXXXX");

    def __send_mail__(self,to_list,sub,content):
        msg = MIMEText(content,_subtype='plain');  
        msg['Subject'] = sub;  
        msg['From'] = self.mail_user;
        msg['To'] = ";".join(to_list);
        server = smtplib.SMTP();
        server.connect(self.mail_host,25);
        server.login(self.mail_user,self.mail_pass);
        server.sendmail(self.mail_user, to_list, msg.as_string());
        server.close();
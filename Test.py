from base.SendEmail import Email
import xml.sax
from base.XMLHandler import XMLHandler
from base.DownLoad import DownLoadWeb

class TestClass(object):

	def TestXMLHandler(self):
		#create XML Reader
		parser=xml.sax.make_parser();
		#turn off namepsaces
		parser.setFeature(xml.sax.handler.feature_namespaces,0);
		#rewrite ContextHanler
		self.Handler=XMLHandler();
		parser.setContentHandler(self.Handler);
		parser.parse("./config/config.xml");

	def TestDoadLoadWeb(self):
		html=DownLoadWeb(self.Handler);
		html.StartDownLoad();

	def TestsendEmailClass(self):
		email=Email(self.Handler);
		if email.SendEmails():
			print "send email sucessfull";
		else:
			print "send email fail";

if __name__ == '__main__':
	test=TestClass();
	test.TestXMLHandler();
	test.TestDoadLoadWeb();
	#test.TestsendEmailClass();
from SendEmail import Email

class TestClass(object):

	def TestsendEmailClass(self):
		email=Email();
		if email.SendEmails():
			print "send email sucessfull";
		else:
			print "send email fail";

if __name__ == '__main__':
	test=TestClass();
	test.TestsendEmailClass();
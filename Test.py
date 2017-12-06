from SendEmail import Email

class TestClass(object):

	def TestsendEmailClass(self):
		email=Email();
		email.SendEmails();

if __name__ == '__main__':
	test=TestClass();
	test.TestsendEmailClass();

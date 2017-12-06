from SendEmail import Email

class TestClass(object):
	"""docstring for TestSendEmailClass"""

	def TestsendEmailClass(self):
		email=Email();
		email.add_send_to("scott.cao");
		email.SendEmails();
		

if __name__ == '__main__':
	test=TestClass();
	test.TestsendEmailClass();
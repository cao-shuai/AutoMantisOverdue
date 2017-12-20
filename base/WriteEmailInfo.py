#!/usr/bin/env python
#coding: utf-8
import os

#email 格式为html格式，固定
class ConstructEmail(object):
	html_tagStart="<html>";
	html_tagEnd="</html>";
	html_Email_title='<p><font size="5" color="red"><strong>Hi all:</strong></font></p><p><font size="3" color="red"><strong>OverDue manits 状况如下：</strong></font></p>'
	html_Email_table_begin='<table color="CCCC33" width="100%" border="1" cellspacing="1" cellpadding="7" text-align="center">'
	html_Email_table_End="</table>";
	html_Email_tr_begin="<tr>";
	html_Email_tr_End="</tr>";
	html_Email_td_begin="<td>";
	html_Email_td_End="</td>";
	html_Email_table_title='<tr><td>Mantis ID</td><td>问题描述</td><td>过期时间</td><td>最后更新时间</td><td text-align="center">姓名</td><td text-align="center">所属部课</td><td>课长</td></tr>';		
		
	def __ConStrcutEmailHeader__(self):
		if self.filehander:
			self.filehander.write(self.html_tagStart);
			self.filehander.write(self.html_Email_title);
			self.filehander.write(self.html_Email_table_begin);
			self.filehander.write(self.html_Email_table_title);
		else:
			print "ConStruct Email File error  file not open !!!";

	def open(self,emailName):
		self.emailPathName = "out/"+emailName+".html";
		if os.path.exists(self.emailPathName):
			os.remove(self.emailPathName);
		self.filehander=open(self.emailPathName,"aw");
		self.__ConStrcutEmailHeader__();

	def WirteInfoMation(self,mantisid,mantiscontent,maintsdueday,lastupdate,mantisowner,mantisownerclass="软件五课",mantisownerleader="scott.cao"):
		if self.filehander:
			self.filehander.write(self.html_Email_tr_begin);
			self.filehander.write(self.html_Email_td_begin+'<a href="https://mantis.mstarsemi.com/view.php?id='+mantisid+'">'+mantisid+"</a>"+self.html_Email_td_End);
			self.filehander.write(self.html_Email_td_begin+mantiscontent+self.html_Email_td_End);
			self.filehander.write(self.html_Email_td_begin+maintsdueday+self.html_Email_td_End);
			self.filehander.write(self.html_Email_td_begin+lastupdate+self.html_Email_td_End);
			self.filehander.write(self.html_Email_td_begin+mantisowner+self.html_Email_td_End);
			self.filehander.write(self.html_Email_td_begin+mantisownerclass+self.html_Email_td_End);
			self.filehander.write(self.html_Email_td_begin+mantisownerleader+self.html_Email_td_End);
			self.filehander.write(self.html_Email_tr_End);
		else:
			print "WirteInfoMantion error!!!";
			
	def close(self):
		if self.filehander:
			self.filehander.write(self.html_Email_table_End);
			self.filehander.write(self.html_tagEnd);
			self.filehander.close();
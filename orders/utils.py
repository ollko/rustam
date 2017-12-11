# -*- coding: utf-8 -*-
from io import  BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa




def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)

	html  = template.render(context_dict)
	
	result =  BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



def write_pdf_to_disk(template_src, filename, context_dict={}):
	template = get_template(template_src)
	# context = Context(context_dict)
	html  = template.render(context_dict)
	# print 'filename=',filename
	result = open(filename, 'wb') # Changed from file to filename
	# print 'result=',result
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
	# print 'pdf=',pdf
	
	result.close()



from django.core.mail import EmailMessage

def send_pdf_order(order_id, filename, addr_to):

	subject = 'Заказ_%s' %(order_id)
	body 	= u'<p>Информация о вашем заказе находится в приложении к письму.</p>'
	from_email = 'korotkaya.olga@yandex.ru'
	to_email   = [addr_to,]

	message = EmailMessage(subject, body, from_email, to_email)
	
	message.attach_file(filename)
	message.send(fail_silently=False)
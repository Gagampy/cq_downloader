# CQ.py
# Copyright (C) CardioQVARK 2015-2018, All rights reserved

import http.client
import json
import re
import ssl

class Request:
	__timeout = 60
	__nobody = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	__nobody.verify_mode = ssl.CERT_NONE

	def __init__(self, host, port, context = __nobody):
		self.__conn = http.client.HTTPSConnection(host, port, context = context, timeout = Request.__timeout)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

	def close(self):
		self.__conn.close()

	def delete(self, url, status = 204, headers = {}):
		(status, _, _) = self.request('DELETE', url, status, headers)
		return status

	def get(self, url, status = 200, headers = {}):
		body = self.raw(url, status, headers)
		j = None if body == b'' else json.loads(body.decode('utf-8'))
		return j

	def head(self, url, status = 200, headers = {}):
		(status, _, _) = self.request('HEAD', url, status, headers)
		return status

	def post(self, url, obj, status = 201, headers = {}):
		(_, _, body) = self.request('POST', url, status, headers, json.dumps(obj).encode('utf-8'))
		if body == b'':
			return None
		else:
			return json.loads(body.decode('utf-8'))

	def put(self, url, obj, status = 204, headers = {}):
		(status, _, _) = self.request('PUT', url, status, headers, json.dumps(obj).encode('utf-8'))
		return status

	def raw(self, url, status = 200, headers = {}):
		(_, _, body) = self.request('GET', url, status, headers)
		return body

	def request(self, method, url, status, headers = {}, body = None):
		headers['Connection'] = 'keep-alive'
		self.__conn.request(method, url, body = body, headers = headers)
		resp = self.__conn.getresponse()
		if not status in [None, resp.status]:
			raise Exception('invalid response status: ' + str(resp.status))
		head = resp.getheaders()
		body = resp.read()
		return (resp.status, head, body)

class Api(Request):
	__reItems = re.compile('items (\d+)-\d+/(\d+)')

	def __init__(self, host, port, cert):
		context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		context.verify_mode = ssl.CERT_NONE
		context.load_cert_chain(cert)
		Request.__init__(self, host, port, context)

	@staticmethod
	def __contentRange(head):
		for (k, v) in head:
			if 'content-range' == k.lower():
				m = Api.__reItems.match(v)
				if m != None:
					return (int(m.group(1)), int(m.group(2)))
		raise Exception('Content-Range header is missing')

	def all(self, url):
		start = 0
		total = 1
		pageSize = 100
		while start < total:
			(_, head, body) = self.request('GET', url, 200, headers = {'Range': 'items={0}-{1}'.format(start, start + pageSize - 1)})
			j = json.loads(body.decode('utf-8'))
			for i in j:
				yield i
			(start, total) = Api.__contentRange(head)
			start += len(j)

	def first(self, url, status = 200):
		j = self.get(url, status)
		return None if j == None or len(j) == 0 else j[0]

class Cloud(Request):
	def __init__(self, host, port):
		Request.__init__(self, host, port)

	def delete(self, url, token):
		return Request.delete(self, url, headers = {'Authorization': 'Token ' + token})

	def get(self, url, token):
		(status, _, body) = self.request('GET', url, None, headers = {'Authorization': 'Token ' + token})
		if status == 200:
			return body
		else:
			return None

	def head(self, url, token):
		return Request.head(self, url, None, {'Authorization': 'Token ' + token})

	def post(self, url, data, token, contentType = 'audio/x-wav'):
		return Request.request(self, 'POST', url, status = 201, headers = {'Authorization': 'Token ' + token, 'Content-type': contentType}, body = data)

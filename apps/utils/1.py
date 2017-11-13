from zeep import Client
from zeep.transports import Transport
import ast
transport = Transport(timeout=5000)
client = Client('http://localhost:7777/pro?wsdl', transport=transport)
with client.options(timeout=5000):
    response = client.service.getMethodAndCallGraph('/Users/yujie/workspace/projects/spring-framework-5.0.1.RELEASE')
    response = ast.literal_eval(response)
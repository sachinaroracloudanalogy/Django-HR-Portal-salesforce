"""
    SALESFORCE API MODULE
"""
import http.client
import requests
from simple_salesforce import Salesforce, SFType
from employee_attendance.utils.config import ConnectionString

class SFConnectAPI:
    """
        SALESFORCE API CLASS
    """
    sf = None
    sf_bulk = None

    def __init__(self, sf_config=ConnectionString):
        """
        :param sf_config:
        """
        print("connecting with salesforce.")
        self.sf = Salesforce(username=sf_config.USERNAME,
                             password=sf_config.PASSWORD,
                             security_token=sf_config.SF_AUTH_TOKEN)

        self.sf_config = sf_config
        print("connection success")


    def get_header(self, session_id):
        """
        :return:
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + session_id,
            'X-PrettyPrint': '1'
        }

    @staticmethod
    def get_connection(host):
        """
        :param host:
        :return:
        """
        conn = http.client.HTTPSConnection(host)
        return conn

    def get_login_connection(self):
        """
        :param host:
        :return:
        """
        from simple_salesforce import  SalesforceLogin
        session_id, instance = SalesforceLogin(
            username=self.sf_config.USERNAME,
            password=self.sf_config.PASSWORD,
            security_token=self.sf_config.SF_AUTH_TOKEN )
        return session_id

    def get_access_token(self, sf_conn=ConnectionString):
        """
        :param sf_conn:
        :return:
        """
        con_data ={"grant_type":'password',
                   "client_id": sf_conn.CLIENT_ID,  # Consumer Key
                   "client_secret":sf_conn.CLIENT_SECRET ,  # Consumer Secret
                   "username":sf_conn.USERNAME,
                   "password":sf_conn.PASSWORD+sf_conn.SF_AUTH_TOKEN}

        r = requests.post( "https://login.salesforce.com/services/oauth2/token", params=con_data )
        access_token = r.json().get( "access_token" )
        return access_token

    def execute_soql(self, query):
        """
        :param sf_conn:
        :param query:
        :param host:
        :return:
        """

        result = self.sf.query(query)
        return result

    def create_record(self, object_name='Employee__c', data=None):
        from simple_salesforce import SalesforceLogin
        session_id, instance = SalesforceLogin(
            username=self.sf_config.USERNAME,
            password=self.sf_config.PASSWORD,
            security_token=self.sf_config.SF_AUTH_TOKEN )
        from simple_salesforce import SFType
        try:
            sf_obj = SFType(object_name, session_id, self.sf_config.SF_URL)
            result = sf_obj.create(data)
        except Exception as ex:
            result = ex
            print(repr(ex))
        return result

    def update_record(self, record_id='a0N7F000003a962UAA', object_name='Employee__c', data=DATA):
        from simple_salesforce import SalesforceLogin
        session_id, instance = SalesforceLogin(
            username=self.sf_config.USERNAME,
            password=self.sf_config.PASSWORD,
            security_token=self.sf_config.SF_AUTH_TOKEN )
        from simple_salesforce import SFType
        try:
            sf_obj = SFType( object_name, session_id, self.sf_config.SF_URL )
            result = sf_obj.update(record_id, data)
        except Exception as ex:
            result = ex
            print(repr(ex))
        return result
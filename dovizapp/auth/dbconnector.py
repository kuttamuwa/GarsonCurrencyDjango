# -*- coding: utf8 -*-
# Author, Formatter : Umut Ucok, Universal

__author__ = 'Umut Ucok'
__supported__ = ('Oracle', 'Microsoft SQL Server', 'PostgreSQL')

import sys

import cx_Oracle
from sqlalchemy import create_engine


class DBConnector(object):
    def __init__(self, *args, **kwargs):
        """
        Let me explain base and target terms:
        Base database will be used to verify. It seems there is no different choosing base and target. However,
        you may face important case:
        Let's asssume that we had stored data in base db. I said had stored because after exporting target database,
        that data was removed. So if the data still populates in target database. We'll mark this as inserted.

        There is no way to understand that was a row removed in the past or inserted in target. We would have to
        create archiving trigger mechanism.

        """
        self.username, self.password, self.dbname, self.port, self.ip, self.dbbrand = args

        self.versioned = False
        self.sde_exist = False

        if self.dbbrand == 'ORACLE':
            # we need sid or tns name or service name
            try:
                self.sid = kwargs['sid']
                self.schema_name = kwargs['schema_name']
            except KeyError:
                raise ImportError('You did not specify sid but your database brand is Oracle. You need to write your '
                                  'tns or service name or service id on sid argument')

        try:
            self.version = kwargs['version']
            self.versioned = True

        except KeyError:
            print("You don't want ESRI, all right :)")
            self.versioned = False

        try:
            self.sde_engine = kwargs['sde_engine']
            self.sde_exist = True
        except KeyError:
            print("You dont have sde file. Okay.")
            self.sde_exist = False

        self.dbengine = None
        self.dbsession = None

        self.make_engine()
        # self.create_session()

    def create_pgengine(self):
        """

        :return: it fills dbengine with sql alchemy engine.
        """
        if self.port is None:
            self.port = 5432
        pgengine = create_engine(
            'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.username, self.password, self.ip, self.port,
                                                          self.dbname))
        try:
            pgengine.connect()
            self.dbengine = pgengine

        except:
            raise AssertionError(
                "PostgreSQL veritabani baglantisi yapilamadi ! Baglanti bilgilerini kontrol ediniz.")

    def create_oraclengine(self):
        """
        difference between others (mssqlserver, postgre) it reads service name instead of
        dbname.
        :return: sql alchemy database connection engine
        """

        try:
            oraengine = create_engine(
                'oracle://{}:{}@{}:{}/{}'.format(self.username, self.password, self.ip, self.port,
                                                 self.sid))
            oraengine.connect()
            self.dbengine = oraengine

        except:
            print("SID yerine TNS'den gitmeyi deneyecegiz.")
            oraengine = create_engine('oracle+cx_oracle://{}:{}@{}'.format(self.username, self.password, self.sid))

            try:
                oraengine.connect()
                self.dbengine = oraengine

            except:
                print("himm belki de tns'yi bizim olusturmamiz gerekiyor. Deneyelim.")
                try:
                    dsn_tns = cx_Oracle.makedsn(self.ip, self.port, self.sid)
                    con = cx_Oracle.connect(self.username, self.password, dsn_tns)
                    self.dbengine = con
                except Exception:
                    e = sys.exc_info()[1]
                    raise AssertionError(
                        "Maalesef Oracle Veritabanina baglanti yapilamadi. Lutfen baglanti bilgilerini"
                        " kontrol ediniz ve tekrar deneyiniz. Hata : \n"
                        "%s" % e)

    def create_msengine(self):
        """
        related with constructors
        :return: sql alchemy database connection engine
        """
        if self.port is None:
            self.port = 1433

        try:
            sqlengine = create_engine("mssql+pymssql://{}:{}@{}:{}/{}".format(self.username, self.password, self.ip,
                                                                              self.port, self.dbname))
            sqlengine.connect()
            print("SQL Server baglanti basarili")
            self.dbengine = sqlengine

        except:
            print("baglanti basarisiz oldu, baska bir yontemle deniyoruz..")
            sqlengine = create_engine("mssql+pyodbc://{}:{}@{}:{}/{}".format(self.username, self.password, self.ip,
                                                                             self.port, self.dbname))
            self.dbengine = sqlengine
            try:
                sqlengine.connect()
                print("SQL Server baglantisi basarili ")
                self.dbengine = sqlengine

            except Exception as e:
                raise AssertionError("SQL Server veritabanina baglanilamadi. Lutfen baglanti bilgilerini kontrol "
                                     "ediniz. \n Hata : %s" % e)

    def make_engine(self):
        if self.dbbrand.upper() == 'ORACLE':
            self.create_oraclengine()
        elif self.dbbrand.upper() == 'SQLSERVER':
            self.create_msengine()
        elif self.dbbrand.upper() == 'POSTGRESQL':
            self.create_pgengine()
        else:
            raise NotImplementedError(f"{self.dbbrand} veritabani desteklenmemektedir !")

    def run_sql(self, sql_sentence):
        if self.dbengine is None:
            self.make_engine()

        return self.dbengine.execute(sql_sentence)

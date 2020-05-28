"""
It will authenticate with on premise server via sql alchemy connecting database
and get a query result
"""
import warnings
from auth.dbconnector import DBConnector
from auth.config_reader import ConfiguresReader


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Auth(metaclass=Singleton):
    _auth_table_name = "auth"
    raise_error = None

    @classmethod
    def get_raise_error(cls):
        return cls.raise_error

    @classmethod
    def raise_error_on(cls):
        cls.raise_error = True

    @classmethod
    def raise_error_off(cls):
        cls.raise_error = False

    def __init__(self, dbconfig):
        self._dbconfigpath = dbconfig

        self._dbconfig = ConfiguresReader(dbconfig)
        self.dbinfo = self._get_dbinformation()
        self._dbconnector = DBConnector(self.dbinfo['username'], self.dbinfo['password'], self.dbinfo['dbname'],
                                        self.dbinfo['port'], self.dbinfo['ip'], self.dbinfo['dbbrand'])

    def get_phone_number_username(self, username):
        sql = f"SELECT phone_number FROM auth where username='{username}'"
        row = [i for i in self._dbconnector.run_sql(sql)]
        if row.__len__() == 0:
            raise _NoUserExistError(f"{username} kullanıcı isimli kayıdı kontrol ediniz !")
        else:
            return row[0]._row[0]

    def get_users(self):
        sql = f"SELECT username FROM auth"
        sql_result = self._dbconnector.run_sql(sql)

        return [i for i in sql_result]

    def get_users_and_passwords(self):
        sql = f"SELECT username, password FROM auth"
        sql_result = self._dbconnector.run_sql(sql)

        return [i for i in sql_result]

    def get_session_username(self, username):
        sql = f"SELECT logged_status FROM auth WHERE username='{username}'"
        sql_result = self._dbconnector.run_sql(sql)

        return bool([i for i in sql_result][0]._row[0])

    def set_session_on_username(self, username):
        sql = f"UPDATE auth SET logged_status=TRUE where username='{username}'"
        sql_result = self._dbconnector.run_sql(sql)

        return sql_result

    def set_session_off_username(self, username):
        sql = f"UPDATE auth SET logged_status=FALSE where username='{username}'"
        sql_result = self._dbconnector.run_sql(sql)

        return sql_result

    def _get_dbinformation(self):
        section = self._dbconfig.read_section('db')
        return section

    def get_moneyorder_information(self):
        section = self._dbconfig.read_section('moneyconfig')
        return section

    def verify_username_password(self, username, password):
        sql = f"SELECT * from auth where username='{username}' and password='{password}'"
        sql_result = self._dbconnector.run_sql(sql)
        if sql_result.rowcount == 1:
            return True
        elif sql_result.rowcount > 1:
            msg = "Aynı username ve password bilgileri birden fazla kayit icin var !"
            if self.get_raise_error():
                raise _WrongPasswordError(msg)
            warnings.warn(msg)

            return True
        else:
            raise _WrongPasswordError("Kullanici adi sifre dogrulamasinda bir seyler yanlis ! \n"
                                      "Lutfen sistem yoneticinize danisiniz",
                                      errors=sql_result)

    def check_username_exist(self, username):
        sql = f"SELECT COUNT(*) FROM auth where username='{username}'"
        sql_result = self._dbconnector.run_sql(sql)

        if sql_result.rowcount == 0:
            msg = f"{username} kullanıcısı bulunamadı"
            if self.get_raise_error():
                raise _NoUserExistError(msg)
            else:
                warnings.warn(msg)
                return True

    def verify_all(self, username, password, phone_number):
        """

        :param username: string
        :param password: string
        :param phone_number: string
        :return:
        """
        raise_error = self.get_raise_error()
        # username check
        self.check_username_exist(username)

        sql = f"SELECT * from auth where username='{username}' " \
            f"and password='{password}' and phone_number='{phone_number}'"
        sql_result = self._dbconnector.run_sql(sql)
        if sql_result.rowcount == 1:
            return True
        elif sql_result.rowcount > 1:
            msg = "Aynı username ve password bilgileri birden fazla kayit icin var !"
            if raise_error:
                raise _ManyUserExistError(msg)
            else:
                warnings.warn(msg)
                return True
        else:
            return False


# todo: All error types will be logged
class DumanError(Exception):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class _NoUserExistError(Exception):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class _ManyUserExistError(Exception):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class _WrongPasswordError(Exception):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class SystemAdministratorError(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

from faker import Faker
from random import randint

base_url = "https://" + "b2c.passport.rt.ru"


"""валидные данные"""
valid_name = 'Валентин'
valid_lastname = 'Емелин'
email = 'fewijep728@meidecn.com'
password = 'helLo6world5b'
login = 'Student'


"""невалидные данные"""
fake = Faker()
name = "Том"
lastname = 'Сойер'
fake_email = 'fewiep78@meidecn.com'
fake_password = 'helasdadorF5b'
email_without_domain = 'ewijep728@meidecn'
email_without_dog = 'fewijep728meidecn.com'
invalid_code = '123456'
invalid_phone1 = '+79999999999'
invalid_phone2 = randint(80000000000, 89999999999)





#Check number country &  carrier
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder

def num_check(phone_number):
	info = []
	number = phonenumbers.parse(phone_number)
	info.append(geocoder.description_for_number(number, "en"))
	info.append(carrier.name_for_number(number, "en"))
	return info
if __name__ == "__main__":
	number = input("Enter number:")
	print(num_check(number))

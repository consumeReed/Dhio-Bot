import re

whole = '56372~Shadow Bow of Celestial Might~Gelebron\'s legendary sceptre took this form after his defeat, to seek a new owner. Grants the skill Aetheric Surge which strikes your target for up to 6500 magic damage.~0~0~0~~~10~3000~11~0~0^200;5^215~11^500~5^215~4~0~0~15~~~0~0~0~7400~1~0~1^215~~~-1~0~~1~~~'

warrior_mord = '~0~0~12~~500~0~~25~0~~~5^180~1~0~0~~~~0~0~0~0~0~0~~7^300~125^6~0~0~~0~~125^0^200~'
general_mord = '~0~0~12~~500~0~~25~0~~~5^180~~0~0~~~~0~0~0~0~0~0~~14^300~4^6~0~0~~0~~4^0^-150~'
mord_spear = '~0~0~0~~25000~18~2850~19~0~0^190;6^200~~5^190~1,4,5~0~0~2~~~0~0~0~0~0~0~1^200~15^500~~0~0~~1~~~'
mord_grim = '~0~0~0~~15000~3~2950~23~0~2^20~~5^180~2,3~0~0~1~~~0~0~0~0~0~0~2^180;3^50~13^300~~0~0~~0~~~'
gele_axe = '~0~0~0~~~20~3000~2~0~1^190;4^180~10^400~5^210~1~0~0~1~~~0~0~0~7398~0~0~3^180~~~-1~0~~1~~~'

def extract_substring(input):
    pattern = r'(5\^[0-9]{3}~[0-9,]*~)'
    matches = re.search(pattern, input)
    classes = re.search('~(.*)~', matches.group(0))
    return classes.group(1)


print(extract_substring(whole))
print(extract_substring(warrior_mord))
print(extract_substring(general_mord))
print(extract_substring(mord_spear))
print(extract_substring(mord_grim))
print(extract_substring(gele_axe))

parsed = '1,2,3'
list = [int(i) for i in parsed.split(',')]
print(list)
# just for testing, running in PI folder
# supported languages: Portuguese and English
import TestBoxComms as TBox

slotRes, moreInfo = TBox.run('Portuguese')
print(slotRes)
print(slotRes['Slot 1'] == 'PASS')

#print(TextBoxComms.string_example)
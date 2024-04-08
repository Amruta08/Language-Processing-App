from googletrans import Translator
translator = Translator()
#data = translator.translate(text='यह हिंदी का एक वाक्य है', dest='en')
data = translator.translate(text='हे मराठीतील वाक्य आहे', dest='en')
print(data.text)

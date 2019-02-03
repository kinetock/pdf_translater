from tkinter import Tk, ttk, font
import pyperclip
import re
import requests


class Application(ttk.Frame):
	def __init__(self, root=None):
		super().__init__(root)
		self.pack()
		self.style = ttk.Style()
		self.style.configure(".",font=("游ゴシック",14))

		self.menu = ttk.LabelFrame(self, relief="ridge", text="menu")
		self.menu.pack(fill="x")

		self.trans_frame = ttk.LabelFrame(self, relief="ridge", text="translated text")
		self.trans_frame.pack(fill="x")
		self.translated_text = ttk.Label(self.trans_frame, relief="ridge", text=' '*120)
		self.translated_text.pack()

		self.clip_frame = ttk.LabelFrame(self, relief="ridge", text="clip text")
		self.clip_frame.pack(fill="x")
		self.clip_text = ttk.Label(self.clip_frame, relief="ridge", text=' '*120)
		self.clip_text.pack()

		self.trans = ttk.Button(self.menu, text="trans&copy", command=self._translate)
		self.trans.pack(side='left')
		self.reshape = ttk.Button(self.menu, text="reshape", command=self._reshape)
		self.reshape.pack(side='left')
		self.copy = ttk.Button(self.menu, text="copy(trans)", command=self._copy)
		self.copy.pack(side='left')
		self.clip_copy = ttk.Button(self.menu, text="copy(clip)", command=self._clip_copy)
		self.clip_copy.pack(side='left')
		self.exchange_trans = ttk.Button(self.menu, text="exchange", command=self._exchange_translate)
		self.exchange_trans.pack(side='left')

		self.url = 'https://script.google.com/macros/s/AKfycbxi1zPNMqxs3vtiBKloLnINiAyz6BHaHla3bC_LTVh5X6mirAPP/exec?'
		self.source = 'en'
		self.target = 'ja'

	def _translate(self):
		self.reshape_text()
		trans_form = '&source=' + self.source + '&target=' + self.target
		r = requests.get(self.url + 'text=' + self.clip_text['text'] + trans_form)
		self.translated_text['text'] = r.text
		pyperclip.copy(r.text + '\n' + self.clip_text['text'])

	def _reshape(self):
		self.reshape_text()
		self.translated_text['text'] = ''
		pyperclip.copy(self.clip_text['text'])

	def reshape_text(self):
		dic = {'\r\n': ' ', 'i.e.':'i.e', 'e.g.':'e.g', '&':'and', 'al.':'al', 'vs.':'vs', 'Sec. ':'Sec.', 'Eq. ':'Eq.', '- ':'', '. . . ':'__', '. ':'.\n', ': ':':\n', '; ':';\n'}
		self.clip_text['text'] = pyperclip.paste()
		for key, value in dic.items():
			self.clip_text['text'] = self.clip_text['text'].replace(key, value)

	def _copy(self):
		pyperclip.copy(self.translated_text['text'])

	def _clip_copy(self):
		pyperclip.copy(self.clip_text['text'])

	def _exchange_translate(self):
		tmp = self.source
		self.source = self.target
		self.target = tmp

if __name__ == "__main__":
	root = Tk()
	root.title("Clip Translater")
	root.geometry("640x480")
	app = Application(root)
	app.mainloop()

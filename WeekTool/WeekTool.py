# coding=utf-8
import sys
import string
import random
import getpass
import os
import urllib
import base64
from PySide import QtGui
from Crypto.Hash import MD5
from Crypto.Cipher import AES, DES3, DES, ARC4, ARC2, Blowfish, CAST, PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA
import UI
reload(sys)
sys.setdefaultencoding("utf-8")

reload(sys)
sys.setdefaultencoding("utf-8")

Ui_MainWindow = UI.Ui_MainWindow


class WeekTool(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # 初始化函数
        super(WeekTool, self).__init__()
        # 初始化UI界面
        Ui_MainWindow.__init__(self)
        # 将按钮与函数相连接
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Pwd_Creat)
        self.pushButton_2.clicked.connect(self.Pwd_Change)
        self.pushButton_3.clicked.connect(self.TransCoding)
        self.pushButton_4.clicked.connect(self.URL_decode)
        self.pushButton_5.clicked.connect(self.Hex_decode)
        self.pushButton_6.clicked.connect(self.Ascii_decode)
        self.pushButton_7.clicked.connect(self.b64_decode)
        self.pushButton_8.clicked.connect(self.readfile_1)
        self.pushButton_9.clicked.connect(self.readfile_2)
        self.pushButton_10.clicked.connect(self.readfile_3)
        self.pushButton_11.clicked.connect(self.readfile_4)
        self.pushButton_12.clicked.connect(self.readfile_5)
        self.pushButton_13.clicked.connect(self.readfile_6)
        self.pushButton_14.clicked.connect(self.DCfile_encrypt)
        self.pushButton_15.clicked.connect(self.DCfile_decrypt)
        self.pushButton_16.clicked.connect(self.FDCfile_encrypt)
        self.pushButton_17.clicked.connect(self.FDCfile_decrypt)
        # 获取当前用户名
        user_name = getpass.getuser()
        # 打开界面时的数据载入
        global key_path
        key_path = 'C:/Users/'+user_name+'/.AES_1'
        if os.path.exists(key_path):
            f = open(key_path, 'rb')
            key = f.read()
            f.close()
            f_ = open('background.jpg', 'ab+')
            data = f_.read()
            f_.close()
            if data != '':
                data = self.AES_decrypt(data, key)
            else:
                pass
            self.textEdit.setText(data.decode('utf-8'))
        else:
            h = MD5.new()
            h.update(Random.new().read(16))
            key = h.hexdigest()
            f = open(key_path, 'wb')
            f.write(key)
            f.close()

    def Pwd_Creat(self):
        # 随机密码创建函数
        a = string.ascii_uppercase if self.checkBox.isChecked() else ''
        b = string.ascii_lowercase if self.checkBox_2.isChecked() else ''
        c = string.digits if self.checkBox_3.isChecked() else ''
        d = self.lineEdit_2.text() if self.checkBox_4.isChecked() else ''
        chars = list(a+b+c+d)
        length = int(self.comboBox.currentText())
        Pwd = ''.join(random.sample(chars, length))
        self.textEdit_2.setText(Pwd)
        sign = self.lineEdit.text()
        data = self.textEdit.toPlainText()
        if data == '':
            data = data+sign+': '+Pwd
        else:
            data = data+'\n'+sign+': '+Pwd
        self.textEdit.setText(data.decode('utf-8'))
        f = open(key_path, 'rb')
        key = f.read()
        iv = Random.new().read(AES.block_size)
        data = self.AES_encrypt(data, key, iv)
        f = open('background.jpg', 'wb')
        f.write(data)
        f.close()

    def Pwd_Change(self):
        # 在文本框中更改密码的函数
        f = open(key_path, 'rb')
        key = f.read()
        f.close()
        iv = Random.new().read(AES.block_size)
        data = self.textEdit.toPlainText()
        data = self.AES_encrypt(data, key, iv)
        f = open('background.jpg', 'wb')
        f.write(data)
        f.close()

    def TransCoding(self):
        # 正向编码转换函数
        Tdata = self.textEdit_3.toPlainText().encode('utf-8')
        Tlength = len(Tdata)
        Udata = ''
        Hdata = ''
        Adata = ''
        for i in range(0, Tlength):
            Ascii = ord(Tdata[i])
            Hex = hex(Ascii)[2:]
            URL = '%'+Hex
            if 33 <= Ascii & Ascii <= 127:
                Adata = Adata+' '+str(Ascii)
                Hdata = Hdata+Hex
            Udata = Udata+URL
        h = MD5.new()
        h.update(Tdata)
        self.textEdit_4.setText(Udata)
        self.textEdit_5.setText('0x'+Hdata)
        self.textEdit_6.setText(Adata)
        self.textEdit_7.setText(base64.b64encode(Tdata))
        self.lineEdit_3.setText(h.hexdigest()[8:-8])
        self.lineEdit_4.setText(h.hexdigest())

    def URL_decode(self):
        # URL解码函数
        urlcode = self.textEdit_4.toPlainText()
        Plaincode = urllib.unquote(str(urlcode)).decode('utf-8')
        self.textEdit_3.setText((Plaincode).decode('utf-8'))

    def Hex_decode(self):
        # 16进制解码函数
        hexcode = self.textEdit_5.toPlainText()
        hexcode = hexcode[2:] if hexcode[0:2] == '0x' else hexcode
        Plaincode = hexcode.decode('hex')
        self.textEdit_3.setText(Plaincode)

    def Ascii_decode(self):
        # ASCII编码解码函数
        try:
            asciicode = int(self.textEdit_6.toPlainText().replace(' ', ''))
            if 33 <= asciicode & asciicode <= 127:
                Plaincode = chr(asciicode)
                self.textEdit_3.setText(Plaincode)
            else:
                error
        except:
            self.textEdit_3.setText(u'请确认你输入了单个可打印ASCII字符')

    def b64_decode(self):
        # base64解码函数
        b64code = self.textEdit_7.toPlainText()
        Plaincode = base64.b64decode(b64code)
        self.textEdit_3.setText(Plaincode)

    def AES_encrypt(self, data, key, iv):
        # AES加密函数
        encrypt = AES.new(key, AES.MODE_CFB, iv)
        data = encrypt.encrypt(data)
        return iv+data

    def AES_decrypt(self, data, key):
        # AES解密函数
        iv = data[0:16]
        decrypt = AES.new(key, AES.MODE_CFB, iv)
        data = decrypt.decrypt(data[16:])
        return data

    def DES3_encrypt(self, data, key, iv):
        # DES3加密函数
        encrypt = DES3.new(key, DES3.MODE_CFB, iv)
        data = encrypt.encrypt(data)
        return iv+data

    def DES3_decrypt(self, data, key):
        # DES3解密函数
        iv = data[0:8]
        decrypt = DES3.new(key, DES3.MODE_CFB, iv)
        data = decrypt.decrypt(data[8:])
        return data

    def Blowfish_encrypt(self, data, key, iv):
        # Blowfish加密函数
        encrypt = Blowfish.new(key, Blowfish.MODE_CFB, iv)
        data = iv+encrypt.encrypt(data)
        return data

    def Blowfish_decrypt(self, data, key):
        # Blowfish解密函数
        iv = data[0:8]
        decrypt = Blowfish.new(key, Blowfish.MODE_CFB, iv)
        data = decrypt.decrypt(data[8:])
        return data

    def CAST_encrypt(self, data, key, iv):
        # CAST加密函数
        encrypt = CAST.new(key, CAST.MODE_CFB, iv)
        data = encrypt.encrypt(data)
        return iv+data

    def CAST_decrypt(self, data, key):
        # CAST解密函数
        iv = data[0:8]
        decrypt = CAST.new(key, CAST.MODE_CFB, iv)
        data = decrypt.decrypt(data[8:])
        return data

    def DES_encrypt(self, data, key, iv):
        # DES加密函数
        encrypt = DES.new(key, DES.MODE_CFB, iv)
        data = encrypt.encrypt(data)
        return iv+data

    def DES_decrypt(self, data, key):
        # DES解密函数
        iv = data[0:8]
        decrypt = DES.new(key, DES.MODE_CFB, iv)
        data = decrypt.decrypt(data[8:])
        return data

    def RC4_encrypt(self, data, key):
        # RC4加密函数
        encrypt = ARC4.new(key)
        data = encrypt.encrypt(data)
        return data

    def RC4_decrypt(self, data, key):
        # RC4解密函数
        decrypt = ARC4.new(key)
        data = decrypt.decrypt(data)
        return data

    def RC2_encrypt(self, data, key, iv):
        # RC2加密函数
        encrypt = ARC2.new(key, ARC2.MODE_CFB, iv)
        data = encrypt.encrypt(data)
        return iv+data

    def RC2_decrypt(self, data, key):
        # RC2解密函数
        iv = data[0:8]
        decrypt = ARC2.new(key, ARC2.MODE_CFB, iv)
        data = decrypt.decrypt(data[8:])
        return data

    def RSA_encrypt(self, data, public_key):
        # RSA加密函数
        key = RSA.importKey(public_key)
        encrypt = PKCS1_v1_5.new(key)
        res = []
        for i in range(0, len(data), 200):
            res.append(encrypt.encrypt(data[i:i+200]))
        data = ''.join(res)
        return data

    def RSA_decrypt(self, data, private_key):
        # RSA解密函数
        sentinel = Random.new().read(16)
        key = RSA.importKey(private_key)
        decrypt = PKCS1_v1_5.new(key)
        res = []
        for i in range(0, len(data), 256):
            res.append(decrypt.decrypt(data[i:i+256], sentinel))
        data = "".join(res)
        return data
# 以下6个为打开文件选择框并输出相应目录到对于文本框的函数
    def readfile_1(self):
        file_name, ok = QtGui.QFileDialog.getOpenFileName(
            self, u'选择待加密文件', './')
        if ok:
            self.lineEdit_5.setText(file_name.decode('utf-8'))

    def readfile_2(self):
        file_name, ok = QtGui.QFileDialog.getOpenFileName(
            self, u'选择待解密文件', './')
        if ok:
            self.lineEdit_6.setText(file_name.decode('utf-8'))

    def readfile_3(self):
        file_name, ok = QtGui.QFileDialog.getOpenFileName(
            self, u'选择密钥文件', './')
        if ok:
            self.lineEdit_7.setText(file_name.decode('utf-8'))

    def readfile_4(self):
        file_name, ok = QtGui.QFileDialog.getOpenFileName(
            self, u'选择待加密文件', './')
        if ok:
            self.lineEdit_8.setText(file_name.decode('utf-8'))

    def readfile_5(self):
        file_name, ok = QtGui.QFileDialog.getOpenFileName(
            self, u'选择待解密文件', './')
        if ok:
            self.lineEdit_9.setText(file_name.decode('utf-8'))

    def readfile_6(self):
        file_name, ok = QtGui.QFileDialog.getOpenFileName(
            self, u'选择私钥文件', './')
        if ok:
            self.lineEdit_10.setText(file_name.decode('utf-8'))

    def DCfile_encrypt(self):
        # 对称加密总函数
        encrypt_type = self.comboBox_2.currentText()
        file_name = self.lineEdit_5.text()

        if encrypt_type == 'AES':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            h = MD5.new()
            h.update(Random.new().read(16))
            iv = Random.new().read(AES.block_size)
            key = h.hexdigest()
            data = self.AES_encrypt(data, key, iv)
        elif encrypt_type == 'DES3':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            h = MD5.new()
            iv = Random.new().read(DES3.block_size)
            h.update(Random.new().read(16))
            key = h.hexdigest()[8:-8]
            data = self.DES3_encrypt(data, key, iv)
        elif encrypt_type == 'Blowfish':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            h = MD5.new()
            iv = Random.new().read(Blowfish.block_size)
            h.update(Random.new().read(16))
            key = h.hexdigest()
            data = self.Blowfish_encrypt(data, key, iv)
        elif encrypt_type == 'CAST':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            h = MD5.new()
            iv = Random.new().read(CAST.block_size)
            h.update(Random.new().read(16))
            key = h.hexdigest()[8:-8]
            data = self.CAST_encrypt(data, key, iv)
        elif encrypt_type == 'DES':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            h = MD5.new()
            iv = Random.new().read(DES.block_size)
            h.update(Random.new().read(16))
            key = h.hexdigest()[0:8]
            data = self.DES_encrypt(data, key, iv)
        elif encrypt_type == 'RC4':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            iv = Random.new().read(ARC4.block_size)
            key = base64.b64encode(Random.new().read(190))
            data = self.RC4_encrypt(data, key)
        elif encrypt_type == 'RC2':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            iv = Random.new().read(ARC2.block_size)
            key = len(base64.b64encode(Random.new().read(94)))
            data = self.RC2_encrypt(data, key, iv)

        f_name, ok = QtGui.QFileDialog.getSaveFileName(self, u'选择输出文件', './')
        if ok:
            f = open(f_name, 'wb')
            f.write(data)
            f.close()
            f = open(f_name+'_key', 'wb')
            f.write(key)
            f.close()
            QtGui.QMessageBox.information(self, u"提示", self.tr("Finished!"))

    def DCfile_decrypt(self):
        # 对称解密总函数
        decrypt_type = self.comboBox_3.currentText()
        file_name = self.lineEdit_6.text()
        if self.comboBox_6.currentText() == '密钥文件':
            key_file = self.lineEdit_7.text()
            f = open(key_file, 'rb')
            key = f.read()
            f.close()
        else:
            key = self.textEdit_8.text()
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
        if decrypt_type == 'AES':
            data = self.AES_decrypt(data, key)
        elif decrypt_type == 'DES3':
            data = self.DES3_decrypt(data, key)
        elif decrypt_type == 'Blowfish':
            data = self.Blowfish_decrypt(data, key)
        elif decrypt_type == 'CAST':
            data = self.CAST_decrypt(data, key)
        elif decrypt_type == 'DES':
            data = self.DES_decrypt(data, key)
        elif decrypt_type == 'RC4':
            data = self.RC4_decrypt(data, key)
        elif decrypt_type == 'RC2':
            data = self.RC2_decrypt(data, key)
        f_name, ok = QtGui.QFileDialog.getSaveFileName(self, u'选择输出文件', './')
        if ok:
            f = open(f_name, 'wb')
            f.write(data)
            f.close()
            QtGui.QMessageBox.information(self, u"提示", self.tr("Finished!"))

    def FDCfile_encrypt(self):
        # 非对称加密总函数
        encrypt_type = self.comboBox_4.currentText()
        file_name = self.lineEdit_8.text()
        if encrypt_type == 'RSA':
            f = open(file_name, 'rb')
            data = f.read()
            f.close()
            rsa = RSA.generate(2048)
            key = rsa.publickey().exportKey('PEM')
            data = self.RSA_encrypt(data, key)
        key = rsa.exportKey('PEM')
        f_name, ok = QtGui.QFileDialog.getSaveFileName(self, u'选择输出文件', './')
        if ok:
            f = open(f_name, 'wb')
            f.write(data)
            f.close()
            f = open(f_name+'_key', 'wb')
            f.write(key)
            f.close()
            QtGui.QMessageBox.information(self, u"提示", self.tr("Finished!"))

    def FDCfile_decrypt(self):
        # 非对称解密总函数
        decrypt_type = self.comboBox_5.currentText()
        file_name = self.lineEdit_9.text()
        key_file = self.lineEdit_10.text()
        f = open(key_file, 'rb')
        key = f.read()
        f.close()
        f = open(file_name, 'rb')
        data = f.read()
        if decrypt_type == 'RSA':
            data = self.RSA_decrypt(data, key)
        f_name, ok = QtGui.QFileDialog.getSaveFileName(self, u'选择输出文件', './')
        if ok:
            f = open(f_name, 'wb')
            f.write(data)
            f.close()
            QtGui.QMessageBox.information(self, u"提示", self.tr("Finished!"))


def main():
    # 主函数
    app = QtGui.QApplication(sys.argv)
    ex = WeekTool()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Python风格，当直接运行时才执行主函数
    main()

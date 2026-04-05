# password-manager
python写的本地密码记录本，其文件打包出来后的样子
<img width="889" height="639" alt="屏幕截图 2026-04-05 164211" src="https://github.com/user-attachments/assets/d0c083f9-8176-452e-b7b8-32af9d4591f5" />
添加保存以后就会在改文件夹里生成

passwords.json（作用：密码箱）

secret.key（作用：钥匙）

不能随便删除，删了数据就没了

成功以后打开软件就会以上面的方式呈现。

我个人觉得是很直观的，当然你也可以拿着这些代码随便改，反正都有注释的

要改用源码的话，需要你自己配置环境

1、python 3.11

2、安装第三方库
pip install cryptography
（我个人是喜欢pycharm或者vs code的这两个IDE的，当然你要用文本文档也行，反正代码也不多，就是格式容易错）安装第三方库时有可能网络超时，就自己配镜像源吧

3、如果改好了可以打包了，个人推荐pyinstaller

（1）安装库pip install pyinstaller
          pip install cryptography（记得要把这个环境一起打包进去，不然运行不了）

（2）打包pyinstaller -F -w --hidden-import=cryptography 文件名字.py

之后就生成一些文件里面就有exe文件，就可以直接拿来用了

希望对你有帮助。

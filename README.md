#keyboard_recording_trojan
[![EOL](https://img.shields.io/badge/Status-EOF-lightgrey.svg?style=flat-square)]()  
A keyboard recording trojan  
## Warning
DO NOT USE THIS CODE TO DO ANYTHING ILLEGAL !!!  
## Environment

    OS:Windows  
    Python edition:Python2.x  
    Packages:pyHook/email/pywin32  

## Illustration
1、本压缩包中含有经过伪装的360安全卫士图标文件“ABE.glj”，  
2、若要打包进行测试则可将程序名改为“开始游戏”或更改源码中相应的位置，否则无法完成将自身复制到C盘。
## Introduction
它可以根据要记录密码的关键词（如“QQ”）匹配当前活动窗口，若含有关键词则记录用户在此窗口内的所有输入，当用户输入回车或点击鼠标左键时进行屏幕截图，并将所记录的输入信息和截图发送到指定邮箱。  
![1](http://img.blog.csdn.net/20150309214837529)  
可我又怎么会那么容易满足呢？让我们来把它做得更像木马一些吧！ 首先，它不能长得就像个木马，我们来把它伪装成一个游戏的开始程序。  
![2](http://img.blog.csdn.net/20150309214847716)  
其次，在这个游戏文件夹中很没有安全感，很容易就会被用户删掉！我们在运行时自动将本体复制至C盘指定文件夹中，并且将其设置为隐藏文件!  
![3](http://img.blog.csdn.net/20150309214857544)  
我这么拼命保护它就是因为我要让它开机自动运行！修改注册表是一种办法，还有一种更简单的办法是在启动文件夹创建一个快捷方式。  
![4](http://img.blog.csdn.net/20150309214905469)  
不要以为就这样就完了！这时用户一定会察觉：疑，我昨天下的游戏怎么会开机启动？于是打开了360。。。我们何不自带伪装，把自己伪装成360，这样用户就会以为那个开机自动启动的程序是360！于是就有了这个经过伪装的图标文件！  
![5](http://img.blog.csdn.net/20150309214802212)  

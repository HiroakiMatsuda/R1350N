R1350N
======================
MicroInfinity社製 1軸ジャイロモジュール[R1350N][gyro]をラップしたRTCです．
[gyro]:http://www.switch-science.com/catalog/1016/

動作環境
------
**OS:**  
Windows 7 32bit/64bit  
Windows 8 32bit/64bit  
Ubuntu12.04 LTS 32bit  

**RT-Middleware:**  
[OpenRTM-aist Python 1.1.0-RC1][py]  
[py]:http://openrtm.org/openrtm/ja/node/4526

ファイル構成
------

ファイル構成について，一部抜粋で説明します．  

R1350N  
│―IMUR1350N  
│  　　　│―cmake    
│  　　　│―cmake_modules    
│  　　　│―cpack_resources    
│  　　　│―doc    
│  　　　│―idl    
│  　　　│―include    
│  　　　│―src    
│  　　　│―.project    
│  　　　│―CMakeLists.txt    
│  　　　│―COPYING    
│  　　　│―COPYING.LESSER    
│  　　　│―imu.py      
│  　　　│―imu.pyc    
│  　　　│―IMUR1350N.conf    
│  　　　│―IMUR1350N.py    
│  　　　│―README.IMUR1350N    
│  　　　│―rtc.conf   
│  　　　│―RTC.xml    
│    
│―README.md    
│―TestRTC    
　　　　　│―PyAcceleration3dConsoleOut  
　　　　　│―PyDoubleSeqConsoleOut  
  
* imu.py  
R1350Nと通信を行うPythonモジュールです．  
R1350N RTCはこのモジュールを通してセンサデータを取得します．  
また詳しくは後述しますが，ジャイロモジュールはUSBシリアル変換器に接続されていることを前提にして通信を行います．  

* IMUR1350N.py  
R1350NのラッパRTCです．  

* TestRTC   
本RTCの動作確認をするためのTest用RTCが収められています．


ジャイロセンサの構成
------  
システムの構成を説明します．  

<img src="http://farm8.staticflickr.com/7386/11304194664_147ff3450e_o.png" width="600px" />  

* R1350N    
MicroInfinity社製 1軸ジャイロモジュール[R1350N][gyro]です．  

* USB to Serial Converter  
R1350NはUART通信を行うので，USBシリアル変換器を用いてPCと接続します．    

* IMUR1350N  
imu.pyを通してR1350Nから取得したセンサ値を出力します．  



ジャイロセンサの実装例
------  
システム構成に適合する実装例を示します．  

<img src="http://farm3.staticflickr.com/2856/11302640864_525f7e6157_o.png" width="400px" /> 

* 使用するデバイス    
[1軸ジャイロモジュールR1350N][gyro]  
[R1350N用 ピッチ変換基板][board]  
[FTDI USBシリアル変換アダプター(5V/3.3V切り替え機能付き)][converter]  

[converter]:http://www.switch-science.com/catalog/1032/
[board]:http://www.switch-science.com/catalog/1065/

①のシリアル変換器を，②のピッチ変換基板上に実装したR1350Nに接続しています．  
最後にケーシングすればコンパクトなセンサモジュールとして使用することができます．  

RTCの構成
------  
<img src="http://farm4.staticflickr.com/3828/11304643206_0d07dc8951_o.png" width="400px" />    
データポートは以下のようになっています  

* acceleration port :OutPort  
データ型; Acceleration3D  
 ・double ax: R1350Nが取得したX軸加速データを出力します．  
 ・double ay: R1350Nが取得したY軸加速データを出力します．  
 ・double az: R1350Nが取得したZ軸加速データを出力します．  

* angle port :OutPort  
データ型; TimedDoubleSeq  
 ・double data[0]: センサ値のインデックス(0-255)です．  
 ・double data[1]: 角度データ [deg]です．  
 ・double data[2]: 角度データ [radian]です．  
 ・double data[3]: 角速度 [deg / sec]です．  

センサの座標系はモジュール表面を基準に以下のようになっています．  

<img src="http://farm4.staticflickr.com/3735/11304655513_c9e389554a_o.png" width="300px" />    
  
使い方
------

###1. ネームサーバーの起動###
ネームサーバーを起動します．  

Windows:  
Start Naming Serviceで起動します．  
Linux:  
以下のコマンドで起動します．2809はポート番号で任意で選んで構いません．  
$ rtm-naming 2809

###2. RTCの起動###
1. IMUR1350Nを起動し，シリアルデバイスを設定します．  
・IMUR1350Nを起動します．  
Windows:  
IMUR1350N.pyをダブルクリックで起動します．    
Linux:  
以下のコマンドで起動します．  
$ python IMUR1350N.py  
・次に，デバイス名を確認します．  
Windows:  
デバイスマネージャーのポートからCOM番号を確認します．  
Linux:   
以下のメッセージでデバイス名を確認します．  
$ dmesg  
・最後に，IMUR1350Nを選択しコンフィギュレーションのdeviceにデバイスを設定します．  
Windows:   
例： COM1   
Linux:   
例： /dev/ttyUSB0  
<img src="http://farm8.staticflickr.com/7436/11304892913_97c23ea94c_o.png" width="500px" />    

2. PyAcceleration3dConsoleOut.pyを起動します．  
Windows:  
PyAcceleration3dConsoleOut.pyをダブルクリックで起動します．  
Linux:  
以下のコマンドで起動します．  
$ python PyAcceleration3dConsoleOut.py  

3. PyDoubleSeqConsoleOut.pyを起動します．  
Windows:  
PyDoubleSeqConsoleOut.pyをダブルクリックで起動します．  
Linux:  
以下のコマンドで起動します．  
$ python PyDoubleSeqConsoleOut.py  

4. RTCの接続
RT System Editorを使用して，RobotServiceとPyStringConsoleOutを接続します．  
<img src="http://farm4.staticflickr.com/3823/11304871594_4578ee826a_o.png" width="500px" />    


###3. センサ値の確認###
全てのRTCをActivateし，センサ値がコンソールに表示されることを確認してください．  

IMUR1350Nの実行画面  
<img src="http://farm6.staticflickr.com/5535/11304872846_55f40b8f04_o.png" width="400px" />    

PyAcceleration3dConsoleOutの実行画面  
<img src="http://farm4.staticflickr.com/3810/11304896194_6a8103ee6c_o.png" width="400px" />    


PyAcceleration3dConsoleOutの実行画面  
<img src="http://farm4.staticflickr.com/3732/11304938223_8a405bac18_o.png" width="400px" />    

以上が本RTCの使い方となります.  

LICENSE
----------
Copyright © 2013 Hiroaki Matsuda
Licensed under the [Apache License, Version 2.0][Apache].  
Distributed under the [MIT License][MIT].  
Dual licensed under the [MIT License][MIT] and [Apache License, Version 2.0][Apache].   
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
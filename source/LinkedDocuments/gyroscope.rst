陀螺儀
=========

.. image:: https://store.ctr-electronics.com/cdn/shop/files/Pigeon-2.0-9-Degrees-of-Freedom-IMU_robotics_FRC_orientation_data.png?v=1756397345&width=1946
    :width: 80%
    :align: center

這是可愛的陀螺儀

-----

.. note::
    通常看到陀螺儀後面會多一個IMU，中文叫做慣性測量單元(Inertial Measurement Unit)，詳細內容可以看這邊

    .. website:: https://www.analog.com/cn/lp/002/tech-articles-taiwan/enhancing-robotic-localization.html
        :title: 運用IMU提升機器人定位性能: 精準導航的基礎技術

在FRC中，機器人要取得自己目前的朝向，除了通靈跟用馬達的位置推算以外，最常見跟可信任的方式就是從陀螺儀抓資料過來。常用的陀螺儀有這三種

 -  Kaukai lab的 NavX
 -  CTRE的 Pigeon 2.0
 -  類比式的ADIS16448跟ADIS 16470(這兩個如果在賽場上見到的話基本上可以去抽彩卷了(誤))

也因爲前面兩個比較常見，所以我就著重在這邊。

陀螺儀讀出來的數據要進到整個資料系統裡面有下面幾種方式

- 用RIO右上角的SPI孔
- 用RIO中間的MXP孔
- 直接走CAN迴路

類比式的IMU常見使用的是 `SPI接口 <https://makerpro.cc/2016/07/learning-interfaces-about-uart-i2c-spi/>`_ ，NavX是用MXP的那一條，然後再從軟體上選要用哪種資料形式。
Pigeon 2則是把所有讀到的資料都丟到CAN迴路

.. note::w
    CTRE他們家不像REV自己的資料有自己的接頭，把全部的資料都丟到CAN迴路上，這樣做的好處雖然整體的接口變簡單了(只有兩組CAN H跟L)，不過這樣就很依賴CAN迴路的資源，2025-26賽季還是用RoboRIO 2.0的控制方式，他在上面提供的CAN 2.0迴路吃不消全CTRE的底盤全開的資料量(當然所以他們有針對這件事情做一點取捨)，針對這個東西CTRE他們有出支援CAN-FD的 `CANivore <https://store.ctr-electronics.com/products/canivore>`_ 。這在26年賽季可能還有優勢，不過在27年的 `SystemCore <https://docs.wpilib.org/en/2027/docs/software/systemcore-info/systemcore-introduction.html>`_ 就會原生支援CAN FD，所以可能再等一下下就不用花1.5個kraken的錢買這個東西。

拿資料的方式
+++++++++++++

陀螺儀根據製造廠家不一樣會有不一樣的函式庫(幹話)，不過最常用的函數是 :code:`getRotation2d()` ，通常回傳值是他的朝向(yaw)，會被喂到位置預估器(Pose Estimator)或是抓出來給人看。

.. code-block:: java

    AHRS gyro = new AHRS(NavXComType.kMXP_SPI);
    Pigeon2 gyro = new Pigeon2(0);

    Rotation2d getyaw = gyro.getRotation2d()

關於陀螺儀的都市傳說
--------------------

陀螺儀的安裝位置一直是一個都市傳說很大的點之一，通常會裝在底盤的正中間然後面對前面。在安裝位置方面，假設底盤在原地旋轉的時候，幾乎所有的物理量都會一樣。方向也是一樣，因為是讀取相對角度的關係，所以只要是Z軸跟底盤平行就可以了(如果不是的話要透過一波計算拿到x-y平面的yaw值)
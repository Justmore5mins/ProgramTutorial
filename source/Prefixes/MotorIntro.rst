馬達與控制器簡介
==================

FRC常用的馬達有分 ``有刷`` 跟 ``無刷`` 兩種，在世界賽中以無刷馬達為主要，有刷馬達主要因為便宜所以蠻常被Rookie隊伍採用。不過因為有刷馬達有物理接觸，所以很容易產生耗損與廢熱，也有人的有刷馬達冒煙過，又因為有刷馬達的表現不穩定，所以傳統強隊才會選擇無刷馬達最為主要使用馬達。

有刷馬達
------------


常見的有刷馬達有CIM, Mini CIM, 775pro 等。

.. image::  https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBpu0e4oquV8tfayfzWOcDnF4Bw5_DxPfq2A&s
    :alt: CIM Motor
    :width: 60%
    :align: center

上面這個小東西是CIM馬達。

因為他供電的方式只有正負極，而且也沒有內建編碼器(encoder)，所以馬達控制器的支援度也是最廣的
可以用的控制器

- REV SparkMax
- CTRE TalonSRX
- VEX VictorSPX

.. note:: 這三個只有VictorSPX沒有支援Encoder的輸入

有沒有編碼器這一點會影響到能不能用更進階的控制(例如PID(閉環控制))方式，有些特別簡單的功能(比如說shooter)其實有沒有encoder不影響。

.. TODO: 要加超連結

如果用一些比較複雜的控制方式(比如說PID，不知道是什麼的請看這邊)，由於這些方式大部分都需要知道馬達的位置跟速度等等資料，而且沒有馬達的讀值的話只有通靈才知道轉到對的位置。

如果用

- SparkMax 一定愛配 `REV Through Bore Encoder <https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.revrobotics.com/rev-11-1271/&ved=2ahUKEwj5oPzZxP-QAxW5bPUHHbLOE5AQFnoECAwQAQ&usg=AOvVaw0suByilwfUfMYEvVJmyoOe>`_
- TalonSRX 一定愛配 `CIM Encoder <https://andymark.com/products/cimcoder-256-hi-resolution-cim-encoder>`_

無刷馬達
----------

無刷馬達通常就有內建控制器了，所以在空間編排跟設計難易度都會比有刷要考慮的東西少一點。不過在這邊馬達的關係就有億點點複雜了

REV
+++

- NEO v1.1 (`REV 21-1650 <https://www.revrobotics.com/rev-21-1650/>`_)
  
    - 優點：爆幹便宜
    - 缺點：扭力跟轉速是最普通的
    - 為什麼要買：因為真的爆幹便宜
    - 為什麼不要買：因為有出二代了
    - 控制器: ``SparkMax`` 或 ``TalonFXS``

- NEO 550 (`REV 21-1651 <https://www.revrobotics.com/rev-21-1651/>`_)
  
    - 優點：轉速爆幹快(11000RPM)
    - 缺點：扭力爆幹小
    - 為什麼要買：轉速快而且體積小
    - 為什麼不買：因為通常會使用的配置會讓他的佔地面積變大很多
    - 控制器: ``SparkMax`` 或 ``TalonFXS``

- NEO Vortex(`REV 21-1652 <https://www.revrobotics.com/rev-21-1652/>`_)

    - 優點：轉速跟扭力是REV家最快的
    - 缺點：爆幹貴
    - 為什麼要買：因為他是REV最好的馬達
    - 為什麼不買：含控制器多20美就可以用Kraken，不上Kraken不香嗎？
    - 控制器: ``SparkFlex`` 或用 `Flex Dock <https://www.revrobotics.com/rev-11-2828/>`_ 配 ``SparkMax``

- NEO 2.0(`REV 21-1653 <https://www.revrobotics.com/rev-21-1653/>`_)

    - 優點：體積比NEO v1.1小，扭力大一點，然後有換SplineXS的連接方式
    - 缺點：轉速還是一樣
    - 為什麼要買：可以無縫換Kraken系列的馬達
    - 為什麼不買：扭力雖然不小但是相對來說還是不大
    - 控制器: ``SparkMax`` 或是 ``TalonFXS``
  
WCP/VEX + CTRE
++++++++++++++

- Kraken X60 (`WCP-0940 <https://wcproducts.com/products/wcp-0940>`_)

    - 優點：FRC最強的馬達
    - 缺點：爆幹貴
    - 為什麼要買：扭力大，轉速快
    - 為什麼不買：真的有點貴
    - 控制器：內建 ``TalonFX``

- Kraken X44(`WCP-0941 <https://wcproducts.com/products/wcp-0941>`_)

    - 優點：比Kraken X60小一圈，扭力比較小但是轉速更快一點
    - 缺點：跟X60一樣貴
    - 為什麼要買：在寬度比較受限的地方可以放
    - 為什麼不買：跟X60一樣的價格真的有億點點貴
    - 控制器：內建 ``TalonFX``

- Minion(`WCP-1691 <https://wcproducts.com/products/wcp-1691>`_)
  
    - 優點：NEO 550的體積但是扭力跟轉速都可以對幹v2.0
    - 缺點：比 NEO 1.1貴一些(80塊)
    - 為什麼要買：優點還不香嗎
    - 為什麼不買：如果要配官方的控制器的話都可以買一顆Kraken了
    - 控制器： ``SparkMax`` 或是 ``TalonFXS``

馬達控制器們
------------

SparkMax (`REV 11-2158 <https://www.revrobotics.com/rev-11-2158/>`_)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

SparkMax 是REV推出的馬達控制器，主要功能就是控制無刷馬達(廢話)。也有支援硬體的PID控制

軟體要裝的包：

.. website:: https://software-metadata.revrobotics.com/REVLib-2025.json

用法

.. code-block:: java

    SparkMax motor = new SparkMax(MotorID, MotorType.kBrushless);
    SparkMaxConfg config = new SparkMaxConfig(); //馬達的設定

    //設定設定
    config
        .idleMode(IdleMode.kBrake)
        .inverted(false);

    motor.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters); //把設定丟到馬達上

- kResetSafeParameters: 要不要把馬達弄回出廠設定(通常要，因為你不知道上一個用的人對他做了什麼事)
- kPersistParameters: 要不要把設定應用出來(當然要啊，不然用心酸的喔)

眼尖的你應該知道，對，SparkMax也可以控制有刷馬達，然後如果要裝編碼器的話，請看這邊

.. website:: https://docs.revrobotics.com/rev-crossover-products/sensors/tbe/application-examples

SparkFlex (`REV 11-2159 <https://www.revrobotics.com/rev-11-2159/>`_)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

很像 SparkMax，不過不太一樣，他是用Vortex的

軟體要裝的包：

.. website:: https://software-metadata.revrobotics.com/REVLib-2025.json

用法

.. code-block:: java

    SparkFlex motor = new SparkMax(MotorID, MotorType.kBrushless);
    SparkFlexConfig config = new SparkMaxConfig(); //馬達的設定

    //設定設定
    config
        .idleMode(IdleMode.kBrake)
        .inverted(false);

    motor.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters); //把設定丟到馬達上

對你沒看錯基本上只要把SparkMax換成SparkFlex就通了(是不是很爽)

TalonFX
++++++++

因為他是Kraken內建的編碼器，所以整合性會更高一些。

.. code-block:: java

    TalonFX motor = new TalonFX(MotorID, CANBus);
    TalonFXConfiguration config = new TalonFXConfiguration();

    config.MotorOutput
        .withNeuralMode(NeuralModeValue.Brake)
        .withInverted(InvertedValue.CounterClockwise_Positive);

    motor.getConfigurator.apply(config);

跟SparkMax不一樣的是，TalonFX(Phoenix API)的控制會比較雜一些，不過他的控制會比REV更細膩一些些。
然後在 :code:`new TalonFXConfiguration();` 的時候，他就是原廠設定了(所以他apply會整個重刷)

軟體包：

.. website:: https://maven.ctr-electronics.com/release/com/ctre/phoenix6/latest/Phoenix6-frc2025-latest.json

TalonFXS
+++++++++

CTRE出的很像SparkMax的東西，(功能基本上也通用)，不過支援 :abbr:`CAN FD (Controller Area Network with Flexible Data-Rate)` 跟CTRE那個炫砲的PID控制。

範例程式

.. code-block:: java

    TalonFXS motor = new TalonFXS(DeviceID, canbus);
    TalonFXSConfiguration config = new TalonFXSConfiguration();

    config.MotorOutput
        .withNeuralMode(NeuralModeValue.Brake)
        .withInverted(InvertedValue.Clockwise_Positive);
    
    motor.getConfigurator().apply(motor);

你的感覺沒錯，這個東西的感覺跟TalonFX有87%像。

軟體包：

.. website:: https://maven.ctr-electronics.com/release/com/ctre/phoenix6/latest/Phoenix6-frc2025-latest.json

TalonSRX
++++++++++

TalonSRX是CTRE針對有刷馬達的所推出的控制器(也因為只能控制有刷所以他基本上也快被遺棄掉了)

.. code-block:: java

    TalonSRX motor = new TalonSRX(DeviceID);
    motor.setInverted(InvertType.InvertMotorOutput);
    motor.setNeutralMode(NeutralMode.Brake);

用看的感覺起來就特別的上古時代，就連他的API都是用上一代的Phoenix 5，就知道他有多過時(大誤)

需要的軟體包

.. website:: https://maven.ctr-electronics.com/release/com/ctre/phoenix/Phoenix5-frc2025-latest.json

.. note:: 他在下載的時候會連Phoenix 6一起下載，不要刪掉，不然會報錯。
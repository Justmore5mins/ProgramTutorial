專有名詞們
============

A
----

AM
++++
    AM是 `AndyMark <https://andymark.com>`_ 的簡稱，AndyMark是FRC物件提供的集大成，除了KOP(Kit of Part)底盤是他們做的以外，也有代賣其他提供商(例如WCP, CTRE)的東西，也因為這個特性，所以基本上只要不要太新或偏僻的東西都會有andymark的sku。

AprilTags
+++++++++
    AprilTag是一種視覺辨識的目標，因為有事先規定大小跟位置，所以在相機 `校正 <https://docs.photonvision.org/en/latest/docs/calibration/calibration.html>`_ 後，只要FPS不要太低(通常20~40+fps)就可以當作位置校正的來源。

    .. figure:: https://docs.photonvision.org/en/latest/_images/apriltag-coords.png
        :width: 80%
        :align: center

        ⬆️ 可愛的AprilTag(?)

    .. admonition:: 熱知識
        :class: important

        FRC用的AprilTag類別(Family)是36h11。

Anderson
++++++++
    電線連接方式，雖然比WAGO麻煩，但也不容易鬆脫。

auto / auton / autonomous
+++++++++++++++++++++++++
    比賽前15秒的自動模式。操作手不能動，但DS仍可強制停止。

B
----

BOM
++++
    Bill of Materials 材料表，通常CAD完成後一起輸出，用於採買與資源管理。

Brake / Coast
+++++++++++++
    馬達模式。Brake：急停。Coast：自然停。底盤/電梯常用Brake，Shooter常用Coast。

Behind the Bumpers
++++++++++++++++++
    由 FUN Robotics Network 拍攝的隊伍介紹影片（10–20分鐘）。

Brownout
++++++++
    電壓過低保護。

Bumper
++++++
    機器保險桿，需要與聯盟顏色一致（紅/藍）。

C
----

CAD
++++
    CAD(Computer Aided Design)為設計機構必備。常見軟體：OnShape、SolidWorks、Solid Edge。

CAM
++++
    CAM(Computer Aided Manufacturing)，將CAD輸出轉成CNC可讀代碼。

CAN
++++
    CAN(Controller Area Network bus, 控制器區域網路匯流排)是一種通訊協定，透過兩組線(H跟L)跟 `菊花鏈 <https://yu-yue.medium.com/frc-can-bus-2dbffef338fe>`_ 可以便利的將所有需要控制與資料傳輸的東西都整合到一個通用的系統上，非常的方便。

CAN-FD
+++++++
    CAN-FD(Controller Area Network with Flexible Datarate, 有彈性資料率的控制器區域網路匯流排)，相比於一般的CAN系統，最大的好處是能承受更大的資料吞吐量跟提供更快的傳輸速度。在實際應用上比如能用高頻率里程計(High frequency odometry)跟更多的CAN裝置等等。

    有關他的詳細技術資料可以看

    .. website:: https://store.ctr-electronics.com/pages/can-fd?srsltid=AfmBOoqjem5EACaZ6MSkZlq_LfVHTh3sA1v2_DrQMAq-AeCSaLDeZxqL

    .. admonition:: 冷知識
        :class: note

        因為CAN是CTRE跟Ni一起開發的，所以CTRE他們家跟FRC有關的電子產品10個有11個都是用CAN迴路走資料的。


CD
+++
    Chief Delphi是受47隊啟發，FRC中最大的以社群為基礎的論壇，基本上各種問題與公告甚至是求神問卜都可以在上面問(誤)

    .. website:: https://www.chiefdelphi.com
        :title: Chief Delphi

    .. admonition:: 冷知識
        :class: note

        `Team 47 <https://www.thebluealliance.com/team/47>`_ 在1996年創立，2009年就沒有消息了，阿們。


CIM
++++
    最強有刷馬達。MiniCIM為其縮小版。

    .. figure:: https://andymark.com/cdn/shop/files/am-0255_1200x1200.jpg?v=1749948964
        :width: 80%
        :align: center

        CIM馬達

Command Based Programming
+++++++++++++++++++++++++
    指令架構編程是把每個要做的事情打包成指令一次丟給子系統(subsystem)執行，相比於傳統的Timed Based，他對於整體程式的可讀性、可維護性與易預測性都會比較高，不過開發時間也會相對長一些

COTS
++++
    Commercial off the shelf，翻譯成中文就是現成的東西，規則基本上比較危險的(例如馬達或需要過電的東西)規定一定要是現成的東西，還不能自己爆改(因為他們沒辦法確定爆改之後有沒有放定時炸彈在裡面)

    .. admonition:: 冷知識
        :class: note

        根據 `這個貼文 <https://www.chiefdelphi.com/t/fun-weird-questions-is-this-legal-to-appear-on-the-robot/507667>`_ ，乖乖綁在機器上是合法的喔


Chassis / Drivetrain
++++++++++++++++++++
    就是底盤，主要有分差速底盤(Differential Drive)、麥克納姆倫(Mecanum Drive)跟向量底盤(Swerve Drive)

Closed / Open Loop
++++++++++++++++++

    閉環/開環控制是在速度與位置控制中是神聖而不可分割的一部分(?)。兩者最大的區別就是有沒有 ``反饋`` 。以自動灑水器的例子來說，一個開還控制器的自動灑水器管他有沒有颳風下雨嚼檳榔(?)，只要時間一到就噴，管他三七二十一，這樣的控制方法固然簡單，不過顯而易見的是很容易造成額外資源的浪費，以噴墨印表機來說，如果用開環的話，今天在印東西的時候如果有誤差(例如有人撞到列印機)，他的噴頭被撞飛了機器還沒發現，就有可能原本要印AprilTag結果變成4K高清Rickroll的照片了。

    .. image:: https://i.ytimg.com/vi/pqFD6psRDm8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDPTuWQtBi8vspc1rhoL8lNxgNmYA
        :width: 60%
        :align: center

    .. attention:: 
        因為閉環與前饋控制的內容比較複雜，有興趣或是鹽巴加太多太閒的人可以看 `這邊 <ClosedLoop.html>`_
        

CSA
++++
    Control System Advisor，可諮詢控制與通訊相關問題。

D
----

DS
++++
    DriverStation的簡稱，如果指軟體的話就是windows上的那個跟機器連接的DriverStation，如果是硬體的話就是場地兩邊，Driver會站的地方


E
----

E-stop / A-stop
+++++++++++++++
    在DriverStation上的兩個PLC開關，通常顏色會不一樣，E-stop(Emergency Stop,緊急停機)會把機器整場disable掉, A-stop(Auton Stop,自動停機)會在Auto的時候把機器停掉，但是TeleOp還是能繼續開。

Elevator / Arm / Telescope
++++++++++++++++++++++++++
    三種常見機構用於運送物件。

    .. figure:: https://images2.imgbox.com/ec/72/1ZniQXdY_o.png
        :width: 60%
        :align: center

    Elevator範例  
    .. website:: https://www.youtube.com/watch?v=l-rA5-0sE44

    Arm範例  
    .. website:: https://www.youtube.com/watch?v=Tnl4hQlI1Gc

    Telescope範例  
    .. website:: https://www.youtube.com/watch?v=kfg6I2UIN_Q

F
----

FMS
++++
    FMS(Field Manangement System, 場地管理系統)是在一個event中控制所有跟場地有關的東西，小到DS上的PLC開關，大到場地中央的直播螢幕都是他在管的，不過最重要的控制項目是在控制機器人在比賽間的通訊，最長常掉的地方也是在那裡。

FTA
++++
    FIRST Technical Advisor(FIRST技術顧問)就是當遇到技術問題的時候，可以問的人，通常在比賽場上可以決定有東西爆了(例如RSL)之後還能不能上場

FUN Robotics Network
+++++++++++++++++++++
    一個專門在拍機器人(FRC, FTC, FLL, VEX都有)的歪踢頻道
    
    .. website:: https://www.youtube.com/@FUNRoboticsNetwork

FF / Feed Forward
++++++++++++++++++
    請看 `這邊 <ClosedLoop.html>`_

I
----

IMU
++++
    簡單來說就是集成陀螺儀跟加速度儀的東西，賽場上常見的有 `NavX2 <https://andymark.com/products/navx2-mxp-robotics-navigation-sensor>`_ 跟 `Pigeon 2.0 <https://store.ctr-electronics.com/products/pigeon-2?_pos=1&_sid=21854bcdb&_ss=r>`_


Intake
++++++
    廣義上來說有分under bumper intake跟over bumper intake，請看例子

    under bumper:

    .. website:: https://www.youtube.com/watch?v=bQV_KAZdCJ0

    over bumper:(第一段介紹就好了)

    .. website:: https://www.youtube.com/watch?v=oAOJTfFOP9I&t=709s

K
----

KOP / AM14U / KitBot
++++++++++++++++++++
    Kit of Part是FRC在公布題目的時候的範例機器人，帶有最基礎的得分功能，在kickoff影片的時候看起來最具體的那台八成就是KitBot，也因為顧及價格因素，通常會搭配NEO跟CIM馬達。

    AM14U就是Andymark推出的底盤，採用差速控制的方式來駕駛。

    .. website:: https://andymark.com/products/am14u6-6-wheel-drop-center-robot-drive-base-2025-frc-kit-of-parts-drive-base

Kickoff / Kickoof
+++++++++++++++++
    在每年的一月初或中時，在台灣時間的凌晨坐在電視機(?)前面看FRC那年的題目是什麼(不過根據經驗，要先聽一大段幹話之後才會是題目內容,請見 `FTC kickoff <https://youtu.be/tRlcAwgMx5Q?si=GOKD-3rTD18c--op>`_ )

L
----

LL / Limelight
++++++++++++++
    一個AIO(All in one)的視覺辨識裝置，目前出到第四代了，競爭品多是主控板+webcam的配置，例如 `Rubik Pi 3 <https://rubikpi.ai>`_ 或是 `Jetson Orin Nano <https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>`_ 搭配PV

    .. website:: https://limelightvision.io

LQR / Model Based Control
+++++++++++++++++++++++++
    Linear Quadratic Regulator(線性二次調節器)，簡單介紹請看這邊

    .. website:: https://www.instagram.com/p/DQZGLUnkr8N/

M
----

MOI
++++
    轉動慣量（Moment of Inertia）。

MXP
+++
    RIO中央的擴充介面，如NavX2會插此處。

Mecanum
++++++++
    麥克納姆輪是一種特殊的輪子，用他不同的受力方式讓他在KOP的長相不過能達到接近Swerve的效果。在FRC中算是KOP跟swerve中間的銜接底盤。在程式複雜度跟靈活性都介於KOP跟swerve之間。

    .. figure:: https://i.redd.it/7lqtqo4k31ce1.jpeg
        :width: 60%
        :align: center

        麥克納姆輪本尊

    .. figure:: https://www.researchgate.net/publication/367879750/figure/fig1/AS:11431281116841895@1675318925027/Movements-of-a-Mecanum-wheel-driven-robot-to-any-directions-side-arrows-indicate-wheel.png
        :width: 60%
        :align: center

        麥克納姆輪的動力學

N
----

Ni
+++
    National Instruments 做RoboRIO的廠家

P
----

PCM
++++
    Pneumatic Control Module，氣控模組。

PDH / PDP
+++++++++
    PDH(Power Distrubtion Hub)跟PDP(Power Distrubtion Panel)都是配電盤，不過一間是REV出的(一間是CTRE出的)。

    .. admonition:: 補充
        :class: note

        雖然Andymark有自己出一個配電盤，不過目前最好用的是REV的配電盤

PoE
+++
    Power over Ethernet，用乙太網路供電的方式除了可以少接兩條線外，還可以讓走線更簡潔，簡直超爽(不過FRC用的是被動式的12~24V的PoE)，不過通常有接PoE就不能接12V的紅黑線了，會爆掉。

    .. figure:: https://megapx-assets.dcard.tw/images/383141ff-d653-404a-81e5-3ab5cc5bc75c/640.jpeg
        :width: 60%
        :align: center

        小黑：當你同時接PoE跟旁邊的紅黑線的時候

PhotonVision / PV
+++++++++++++++++
    一個由6328開發的開源影像處理軟體，常被FRC的隊伍使用

    .. website:: https://photonvision.org

PathPlanner / PP
+++++++++++++++++
    一個路徑規劃軟體，在Auto的部分使用，也因為他支援實時路徑生成，所以也有被用在自動化路徑設計。也因為他易於使用的GUI設計，使他成為常見的Auto路徑規劃的軟體之一

R
----

REV
++++
    就是那個傳說中NEO跟SparkMax的製造商，主打的是親民的價格跟還可以用的性能，常常受rookie隊伍喜歡


RI / LRI
++++++++
    (lead) Robot Inspector機器檢查員就是在比賽開始前檢查機器時檢查機器的人，通常包含重量，毛邊與電檢。

RSL
++++
    Robot Signal Light(機器訊號燈)是在機器人上一定要有的東西(沒有會被鞭數十，驅之別院)，而且要跟RIO上的RSL信號燈同步

Ri3D
++++
    Robot in 3 days，國外有一群FRC狂人會在題目公布後不眠不休輪班在三天之內把機器設計跟做出來，常常被rookie或是中階隊伍參考當作機器設計idea。

rookie
++++++
    新隊伍

Robot Reveal
++++++++++++
    機器的展示影片，主要是在炫耀自己隊伍設計的機器超屌(並沒有好嗎)。國外的強隊(例如1690, 6328, 118)等都會有，不過時間會比Ri3D晚，通常會在題目公布後2~3週才會有。


RoboRIO
+++++++
    機器的車控電腦

    .. website:: https://andymark.com/products/ni-roborio-2-0


S
----

SKU
+++
    Stock keeping unit，庫存單位。在FRC中，只要是廠家有在賣的東西(例如馬達)，九成都會有一個自己的SKU而且不會重複，不了解的可以想像成是番號就好了(咦？)


Swerve
++++++
    中文比較常見的翻譯是向量底盤，向量底盤的最大特徵是一顆輪子會有兩顆馬達來帶，一顆用來開，一顆用來轉向。也是目前FRC性能最強的底盤。(還有爆幹貴也是他的特徵之一)

    .. figure:: https://docs.wcproducts.com/frc-build-system/~gitbook/image?url=https%3A%2F%2F1911150060-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FByQLBt0bw4wTa9DDV1kH%252Fuploads%252F7UbfXEiTI9ZpmDVhaMlt%252FSwerve%2520XS%2520-%2520Cover.svg%3Falt%3Dmedia%26token%3D991027b6-c7d5-4ed0-b708-6eca771c1def&width=768&dpr=4&quality=100&sign=166a89a3&sv=2
        :width: 60%
        :align: center

        ⬆️向量模塊之一(WCP的)

SDS
+++
    Swerve Drive Specialties，看名字應該知道是賣什麼的，除了向量模塊以外，還有電梯滑塊也還不錯用

    .. website:: https://www.swervedrivespecialties.com

SystemCore
++++++++++
    2027年與之後的RoboRIO的名字，相比於一般的RIO，有支援CAN-FD跟內建IMU還有跟LimeLight合作內建的視覺處理單元就已經可以屌打RoboRIO 2.0了，據說還會比較便宜？

    .. website:: https://docs.wpilib.org/en/2027/docs/software/systemcore-info/systemcore-introduction.html

T
----

TBA
++++
    The Blue Alliance, 一個拿來看隊伍的資料跟情蒐還蠻好用ㄉ網站

    .. website:: https://www.thebluealliance.com

TeleOp
++++++
    手動模式，在比賽中過完前面15秒的之後的模式，不過有些視覺很強的隊伍也把手動當自動開。

Thrifty Bot / TTB
+++++++++++++++++
    做電梯連接跟telescope蠻有名的，最近有出相機跟進軍swerve市場。

    .. website:: https://www.thethriftybot.com

Timed Based
+++++++++++

    最簡單的程式架構，比較常拿來用在初期測試還有看東西有沒有壞掉。

V
-

VH-109 / 小黑
+++++++++++++
    FRC 2025開始用的Radio，相比於OpenMesh的小白，他用6GHz的頻段可以提供更低延遲的傳輸(應該)，而且當FMS爆掉的時候，能用6GHz對連的小黑也比純2.4GHz好。不過出了名的容易過熱當機(大概連續1.5~2小時)

    .. website:: https://frc-radio.vivid-hosting.net

    .. figure:: https://store.ctr-electronics.com/cdn/shop/files/VH-109_WCP-1538_2_2048x2048_bd9e86db-7e66-4029-975c-62b6654f6bfd.webp?v=1729551120&width=1445
        :width: 60%
        :align: center

        小黑(2025-)

    .. figure:: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3tSHTfgUmbi8RYq0GYhO_JhWp3rHV5wFobw&s
        :width: 60%
        :align: center

        小白(2016-2024)

W
----

WAGO
++++
    快速接線方式，比Anderson快但可能脫落。

WCP
+++
    West Coast Product，跟andymark很像，不過他是都有自己賣，而且還有跟CTRE合作推出馬達喔(就是Kraken X60跟x44)。

    .. website:: https://wcproducts.com

WPILib
++++++
    就是你各位寫程式用的那個圖書館(library)

    .. website:: https://docs.wpilib.org

VRM
+++
    Voltae Regulator Module，電壓穩定模組，主要供應對電壓要求比較高的東西(比如webcam或是有的沒有的sensor)

    .. website:: https://hackmd.io/@FRC-7130-4th/BkZF7WFx5

    .. figure:: https://store.ctr-electronics.com/cdn/shop/files/VRM__22344_1641570374_1280_1280.jpg?v=1723228408&width=416
        :width: 60%
        :align: center

        VRM本人

Y
----

YASS
++++
    Yet Another Software Suite 是由3481, 457, 3561, 9658一起弄的軟體資料庫，有

       - YASGL(Yet Another Swerve Generic library,弄向量底盤的)
       - YAMS(Yet another mechnism system, 弄電梯跟手臂的)
       - YAMG(Yet Another Mechnism Generator,上面的機構的code的生成器，很神奇的是居然沒有串自己家的YAMS) 
       - YALL(Yet Another Limelight Library,搞limelight的)

    .. website:: https://yetanothersoftwaresuite.com
        :title: YASS - Yet Another Software Suite

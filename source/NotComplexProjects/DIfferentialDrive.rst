KOP底盤程式
=================

需要的硬體
------------
    1. 馬達x2 / 4
    2. 馬達控制器 x2 / 4
    3. 配好電的底盤(建議有 `陀螺儀 <../LinkedDocuments/gyroscope.html>`_ )
   
大概講解
-----------

.. code-block:: text
    :caption: 4K高清底盤

        這是前面
     輪距TrackWidth
    |--------------|
    -----------------
    | |  x       | |   這
      |  ^       |     是
      |  └>y     |     右
    | |          | |   邊
    -----------------

    ⬇️請想像他是圓的
    ┌--------┐
    |        | 
    |--------| R:直徑，輪周長:πR
    └--------┘

    如果是用KOP的話，要記得改成自己是適合的齒輪比喔

.. tip::
    如果還沒有自己寫程式的習慣的話，在變數命名這方面建議用 ``有意義`` 的方式命名(例如LeftID, RightID等)，因為可能只要換個檔案回來你就會忘記那個變數a是什麼了

初始化與定義變數
----------------

常數們:

.. code-block:: java
    :caption: Constants.java

    public static final int LeftID = 10; //左邊的ID
    public static final int RightID = 11; //右邊的ID
    public static final double WheelCirc = Inches.of(6).times(Math.PI).in(Meters); //輪子的圓周
    public static final double GearRatio = 10.71; //齒輪比
    public static final double PositionConvertionFactor = WheelCirc/GearRatio; //位置轉換係數
    public static final double VelocityConvertionFactor = PositionConvertionFactor/60; //速度轉換係數
    public static final Distance TrackWidth = Centimeters.of(65); //兩個輪子的間距
    public static final NavXComType GyroCom = NavXComType.kMXP_SPI; //設定陀螺儀的連接方式

定義需要的變數

.. code-block:: java
    :caption: DifferentialDrive.java

    public SparkMax LeftMotor, RightMotor; //差速驅動只有兩個馬達
    public RelativeEncoder LeftEncoder, RightEncoder; //兩個編碼器
    public AHRS gyro; //陀螺儀

    public DifferentialDriveKinematics kinematics; //差速驅動運動學
    public DifferentialDrivePoseEstimator PoseEstimator; //位置估計器
    private SparkMaxConfig LeftConfig, RightConfig; //馬達設定

小補充
    Encoder(編碼器)是可以藉由 `磁編碼器 <https://hackmd.io/@0914FRC10390programming/By-QB2FZel>`_ 來拿到精準的位置，速度，加速度(部分)等等的資料，對於反饋型控制有相當程度的幫助

把剛剛的變數初始化

.. code-block:: java
    :caption: DifferentialDrive.java

    //把各個東西都初始化
    LeftMotor = new SparkMax(Constants.LeftID, MotorType.kBrushless); //這邊用無刷馬達示範
    RightMotor = new SparkMax(Constants.RightID, MotorType.kBrushless);
    LeftEncoder = LeftMotor.getEncoder();
    RightEncoder = RightMotor.getEncoder();
    gyro = new AHRS(NavXComType.kMXP_SPI);

    kinematics = new DifferentialDriveKinematics(Constants.SwerveModules.TrackWidth);
    PoseEstimator = new DifferentialDrivePoseEstimator(
        kinematics,  
        gyro.getRotation2d(), 
        getPosition().leftMeters, 
        getPosition().rightMeters, 
        new Pose2d()); //初始位置，如果有視覺定位的話通常是由視覺定位提供

    LeftConfig = new SparkMaxConfig();
    RightConfig = new SparkMaxConfig();

    LeftConfig
        .idleMode(IdleMode.kBrake) //自然模式，Brake是急停(比較不滑動)，Coast是滑行
        .inverted(false) //馬達方向
        .voltageCompensation(12) //電壓補償(避免電池電壓過低影響表現)
        .smartCurrentLimit(40); //電流限制，避免馬達過熱還有降低瞬間對於電池的傷害

    LeftConfig.encoder
        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //位置轉換因子，將編碼器的單位轉換成實際單位(例如公尺)   
        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //速度轉換因子，將編碼器的單位轉換成實際單位(例如公尺/秒)

    RightConfig
        .idleMode(IdleMode.kBrake)
        .inverted(true) //右邊馬達通常需要反轉
        .voltageCompensation(12)
        .smartCurrentLimit(40);
    RightConfig.encoder
        .positionConversionFactor(Constants.DrivePositionConvertionFactor)
        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor);

    //應用設定到馬達
    LeftMotor.configure(LeftConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
    RightMotor.configure(RightConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);

還有補充需要的函數

.. code-block:: java
    :caption: DifferentialDrive.java

    /**
     * 取得左右輪位置
     * 
     * @return DifferentialDriveWheelPositions 左右輪位置
     */
    public DifferentialDriveWheelPositions getPosition(){
        return new DifferentialDriveWheelPositions(
            LeftEncoder.getPosition(), 
            RightEncoder.getPosition());
    }

    /**
     * 取得左右輪速度
     * @return DifferentialDriveWheelSpeeds 左右輪速度
     */
    public DifferentialDriveWheelSpeeds getSpeeds(){
        return new DifferentialDriveWheelSpeeds(
            LeftEncoder.getVelocity(),
            RightEncoder.getVelocity()
        );
    }

    /**
     * 差速驅動
     * @param throttle 前進速度
     * @param turn 轉向速度
     * @return Command 差速驅動指令
     */
    public Command drive(Supplier<Double> throttle, Supplier<Double> turn){
        return run(() -> { //他會執行到被打斷或是外加的.until()條件成立為止
            double leftSpeed = throttle.get() + turn.get(); //左輪速度=前進速度+轉向速度
            double rightSpeed = throttle.get() - turn.get(); //右輪速度=前進速度-轉向速度
            drive(leftSpeed, rightSpeed); //驅動馬達
        });

    }

    /**
     * 驅動馬達
     * @param leftSpeed 左邊的速度
     * @param rightSpeed 右邊的速度
     */
    private void drive(double leftSpeed, double rightSpeed){
        LeftMotor.set(leftSpeed/(5676*Constants.DrivePositionConvertionFactor)); //5676是無刷馬達的最大RPM
        RightMotor.set(rightSpeed/(5676*Constants.DrivePositionConvertionFactor)); //轉換成百分比
    }

    /**
     * 每個週期更新位置的東西
     * 
     */
    @Override
    public void periodic(){
        PoseEstimator.update(gyro.getRotation2d(), getPosition()); //更新位置
    }

小總結
-----------

在這邊，你學到了如何控制底盤的馬達

完整的程式碼：

.. tabs::

    .. tab:: Kraken X60 + Pigeon2

        .. code-block:: java
            
            public class DifferentialDrive extends SubsystemBase{
                public TalonFX LeftMotor, RightMotor;
                public Pigeon2 gyroscope;
                private TalonFXConfiguration LeftConfig, RightConfig;

                public DifferentialDriveKinematics kinemtatics;
                public DifferentialDrivePoseEstimator PoseEstimator;

                public DifferentialDrive(){
                    LeftMotor = new TalonFX(10);
                    RightMotor = new TalonFX(11);
                    gyroscope = new Pigeon2(0);

                    kinemtatics = new DifferentialDriveKinematics(Centimeters.of(65));
                    PoseEstimator = new DifferentialDrivePoseEstimator(
                        kinemtatics, 
                        gyroscope.getRotation2d(), 
                        getPosition().leftMeters, 
                        getPosition().rightMeters, 
                        new Pose2d());

                    LeftConfig = new TalonFXConfiguration(); //在這邊就會用出廠設定了
                    RightConfig = new TalonFXConfiguration();

                    LeftConfig.MotorOutput
                        .withNeutralMode(NeutralModeValue.Brake) //設定空轉模式, Brake為煞車模式, Coast為滑行模式
                        .withInverted(InvertedValue.CounterClockwise_Positive); //設定馬達反轉方向
                    LeftConfig.Feedback
                        .withSensorToMechanismRatio(Constants.DriveGearRatio); //設定編碼器轉換比例(這邊不能直接換成車輪的轉換比例, 要用馬達的齒輪比)

                    
                    RightConfig.MotorOutput
                        .withNeutralMode(NeutralModeValue.Brake) //設定空轉模式, Brake為煞車模式, Coast為滑行模式
                        .withInverted(InvertedValue.CounterClockwise_Positive); //設定馬達反轉方向
                    RightConfig.Feedback
                        .withSensorToMechanismRatio(Constants.DriveGearRatio); //設定編碼器轉換比例(這邊不能直接換成車輪的轉換比例, 要用馬達的齒輪比)

                    LeftMotor.getConfigurator().apply(LeftConfig);
                    RightMotor.getConfigurator().apply(RightConfig);
                }

                public DifferentialDriveWheelPositions getPosition(){
                    return new DifferentialDriveWheelPositions(
                        LeftMotor.getPosition().getValue().times(Constants.WheelCirc).in(MultUnit.combine(Rotations, Meters)), //把馬達的旋轉轉換成車輪移動的距離
                        LeftMotor.getPosition().getValue().times(Constants.WheelCirc).in(MultUnit.combine(Rotations, Meters))
                    );
                }

                public DifferentialDriveWheelSpeeds getVelocity(){
                    return new DifferentialDriveWheelSpeeds(
                        LeftMotor.getVelocity().getValue().times(Constants.WheelCirc).in(MultUnit.combine(RotationsPerSecond, Meters)), //把馬達的旋轉速度轉換成車輪的線速度
                        RightMotor.getVelocity().getValue().times(Constants.WheelCirc).in(MultUnit.combine(RotationsPerSecond, Meters))
                    );
                }

                public Command drive(Supplier<Double> ForwardMPS, Supplier<Double> RotationMPS){
                    return run(() -> {
                        DifferentialDriveWheelSpeeds speeds = new DifferentialDriveWheelSpeeds(ForwardMPS.get() + RotationMPS.get(), ForwardMPS.get() - RotationMPS.get()); //計算左右輪速度
                        speeds.desaturate(6000*Constants.DriveVelocityConvertionFactor); //限制最大速度
                        drive(speeds.leftMetersPerSecond, speeds.rightMetersPerSecond); //設定馬達速度
                    });
                    
                }

                private void drive(double leftSpeed, double rightSpeed){
                    LeftMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                    RightMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                }

                @Override
                public void periodic(){
                    PoseEstimator.update(gyroscope.getRotation2d(), getPosition());
                }
            }
    .. tab:: NEO + NavX(AHRS)

        .. code-block:: java

            public class DifferentialDrive extends SubsystemBase{
                public SparkMax LeftMotor, RightMotor;
                public RelativeEncoder LeftEncoder, RightEncoder;
                public AHRS gyroscope;
                private SparkMaxConfig LeftConfig, RightConfig;

                public DifferentialDriveKinematics kinemtatics;
                public DifferentialDrivePoseEstimator PoseEstimator;

                public DifferentialDrive(){
                    LeftMotor = new SparkMax(10, MotorType.kBrushless);
                    RightMotor = new SparkMax(11, MotorType.kBrushless);
                    gyroscope = new AHRS(NavXComType.kMXP_SPI);

                    kinemtatics = new DifferentialDriveKinematics(Centimeters.of(65));
                    PoseEstimator = new DifferentialDrivePoseEstimator(
                        kinemtatics, 
                        gyroscope.getRotation2d(), 
                        getPosition().leftMeters, 
                        getPosition().rightMeters, 
                        new Pose2d());

                    LeftConfig = new SparkMaxConfig();
                    RightConfig = new SparkMaxConfig();

                    LeftConfig
                        .idleMode(IdleMode.kBrake)
                        .inverted(false)
                        .voltageCompensation(12) //啟用電壓補償, 參數為標準電壓
                        .smartCurrentLimit(40); //設定馬達電流限制(為滑動前能承受的最大電流(SlipCurrent))
                    LeftConfig.encoder
                        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //設定編碼器位置轉換比例
                        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //設定編碼器速度轉換比例
                        
                    
                    RightConfig
                        .idleMode(IdleMode.kBrake)
                        .inverted(true)
                        .voltageCompensation(12) //啟用電壓補償, 參數為標準電壓
                        .smartCurrentLimit(40); //設定馬達電流限制(為滑動前能承受的最大電流(SlipCurrent))
                    RightConfig.encoder
                        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //設定編碼器位置轉換比例
                        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //設定編碼器速度轉換比例
                    
                    LeftMotor.configure(LeftConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
                    RightMotor.configure(RightConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
                }

                public DifferentialDriveWheelPositions getPosition(){
                    return new DifferentialDriveWheelPositions(
                        LeftEncoder.getPosition(),
                        RightEncoder.getPosition()
                    );
                }

                public DifferentialDriveWheelSpeeds getVelocity(){
                    return new DifferentialDriveWheelSpeeds(
                        LeftEncoder.getVelocity(),
                        RightEncoder.getVelocity()
                    );
                }

                public Command drive(Supplier<Double> ForwardMPS, Supplier<Double> RotationMPS){
                    return run(() -> {
                        DifferentialDriveWheelSpeeds speeds = new DifferentialDriveWheelSpeeds(ForwardMPS.get() + RotationMPS.get(), ForwardMPS.get() - RotationMPS.get()); //計算左右輪速度
                        speeds.desaturate(6000*Constants.DriveVelocityConvertionFactor); //限制最大速度
                        drive(speeds.leftMetersPerSecond, speeds.rightMetersPerSecond); //設定馬達速度
                    });
                    
                }

                private void drive(double leftSpeed, double rightSpeed){
                    LeftMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                    RightMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                }

                @Override
                public void periodic(){
                    PoseEstimator.update(gyroscope.getRotation2d(), getPosition());
                }
            }

    .. tab:: Kraken + NavX(AHRS)

        .. code-block:: java

            public class DifferentialDrive extends SubsystemBase{
                public TalonFX LeftMotor, RightMotor;
                public AHRS gyroscope;
                private TalonFXConfiguration LeftConfig, RightConfig;

                public DifferentialDriveKinematics kinemtatics;
                public DifferentialDrivePoseEstimator PoseEstimator;

                public DifferentialDrive(){
                    LeftMotor = new TalonFX(10);
                    RightMotor = new TalonFX(11);
                    gyroscope = new AHRS(NavXComType.kMXP_SPI);

                    kinemtatics = new DifferentialDriveKinematics(Centimeters.of(65));
                    PoseEstimator = new DifferentialDrivePoseEstimator(
                        kinemtatics, 
                        gyroscope.getRotation2d(), 
                        getPosition().leftMeters, 
                        getPosition().rightMeters, 
                        new Pose2d());

                    LeftConfig = new TalonFXConfiguration(); //在這邊就會用出廠設定了
                    RightConfig = new TalonFXConfiguration();

                    LeftConfig.MotorOutput
                        .withNeutralMode(NeutralModeValue.Brake) //設定空轉模式, Brake為煞車模式, Coast為滑行模式
                        .withInverted(InvertedValue.CounterClockwise_Positive); //設定馬達反轉方向
                    LeftConfig.Feedback
                        .withSensorToMechanismRatio(Constants.DriveGearRatio); //設定編碼器轉換比例(這邊不能直接換成車輪的轉換比例, 要用馬達的齒輪比)

                    
                    RightConfig.MotorOutput
                        .withNeutralMode(NeutralModeValue.Brake) //設定空轉模式, Brake為煞車模式, Coast為滑行模式
                        .withInverted(InvertedValue.CounterClockwise_Positive); //設定馬達反轉方向
                    RightConfig.Feedback
                        .withSensorToMechanismRatio(Constants.DriveGearRatio); //設定編碼器轉換比例(這邊不能直接換成車輪的轉換比例, 要用馬達的齒輪比)

                    LeftMotor.getConfigurator().apply(LeftConfig);
                    RightMotor.getConfigurator().apply(RightConfig);
                }

                public DifferentialDriveWheelPositions getPosition(){
                    return new DifferentialDriveWheelPositions(
                        LeftMotor.getPosition().getValue().times(Constants.WheelCirc).in(MultUnit.combine(Rotations, Meters)), //把馬達的旋轉轉換成車輪移動的距離
                        LeftMotor.getPosition().getValue().times(Constants.WheelCirc).in(MultUnit.combine(Rotations, Meters))
                    );
                }

                public DifferentialDriveWheelSpeeds getVelocity(){
                    return new DifferentialDriveWheelSpeeds(
                        LeftMotor.getVelocity().getValue().times(Constants.WheelCirc).in(MultUnit.combine(RotationsPerSecond, Meters)), //把馬達的旋轉速度轉換成車輪的線速度
                        RightMotor.getVelocity().getValue().times(Constants.WheelCirc).in(MultUnit.combine(RotationsPerSecond, Meters))
                    );
                }

                public Command drive(Supplier<Double> ForwardMPS, Supplier<Double> RotationMPS){
                    return run(() -> {
                        DifferentialDriveWheelSpeeds speeds = new DifferentialDriveWheelSpeeds(ForwardMPS.get() + RotationMPS.get(), ForwardMPS.get() - RotationMPS.get()); //計算左右輪速度
                        speeds.desaturate(6000*Constants.DriveVelocityConvertionFactor); //限制最大速度
                        drive(speeds.leftMetersPerSecond, speeds.rightMetersPerSecond); //設定馬達速度
                    });
                    
                }

                private void drive(double leftSpeed, double rightSpeed){
                    LeftMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                    RightMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                }

                @Override
                public void periodic(){
                    PoseEstimator.update(gyroscope.getRotation2d(), getPosition());
                }
            }
    
    .. tab:: NEO + Pigeon2

        .. code-block:: java

            public class DifferentialDrive extends SubsystemBase{
                public SparkMax LeftMotor, RightMotor;
                public RelativeEncoder LeftEncoder, RightEncoder;
                public Pigeon2 gyroscope;
                private SparkMaxConfig LeftConfig, RightConfig;

                public DifferentialDriveKinematics kinemtatics;
                public DifferentialDrivePoseEstimator PoseEstimator;

                public DifferentialDrive(){
                    LeftMotor = new SparkMax(10, MotorType.kBrushless);
                    RightMotor = new SparkMax(11, MotorType.kBrushless);
                    gyroscope = new Pigeon2(12);

                    kinemtatics = new DifferentialDriveKinematics(Centimeters.of(65));
                    PoseEstimator = new DifferentialDrivePoseEstimator(
                        kinemtatics, 
                        gyroscope.getRotation2d(), 
                        getPosition().leftMeters, 
                        getPosition().rightMeters, 
                        new Pose2d());

                    LeftConfig = new SparkMaxConfig();
                    RightConfig = new SparkMaxConfig();

                    LeftConfig
                        .idleMode(IdleMode.kBrake)
                        .inverted(false)
                        .voltageCompensation(12) //啟用電壓補償, 參數為標準電壓
                        .smartCurrentLimit(40); //設定馬達電流限制(為滑動前能承受的最大電流(SlipCurrent))
                    LeftConfig.encoder
                        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //設定編碼器位置轉換比例
                        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //設定編碼器速度轉換比例
                        
                    
                    RightConfig
                        .idleMode(IdleMode.kBrake)
                        .inverted(true)
                        .voltageCompensation(12) //啟用電壓補償, 參數為標準電壓
                        .smartCurrentLimit(40); //設定馬達電流限制(為滑動前能承受的最大電流(SlipCurrent))
                    RightConfig.encoder
                        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //設定編碼器位置轉換比例
                        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //設定編碼器速度轉換比例
                    
                    LeftMotor.configure(LeftConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
                    RightMotor.configure(RightConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
                }

                public DifferentialDriveWheelPositions getPosition(){
                    return new DifferentialDriveWheelPositions(
                        LeftEncoder.getPosition(),
                        RightEncoder.getPosition()
                    );
                }

                public DifferentialDriveWheelSpeeds getVelocity(){
                    return new DifferentialDriveWheelSpeeds(
                        LeftEncoder.getVelocity(),
                        RightEncoder.getVelocity()
                    );
                }

                public Command drive(Supplier<Double> ForwardMPS, Supplier<Double> RotationMPS){
                    return run(() -> {
                        DifferentialDriveWheelSpeeds speeds = new DifferentialDriveWheelSpeeds(ForwardMPS.get() + RotationMPS.get(), ForwardMPS.get() - RotationMPS.get()); //計算左右輪速度
                        speeds.desaturate(6000*Constants.DriveVelocityConvertionFactor); //限制最大速度
                        drive(speeds.leftMetersPerSecond, speeds.rightMetersPerSecond); //設定馬達速度
                    });
                    
                }

                private void drive(double leftSpeed, double rightSpeed){
                    LeftMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                    RightMotor.set(leftSpeed/(6000*Constants.DrivePositionConvertionFactor));
                }

                @Override
                public void periodic(){
                    PoseEstimator.update(gyroscope.getRotation2d(), getPosition());
                }
            }

    .. tab:: Timed Based(NEO+AHRS)

        .. code-block:: java

            public class Robot extends TimedRobot {
                public class DifferentialDrive extends SubsystemBase{
                public SparkMax LeftMotor, RightMotor;
                public RelativeEncoder LeftEncoder, RightEncoder;
                public AHRS gyroscope;
                private SparkMaxConfig LeftConfig, RightConfig;

                public DifferentialDriveKinematics kinemtatics;
                public DifferentialDrivePoseEstimator PoseEstimator;

                public XboxController controller = new XboxController(0);

                public Robot() {
                       LeftMotor = new SparkMax(10, MotorType.kBrushless);
                    RightMotor = new SparkMax(11, MotorType.kBrushless);
                    gyroscope = new AHRS(NavXComType.kMXP_SPI);

                    kinemtatics = new DifferentialDriveKinematics(Centimeters.of(65));
                    PoseEstimator = new DifferentialDrivePoseEstimator(
                        kinemtatics, 
                        gyroscope.getRotation2d(), 
                        getPosition().leftMeters, 
                        getPosition().rightMeters, 
                        new Pose2d());

                    LeftConfig = new SparkMaxConfig();
                    RightConfig = new SparkMaxConfig();

                    LeftConfig
                        .idleMode(IdleMode.kBrake)
                        .inverted(false)
                        .voltageCompensation(12) //啟用電壓補償, 參數為標準電壓
                        .smartCurrentLimit(40); //設定馬達電流限制(為滑動前能承受的最大電流(SlipCurrent))
                    LeftConfig.encoder
                        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //設定編碼器位置轉換比例
                        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //設定編碼器速度轉換比例
                        
                    
                    RightConfig
                        .idleMode(IdleMode.kBrake)
                        .inverted(true)
                        .voltageCompensation(12) //啟用電壓補償, 參數為標準電壓
                        .smartCurrentLimit(40); //設定馬達電流限制(為滑動前能承受的最大電流(SlipCurrent))
                    RightConfig.encoder
                        .positionConversionFactor(Constants.DrivePositionConvertionFactor) //設定編碼器位置轉換比例
                        .velocityConversionFactor(Constants.DriveVelocityConvertionFactor); //設定編碼器速度轉換比例
                    
                    LeftMotor.configure(LeftConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
                    RightMotor.configure(RightConfig, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
                }

                @Override
                public void robotPeriodic() {
                    PoseEstimator.update(gyro.getRotation2d(), new DifferentialDriveWheelPositions(LeftEncoder.getPosition, RightEncoder.getPosition));
                }
                @Override
                public void teleopPeriodic() {
                    double forward = controller.getLeftY() + ;
                    double rotation = controller.getLeftX();
                    LeftMotor.set(forward+rotation);
                    RightMotor.set(forward-rotation);
                }
            }

Command Based看這邊，還要寫RobotContainer喔

.. code-block:: java

    public class RobotContainer {
        public DifferentialDrivetrain drivetrain = new DifferentialDrivetrain();
        public XoboxController controller = new XboxController(0);
        
        public RobotContainer() {
           
           drivetrain.setDefaultCommand(drivetrain.drive(
            () -> controller.getLeftY() * Constants.MaxVelocity,
            () -> controller.getLeftX() * Constants.MaxOmega
           ))
        }

        private void configureBindings() {
        }

        public Command getAutonomousCommand() {
            return Commands.print("No autonomous command configured");
        }
    }


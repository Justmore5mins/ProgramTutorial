FRC的程式架構
===============

FRC的程式架構主要分兩種: ``Timed Based`` 與 ``Command Based`` 這兩個主要差在Timed based雖然方便開發，但是到比較複雜的專案(例如比賽的時候整台機器的程式)就會很難維護跟debug，反觀Command Based，他雖然架構很明確，而且非常容易維護，不過壞處就是會寫很多原本Timed Based不用寫的程式碼。

使用情境：

Timed Based:
    - 剛拿到新東西要試API的時候
    - 一個東西不確定有沒有壞掉跑跑看程式的時候
    - 短時間/簡單的測試

Command based:
    - 完整的機器的專案
    - 需要多人共編的環境
    - 長時間/複雜的專案

Timed Based：

最小執行單位是一行程式碼，就含其他程式的專案一樣，就是由上往下一條條執行。

.. code-block:: java
    :caption: TimedBased.java

    //Libraries url
    //https://software-metadata.revrobotics.com/REVLib-2023.json
    //https://maven.ctr-electronics.com/release/com/ctre/phoenix/Phoenix5-frc2023-latest.json

    package frc.robot;

    public class Robot extends TimedRobot {
        private CANSparkMax motor0; // intake馬達
        private CANSparkMax motor1; // 底盤馬達
        private CANSparkMax motor2; // 底盤馬達
        private CANSparkMax motor3; // 底盤馬達
        private CANSparkMax motor4; // 底盤馬達
        private CANSparkMax motor5; // 升降機構
        private CANSparkMax motor6; // 升降機構
        private CANSparkMax motor7; // Shooter馬達
        private CANSparkMax motor8; // Shooter馬達
        private RelativeEncoder encoder5; // 軸編碼器
        private RelativeEncoder encoder6; // 軸編碼器
        private MotorControllerGroup right;
        private MotorControllerGroup left;
        private DifferentialDrive drive;
        private Joystick joystick;
        private double startTime;

        @Override
        public void robotInit() {
            motor0 = new CANSparkMax(9, MotorType.kBrushless);
            motor1 = new CANSparkMax(1, MotorType.kBrushless);
            motor2 = new CANSparkMax(2, MotorType.kBrushless);
            motor3 = new CANSparkMax(3, MotorType.kBrushless);
            motor4 = new CANSparkMax(4, MotorType.kBrushless);
            motor5 = new CANSparkMax(5, MotorType.kBrushless);
            motor6 = new CANSparkMax(6, MotorType.kBrushless);
            motor7 = new CANSparkMax(7, MotorType.kBrushless);
            motor8 = new CANSparkMax(8, MotorType.kBrushless);

            encoder5 = motor5.getEncoder();
            encoder6 = motor6.getEncoder();

            motor5.restoreFactoryDefaults();
            motor6.restoreFactoryDefaults();

            encoder5.setPosition(0);
            encoder6.setPosition(0);

            left = new MotorControllerGroup(motor1, motor2);
            right = new MotorControllerGroup(motor3, motor4);

            drive = new DifferentialDrive(left, right);
            joystick = new Joystick(0);
        }

        @Override
        public void teleopPeriodic() {
            // 底盤變數
            double turnSpeed = 0.4 * joystick.getRawAxis(0);
            double driveSpeed = 0.6 * joystick.getRawAxis(5);
            // 編碼器變數 (Pos是位置、Spd是速度)
            double motorPos5 = encoder5.getPosition();
            double motorSpd5 = encoder5.getVelocity();
            double motorPos6 = encoder6.getPosition();
            double motorSpd6 = encoder6.getVelocity();

            // intke運作
            if (joystick.getRawButton(1)) {
            motor0.set(0.8);
            } else if (joystick.getRawButton(2)) {
            motor0.set(-0.8);
            } else {
            motor0.set(0);
            }

            // 升降機構運作
            if (joystick.getRawButton(5)) {
            motor5.set(0.3);
            motor6.set(-0.3);
            } else if (joystick.getRawButton(6)) {
            motor5.set(-0.3);
            motor6.set(0.3);
            } else {
            motor5.set(0);
            motor6.set(0);
            }

            // shooter運作
            if (joystick.getRawButton(3)) {
            motor7.set(0.8);
            motor8.set(0.8);
            } else if (joystick.getRawButton(4)) {
            motor7.set(-0.8);
            motor8.set(-0.8);
            } else {
            motor7.set(0);
            motor8.set(0);
            }

            // 底盤運作
            drive.arcadeDrive(turnSpeed, driveSpeed);

            // 數值監控
            SmartDashboard.putNumber("turnSpeed", turnSpeed);
            SmartDashboard.putNumber("driveSpeed", driveSpeed);
            SmartDashboard.putNumber("motor5Pos", motorPos5);
            SmartDashboard.putNumber("motor5Spd", motorSpd5);
            SmartDashboard.putNumber("motor6Pos", motorPos6);
            SmartDashboard.putNumber("motor6Spd", motorSpd6);
        }

        @Override
        public void autonomousInit() {
            startTime = Timer.getFPGATimestamp();
        }

        @Override
        public void autonomousPeriodic() {
            double time = Timer.getFPGATimestamp();

        }
    }

Command Based:

最小單位是指令(command)，最小的執行單位是子系統(subsystem)，通常一個子系統一次只能執行一個指令。要執行指令可以透過排程(schedule)的方式去跑，當然也可以發展出相對複雜的關係(之後會出現)。

.. code-block:: java
    :caption: Drivetrain.java

    package frc.robot.Drivetrain;

    public class Drivetrain extends SwerveDrivetrain<TalonFX, TalonFX, CANcoder> implements Subsystem {
        private static final Time SimLoop = Milliseconds.of(5);
        private Notifier SimNotifer = null;
        public Vision vision;
        private static SimDrive simDrive;
        private static boolean OperatorPerspectiveApplied = false;

        private SwerveRequest.ApplyRobotSpeeds AutoDrive;
        private DoublePublisher[] CANCoderPositions;
        private DoublePublisher MotorTorque;

        public Drivetrain(SwerveDrivetrainConstants DrivetrainConstants, SwerveModuleConstants<?, ?, ?>... modules) {
            super(TalonFX::new, TalonFX::new, CANcoder::new, DrivetrainConstants,
                    Utils.isSimulation() ? SimDrive.regulateModuleConstantsForSimulation(modules) : modules);

            CANCoderPositions = new DoublePublisher[] {
                    NetworkTableInstance.getDefault().getDoubleTopic("Drivetrain/debug/FLPosition").publish(),
                    NetworkTableInstance.getDefault().getDoubleTopic("Drivetrain/debug/FRPosition").publish(),
                    NetworkTableInstance.getDefault().getDoubleTopic("Drivetrain/debug/BLPosition").publish(),
                    NetworkTableInstance.getDefault().getDoubleTopic("Drivetrain/debug/BRPosition").publish()
            };
            MotorTorque = NetworkTableInstance.getDefault().getDoubleTopic("Drivetrain/MotorTorque").publish();

            vision = Utils.isSimulation() ? new SimVision()
                    : (NetworkTableInstance.getDefault().getTable("photonvision").getTopic("version").exists())
                            ? new RealVision()
                            : null;

            AutoDrive = new ApplyRobotSpeeds()
                    .withDriveRequestType(DriveRequestType.OpenLoopVoltage)
                    .withSteerRequestType(SteerRequestType.Position)
                    .withDesaturateWheelSpeeds(true);

            AutoInit();
            if (Utils.isSimulation())
                startSim();
        }

        public Command drive(Supplier<SwerveRequest> req) {
            return run(() -> setControl(req.get()));
        }

        public Command drive(FieldPieces pieces, ReefSide side) {
            return drive(
                    pieces.getItemPose(getState().Pose, DriverStation.getAlliance().orElseThrow()).transformBy(side.getPose()))
                    .alongWith(Commands.runOnce(() -> FullState.getInstance().withDrivetrainTarget(pieces, side)));
        }

        public Command drive(Pose2d CenterPose) {
            try {
                return new PathfindingCommand(
                        offsetPose(CenterPose),
                        frc.robot.Auto.Constants.Constraints,
                        () -> getState().Pose,
                        () -> getState().Speeds,
                        (speeds, ff) -> setControl(
                                AutoDrive
                                        .withSpeeds(speeds)
                                        .withDesaturateWheelSpeeds(true)
                                        .withWheelForceFeedforwardsX(ff.robotRelativeForcesX())
                                        .withWheelForceFeedforwardsY(ff.robotRelativeForcesY())),
                        new PPHolonomicDriveController(
                                new PIDConstants(4, 0, 0),
                                new PIDConstants(8, 0, 0.02)),
                        RobotConfig.fromGUISettings(),
                        this);
            } catch (Exception e) {
                return null;
            }
        }

        /**
        * offset pose from AprilTagFieldLayout raw output
        * 
        * @param pose
        * @return
        */
        private Pose2d offsetPose(Pose2d pose) {
            return pose.plus(new Transform2d(frc.robot.Auto.Constants.RobotSize, Centimeters.of(0), Rotation2d.k180deg));
        }

        @Override
        public void resetPose(Pose2d pose) {
            if (simDrive != null)
                simDrive.mapleSimDrive.setSimulationWorldPose(pose);
            Timer.delay(0.05);
            super.resetPose(pose);
        }

        @SuppressWarnings("unchecked")
        private void startSim() {
            simDrive = new SimDrive(
                    SimLoop,
                    Constants.RobotWeight,
                    Constants.BumperSize,
                    Constants.BumperSize,
                    DCMotor.getKrakenX60Foc(1),
                    DCMotor.getKrakenX60Foc(1),
                    Constants.WheelCoF,
                    getModuleLocations(),
                    getPigeon2(),
                    getModules(),
                    Constants.SwerveMod.FrontLeft.constants,
                    Constants.SwerveMod.FrontRight.constants,
                    Constants.SwerveMod.BackLeft.constants,
                    Constants.SwerveMod.BackRight.constants);
            SimNotifer = new Notifier(simDrive::update);
            SimNotifer.setName("SimDrivetrainNotifer");
            SimNotifer.startPeriodic(SimLoop.in(Seconds));
        }

        @Override
        public void periodic() {
            if (!OperatorPerspectiveApplied || DriverStation.isDisabled())
                DriverStation.getAlliance().ifPresent(color -> setOperatorPerspectiveForward(
                        color == Alliance.Red ? Constants.RedAlliancePerspective : Constants.BlueAlliancePerspective));
            for (int i = 0; i < CANCoderPositions.length; i++)
                CANCoderPositions[i].accept(180.0 - getModule(i).getEncoder().getAbsolutePosition().getValue().in(Degrees));

            if (vision != null && vision.getPose() != null) {
                try {
                    addVisionMeasurement(vision.getPose(), Utils.getCurrentTimeSeconds());
                } catch (Exception e) {
                    DriverStation.reportWarning(
                            "Fucked up at updating Pose2d with PhotonVision with \n %s".formatted(e.getMessage()),
                            e.getStackTrace());
                }
            }

            vision.update(getState().Pose);
            MotorTorque.accept(4*getModule(1).getDriveMotor().getStatorCurrent().getValueAsDouble()*getModule(1).getDriveMotor().getMotorKT().getValueAsDouble()*Constants.DriveGearRatio*0.9/Constants.WheelRadius.times(Math.PI).in(Meters));
        }

        public void AutoInit() {
            try {
                AutoBuilder.configure(
                        () -> this.getState().Pose,
                        this::resetPose,
                        () -> this.getState().Speeds,
                        (speeds, ff) -> setControl(
                                AutoDrive
                                        .withSpeeds(speeds)
                                        .withDesaturateWheelSpeeds(true)
                                        .withWheelForceFeedforwardsX(ff.robotRelativeForcesX())
                                        .withWheelForceFeedforwardsY(ff.robotRelativeForcesY())),
                        new PPHolonomicDriveController(
                                new PIDConstants(4, 0, 0),
                                new PIDConstants(8, 0, 0.02)),
                        RobotConfig.fromGUISettings(),
                        () -> DriverStation.getAlliance().get() == Alliance.Red,
                        this);
            } catch (Exception e) {
                DriverStation.reportError("Fucked up at loading PathPlanner with \n %s".formatted(e.getMessage()),
                        e.getStackTrace());
            }
        }

        public static Drivetrain system() {
            return Constants.createDrivetrain();
        }
    }

.. code-block:: java
    :caption: RobotContainer.java

    package frc.robot;
    
    public class RobotContainer {
        public Drivetrain drivetrain = Drivetrain.system();
        public RealElevator elevator = RealElevator.system();
        public Auto auto;
        public XboxController joystick = new XboxController(0);
        public Telemetry telemetry = new Telemetry();
        public double SpeedMode = 0.4;
        public SwerveRequest.FieldCentric driveRequest = new SwerveRequest.FieldCentric()
            .withDeadband(Constants.MaxVelocity.times(0.05))
            .withRotationalDeadband(Constants.MaxOmega.times(0.05))
            .withDriveRequestType(DriveRequestType.OpenLoopVoltage)
            .withSteerRequestType(SteerRequestType.Position)
            .withDesaturateWheelSpeeds(true);

        public RobotContainer() {
            auto = new Auto(drivetrain, elevator);

            drivetrain.setDefaultCommand(drivetrain.drive(() -> driveRequest
            .withVelocityX(Constants.MaxVelocity.times(joystick.getLeftX()*SpeedMode))
            .withVelocityY(Constants.MaxVelocity.times(joystick.getLeftY()*SpeedMode))
            .withRotationalRate(Constants.MaxOmega.times(-joystick.getRightX()))));
            configureBindings();
        }

        private void configureBindings() {
            // new Trigger(() -> joystick.getLeftBumperButton()).and(() -> SpeedMode >= 0)
            //   .onTrue(Commands.runOnce(() -> SpeedMode -= 0.1));
            // new Trigger(() -> joystick.getRightBumperButton()).and(() -> SpeedMode <= 1)
            //   .onTrue(Commands.runOnce(() -> SpeedMode += 0.1));
            // new Trigger(() -> joystick.getStartButton())
            //   .onTrue(Commands.runOnce(() -> drivetrain.seedFieldCentric()));
            // new Trigger(() -> joystick.getXButton())
            //   .onTrue(drivetrain.drive(FieldPieces.CoralStation));
            new Trigger(() -> joystick.getRawButton(1)).and(() -> SpeedMode >= 0)
            .onTrue(Commands.runOnce(() -> SpeedMode -= 0.1));
            new Trigger(() -> joystick.getRawButton(2)).and(() -> SpeedMode <= 1)
            .onTrue(Commands.runOnce(() -> SpeedMode += 0.1));

            new Trigger(() -> joystick.getStartButton())
            .onTrue(Commands.runOnce(() -> drivetrain.seedFieldCentric()));
            drivetrain.registerTelemetry(telemetry::telemerize);
        }

        public Command getAutonomousCommand() {
            return auto.getAuto();
        }
    }

.. note::
    之後的小專案在一開始沒那麼複雜的時候Timed Based跟Command Based都會給，不過到比較複雜的專案(例如向量底盤)就會只有Command Based的程式
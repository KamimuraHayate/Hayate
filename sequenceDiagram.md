sequenceDiagram
    participant User
    participant Main as main()
    participant HC as HayatCar
    participant HCL as HayatCarWithListener
    participant HCLG as HayatCarWithLog
    participant TK as TimeKeeper
    participant CCT as ColorCheckerThread
    participant HND as HayatNaiveDriver
    participant HNLET as HayatNaiveLeftEdgeTracer
    participant HNRET as HayatNaiveRightEdgeTracer
    participant B as Button
    participant LCD as LCD
    participant LT as LoggerThread

    Note over User,HCLG: システム起動と初期化

    User->Main: プログラム実行
    Main->HC: HayatCar.main()が呼ばれる
    activate HC
    HC->LCD: "EdgeToggleCar"を表示
    HC->HC: HayatCarインスタンスを生成
    activate HC
    HC->CCT: ColorCheckerThread.getInstance()を呼び出し
    activate CCT
    CCT-->HC: ColorCheckerThreadインスタンスを返す
    deactivate CCT
    HC->HND: HayatNaiveDriverインスタンスを生成("B", "C"ポート指定)
    activate HND
    HND-->HC: HayatNaiveDriverインスタンスを返す
    deactivate HND
    HC->HNLET: HayatNaiveLeftEdgeTracerインスタンスを生成
    activate HNLET
    HNLET-->HC: HayatNaiveLeftEdgeTracerインスタンスを返す
    deactivate HNLET
    HC->B: Button.ENTER.addKeyListener(this)を登録
    HC->B: Button.ESCAPE.addKeyListener(this)を登録
    HC->LCD: "Mode: Left Edge "を表示
    HC->TK: start()を呼び出し
    deactivate HC
    activate TK
    TK->HC: run()を呼び出し
    activate HC

    Note over HC,HND: HayatCarの走行ループ

    loop While isActive and Color is not RED
        HC->CCT: getColorId()を呼び出し
        activate CCT
        CCT-->HC: 現在のColorIdを返す
        deactivate CCT
        HC->HNLET: decision(colorChecker, driver)を呼び出し
        activate HNLET
        HNLET->HND: turnRight()/turnLeft()/goStraight()を呼び出し
        activate HND
        HND->HND: setSpeed()
        HND->HND: モーターを駆動
        HND-->HNLET: 制御を返す
        deactivate HND
        HNLET->HND: forward()を呼び出し
        activate HND
        HND->HND: モーターを駆動
        HND-->HNLET: 制御を返す
        deactivate HND
        HNLET-->HC: 制御を返す
        deactivate HNLET
    end
    HC->HND: stop()を呼び出し (ループ終了時)
    deactivate HND
    deactivate HC

    Note over User,HC: HayatCarでのボタン操作

    User->B: ENTERボタンを押す
    B->HC: keyPressed(Button.ENTER)を通知
    activate HC
    HC->HC: isLeftEdgeを切り替える
    alt isLeftEdge == true
        HC->HNLET: HayatNaiveLeftEdgeTracerインスタンスを生成
        HC->LCD: "Mode: Left Edge "を表示
    else isLeftEdge == false
        HC->HNRET: HayatNaiveRightEdgeTracerインスタンスを生成
        HC->LCD: "Mode: Right Edge"を表示
    end
    deactivate HC

    User->B: ESCAPEボタンを押す
    B->HC: keyPressed(Button.ESCAPE)を通知
    activate HC
    HC->HC: isActive = falseに設定
    deactivate HC

    ---

    Note over User,HCLG: HayatCarWithListenerの初期化と動作

    User->Main: HayatCarWithListener.main()が呼ばれる (別の実行パス)
    activate HCL
    HCL->LCD: "ButtonEventCar"を表示
    HCL->HCL: HayatCarWithListenerインスタンスを生成
    activate HCL
    HCL->CCT: ColorCheckerThread.getInstance()を呼び出し
    CCT-->HCL: ColorCheckerThreadインスタンスを返す
    HCL->HND: HayatNaiveDriverインスタンスを生成
    HND-->HCL: HayatNaiveDriverインスタンスを返す
    HCL->HNLET: HayatNaiveLeftEdgeTracerインスタンスを生成
    HNLET-->HCL: HayatNaiveLeftEdgeTracerインスタンスを返す
    HCL->HNRET: HayatNaiveRightEdgeTracerインスタンスを生成
    HNRET-->HCL: HayatNaiveRightEdgeTracerインスタンスを返す
    HCL->LT: LoggerThread.getInstance()を呼び出し
    activate LT
    LT-->HCL: LoggerThreadインスタンスを返す
    deactivate LT
    HCL->LT: setCar(this)を呼び出し
    activate LT
    LT-->HCL: 制御を返す
    deactivate LT
    HCL->B: Button.ESCAPE.addKeyListener(this)を登録
    HCL->CCT: addColorChangeListener(this)を登録
    HCL->TK: start()を呼び出し
    deactivate HCL
    activate TK
    TK->HCL: run()を呼び出し
    activate HCL

    Note over HCL,HND: HayatCarWithListenerの走行ループとイベント

    loop While isActive
        HCL->CCT: getColorId()を呼び出し
        CCT-->HCL: 現在のColorIdを返す
        HCL->HNLET: decision(colorChecker, driver)を呼び出し (またはHNRET)
        activate HNLET
        HNLET->HND: driver操作
        deactivate HNLET
    end
    HCL->HND: stop()を呼び出し (ループ終了時)
    deactivate HCL

    User->B: ESCAPEボタンを押す
    B->HCL: keyPressed(Button.ESCAPE)を通知
    activate HCL
    HCL->HCL: isActive = falseに設定
    HCL->HND: stop()を呼び出し
    deactivate HCL

    CCT->HCL: colorChangeDetected(Color.RED)を通知
    activate HCL
    HCL->HCL: isActive = falseに設定
    HCL->HND: stop()を呼び出し
    deactivate HCL

    ---

    Note over User,HCLG: HayatCarWithLogの初期化と動作

    User->Main: HayatCarWithLog.main()が呼ばれる (別の実行パス)
    activate HCLG
    HCLG->HCLG: HayatCarWithLogインスタンスを生成
    activate HCLG
    HCLG->CCT: ColorCheckerThread.getInstance()を呼び出し
    CCT-->HCLG: ColorCheckerThreadインスタンスを返す
    HCLG->HND: HayatNaiveDriverインスタンスを生成
    HND-->HCLG: HayatNaiveDriverインスタンスを返す
    HCLG->HNLET: HayatNaiveLeftEdgeTracerインスタンスを生成
    HNLET-->HCLG: HayatNaiveLeftEdgeTracerインスタンスを返す
    HCLG->HNRET: HayatNaiveRightEdgeTracerインスタンスを生成
    HNRET-->HCLG: HayatNaiveRightEdgeTracerインスタンスを返す
    HCLG->LT: LoggerThread.getInstance()を呼び出し
    LT-->HCLG: LoggerThreadインスタンスを返す
    HCLG->LT: setCar(this)を呼び出し
    LT-->HCLG: 制御を返す
    HCLG->TK: start()を呼び出し
    deactivate HCLG
    activate TK
    TK->HCLG: run()を呼び出し
    activate HCLG

    Note over HCLG,HND: HayatCarWithLogの走行ループ

    loop While ESCAPE button not pressed and Color is not RED
        HCLG->B: Button.ESCAPE.isDown()をチェック
        B-->HCLG: ボタンの状態を返す
        HCLG->CCT: getColorId()を呼び出し
        CCT-->HCLG: 現在のColorIdを返す
        HCLG->HNLET: decision(colorChecker, driver)を呼び出し (またはHNRET)
        activate HNLET
        HNLET->HND: driver操作
        deactivate HNLET
    end
    deactivate HCLG
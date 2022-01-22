// シリアル通信のサンプルコードです。
// シリアル経由でトリガーを受信したら、LEDを点滅します。
static uint8_t g_flg = 0;
static int g_led = LOW;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, g_led);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if (g_flg) {
    //シリアル経由でトリガーを受信したら実行する処理を記述します。 
    if (LOW == g_led) {
      g_led = HIGH;
    } else {
      g_led = LOW;
    }
    digitalWrite(13, g_led);
    g_flg = 0;
  }
  serialEvent();
}

void serialEvent() {
    uint8_t tmp = 0;
    while (Serial.available() > 0) {
      tmp = Serial.read();
      Serial.write(tmp);
      if (tmp == 'a') {
        g_flg = 1; 
      }
    }  
}

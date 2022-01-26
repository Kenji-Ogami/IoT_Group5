// シリアル通信のサンプルコードです。
// シリアル経由でトリガーを受信したら、LEDを点滅します。

#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

SoftwareSerial mySerial(10, 11); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

static uint8_t g_flg = 0;
static int g_led = LOW;
void setup() {
  // put your setup code here, to run once:
  mySerial.begin(9600);
  Serial.begin(9600);
  if (!myDFPlayer.begin(mySerial)) {
    // DFPlayerを初期化します。USBピンを使ってなければ、デバイスはSD(TF)カードが選択されます
    Serial.println(F("Unable to begin:"));
    while (true) {
      delay(0); // Code to compatible with ESP8266 watch dog.
    }
  }
  
  Serial.println(F("DFPlayer Mini online."));
  myDFPlayer.volume(25);  // ボリュームをセット、 ボリュームは0から30の値で指定可能
  delay(1000);
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
    
    myDFPlayer.play(1);  // 先頭のmp3ファイルを再生
    delay(28000);
    delay(10000);
    
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

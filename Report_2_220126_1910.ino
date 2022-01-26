#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

SoftwareSerial mySerial(10, 11); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

void setup() {
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
}

void loop() {
  myDFPlayer.play(1);  // 先頭のmp3ファイルを再生
  delay(28000);
  delay(10000);
}

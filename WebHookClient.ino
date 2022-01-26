#include <Arduino.h>
#include <HTTPServer.h>
#include <ESP32Interface.h>

ESP32Interface network;
#define WIFI_SSID "MY-WiFi-SSID"
#define WIFI_PW "WiFi-PASSWORD"
const char * IFTTT_EVENT = "request_received";
const char * IFTTT_KEY = "MY-IFTTT-KEY";

char flg = 0;
long rnd = 0;
void ub0_interrupt() {
  while (digitalRead(PIN_SW0) == LOW)
    ;
  flg = 1;
  rnd = random(0,9999);
}


void setup() {
  char buf[128];
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PIN_SW0, INPUT);
  attachInterrupt(4, ub0_interrupt, FALLING);
  randomSeed(analogRead(0));
  
  Serial.println("Starts.");
 
  Serial.print("Connecting Wi-Fi..");
  network.connect(WIFI_SSID, WIFI_PW, NSAPI_SECURITY_WPA_WPA2);
  Serial.println("done");
 
  Serial.print("MAC Address is ");
  Serial.println(network.get_mac_address());
  Serial.print("IP Address is ");
  Serial.println(network.get_ip_address());
  Serial.print("NetMask is ");
  Serial.println(network.get_netmask());
  Serial.print("Gateway Address is ");
  Serial.println(network.get_gateway());
  Serial.println("Network Setup OK\r\n");
  
}


void loop() {
  // put your main code here, to run repeatedly: 
  
  if (flg) {
    char buf[128];
    TCPSocket socket;
    nsapi_error_t response;
    response = socket.open(&network);
    if(0 != response) {
        sprintf(buf, "socket.open() failed: %d\n", response);
        Serial.print(buf);
        return;
    }
    
    response = socket.connect("maker.ifttt.com", 80);
    if(0 != response) {
        sprintf(buf, "Error connecting: %d\n", response);
        Serial.print(buf);
        socket.close();
        return;
    }
    

    char url[256];
    sprintf(url, "POST /trigger/%s/with/key/%s HTTP/1.1\r\nHost: maker.ifttt.com\r\nContent-Type: application/json\r\nContent-Length: 17\r\n\r\n{\"value1\":\"%04d\"}Connection: keep-alive\r\n\r\n",IFTTT_EVENT, IFTTT_KEY, rnd);
    //Serial.println(url);
    nsapi_size_t size = strlen(url);
   
    // Loop until whole request send
    while(size) {
      response = socket.send(url+response, size);
      if (response < 0) {
          sprintf(buf, "Error sending data: %d\n", response);
          Serial.print(buf);
          socket.close();
          return;
      }
      size -= response;
      sprintf(buf, "sent %d [%.*s]\n", response, strstr(sbuffer, "\r\n")-sbuffer, sbuffer);
      Serial.print(buf);
    }
   
    // Receieve a simple http response and print out the response line
    char rbuffer[64];
    response = socket.recv(rbuffer, sizeof rbuffer);
    if (response < 0) {
        sprintf(buf, "Error receiving data: %d\n", response);
        Serial.print(buf);
    } else {
        sprintf(buf, "recv %d [%.*s]\n", response, strstr(rbuffer, "\r\n")-rbuffer, rbuffer);
        Serial.print(buf);
    }
   
    // Close the socket to return its memory and bring down the network interface
    socket.close();
    flg = 0;
  }
  
}

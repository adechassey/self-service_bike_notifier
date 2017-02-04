/********** Utils functions **********/

String macToStr(const uint8_t* mac) {
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    //if (i < 5)
    //result += ':';
  }
  return result;
}

const char* client_MAC() {
  unsigned char mac[6];
  WiFi.macAddress(mac);
  String clientMac = macToStr(mac);
  return String(clientMac).c_str();
}



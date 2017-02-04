/********** Controller functions **********/

void control(int bikes, int spots) {
  // red
  if (bikes == 0) {
    leds[0] = CRGB(255, 0, 0);
    FastLED.show();
  }
  if (spots == 0) {
    leds[1] = CRGB(255, 0, 0);
    FastLED.show();
  }

  // orange
  if (bikes > 0 && bikes <= 2) {
    leds[0] = CRGB(255, 128, 0);
    FastLED.show();
  }
  if (spots > 0 && spots <= 2) {
    leds[1] = CRGB(255, 128, 0);
    FastLED.show();
  }

  // blue
  if (bikes > 2 && bikes <= 5) {
    leds[0] = CRGB(0, 0, 255);
    FastLED.show();
  }
  if (spots > 2 && spots <= 5) {
    leds[1] = CRGB(0, 0, 255);
    FastLED.show();
  }

  // green
  if (bikes > 5) {
    leds[0] = CRGB(0, 255, 0);
    FastLED.show();
  }
  if (spots > 5) {
    leds[1] = CRGB(0, 255, 0);
    FastLED.show();
  }
}


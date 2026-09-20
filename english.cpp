#include "USB.h"
#include "USBHIDKeyboard.h"

USBHIDKeyboard Keyboard;

const uint8_t braillePins[6] = {15, 5, 4, 46, 11, 12};
const uint8_t keyConfirm = 14;
const uint8_t keySpace   = 40;
const uint8_t keyEnter   = 2;
const uint8_t keyBack    = 35;

String currentPattern = "";

struct Pair {
  const char* pattern;
  char letter;
};

Pair table[] = {
  {"100000",'A'}, {"110000",'B'}, {"100100",'C'}, {"100110",'D'},
  {"100010",'E'}, {"110100",'F'}, {"110110",'G'}, {"110010",'H'},
  {"010100",'I'}, {"010110",'J'}, {"101000",'K'}, {"111000",'L'},
  {"101100",'M'}, {"101110",'N'}, {"101010",'O'}, {"111100",'P'},
  {"111110",'Q'}, {"111010",'R'}, {"011100",'S'}, {"011110",'T'},
  {"101001",'U'}, {"111001",'V'}, {"010111",'W'}, {"101101",'X'},
  {"101111",'Y'}, {"101011",'Z'}
};

char decode(String p){
  for(auto &t : table){
    if(p == t.pattern) return t.letter;
  }
  return '?';
}

void setup(){
  USB.begin();
  Keyboard.begin();

  for(int i=0;i<6;i++)
    pinMode(braillePins[i], INPUT_PULLUP);

  pinMode(keyConfirm, INPUT_PULLUP);
  pinMode(keySpace, INPUT_PULLUP);
  pinMode(keyEnter, INPUT_PULLUP);
  pinMode(keyBack, INPUT_PULLUP);
}

void loop(){
  // зчитуємо 6 тактильних кнопок
  currentPattern = "";
  for(int i=0;i<6;i++){
    currentPattern += digitalRead(braillePins[i]) ? "0" : "1";
  }

  // підтвердження = надрукувати букву
  if(!digitalRead(keyConfirm)){
    char l = decode(currentPattern);
    if(l!='?') Keyboard.print(l);
    delay(300);
  }

  if(!digitalRead(keySpace)){
    Keyboard.print(" ");
    delay(300);
  }

  if(!digitalRead(keyEnter)){
    Keyboard.write(KEY_RETURN);
    delay(300);
  }

  if(!digitalRead(keyBack)){
    Keyboard.write(KEY_BACKSPACE);
    delay(300);
  }
}

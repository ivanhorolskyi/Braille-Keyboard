#include <Keyboard.h>

// ===== Піни Брайля =====
const int braillePins[6] = {15, 26, 27, 7, 6, 5};

// ===== Додаткові кнопки =====
const int confirmPin = 4;
const int spacePin   = 3;
const int enterPin   = 2;
const int deletePin  = 1;

// ===== Структура: Брайль → ALT =====
struct BrailleAlt {
  const char* pattern;
  const char* alt;
};

// ===== Таблиця символів =====
BrailleAlt table[] = {
  // ===== ЛІТЕРИ =====
  {"100000","0192"}, {"110000","0193"}, {"010111","0194"},
  {"110110","0195"}, {"110111","0165"}, {"100110","0196"},
  {"100010","0197"}, {"001110","0170"}, {"010110","0198"},
  {"101011","0199"}, {"010100","0200"}, {"101111","0178"},
  {"100111","0175"}, {"111101","0201"}, {"101000","0202"},
  {"111000","0203"}, {"101100","0204"}, {"101110","0205"},
  {"101010","0206"}, {"111100","0207"}, {"111010","0208"},
  {"011100","0209"}, {"011110","0210"}, {"101001","0211"},
  {"110100","0212"}, {"110010","0213"}, {"100100","0214"},
  {"111110","0215"}, {"100011","0216"}, {"101101","0217"},
  {"011111","0220"}, {"110011","0222"}, {"110101","0223"},

  // ===== ПУНКТУАЦІЯ =====
  {"010000","0044"}, // ,
  {"010011","0046"}, // .
  {"011000","0059"}, // ;
  {"010010","0058"}, // :
  {"011010","0033"}, // !
  {"011001","0063"}, // ?
  {"001000","0039"}, // '
  {"001001","0045"}, // -
  {"011011","0034"}  // "
};

const int tableSize = sizeof(table) / sizeof(table[0]);

// ===== Відправка ALT-коду через NumPad =====
void sendAltCode(const char* code) {
  Keyboard.press(KEY_LEFT_ALT);
  delay(50);

  for (int i = 0; code[i] != '\0'; i++) {
    switch (code[i]) {
      case '0': Keyboard.write(KEY_KP_0); break;
      case '1': Keyboard.write(KEY_KP_1); break;
      case '2': Keyboard.write(KEY_KP_2); break;
      case '3': Keyboard.write(KEY_KP_3); break;
      case '4': Keyboard.write(KEY_KP_4); break;
      case '5': Keyboard.write(KEY_KP_5); break;
      case '6': Keyboard.write(KEY_KP_6); break;
      case '7': Keyboard.write(KEY_KP_7); break;
      case '8': Keyboard.write(KEY_KP_8); break;
      case '9': Keyboard.write(KEY_KP_9); break;
    }
    delay(30);
  }

  Keyboard.release(KEY_LEFT_ALT);
  delay(50);
}

// ===== Зчитування Брайля =====
String readBraille() {
  String p = "";
  for (int i = 0; i < 6; i++) {
    p += (digitalRead(braillePins[i]) == LOW) ? '1' : '0';
  }
  return p;
}

// ===== Пошук ALT-коду =====
const char* findAlt(const String& pattern) {
  for (int i = 0; i < tableSize; i++) {
    if (pattern == table[i].pattern) {
      return table[i].alt;
    }
  }
  return nullptr;
}

void setup() {
  Keyboard.begin();

  for (int i = 0; i < 6; i++) {
    pinMode(braillePins[i], INPUT_PULLUP);
  }

  pinMode(confirmPin, INPUT_PULLUP);
  pinMode(spacePin,   INPUT_PULLUP);
  pinMode(enterPin,   INPUT_PULLUP);
  pinMode(deletePin,  INPUT_PULLUP);
}

void loop() {
  static bool lastConfirm = HIGH;
  static bool lastSpace   = HIGH;
  static bool lastEnter   = HIGH;
  static bool lastDelete  = HIGH;

  bool confirmState = digitalRead(confirmPin);
  bool spaceState   = digitalRead(spacePin);
  bool enterState   = digitalRead(enterPin);
  bool deleteState  = digitalRead(deletePin);

  // ===== Підтвердження символу =====
  if (lastConfirm == HIGH && confirmState == LOW) {
    delay(50);
    String pattern = readBraille();
    const char* alt = findAlt(pattern);
    if (alt != nullptr) {
      sendAltCode(alt);
    }
    delay(300);
  }

  // ===== Пробіл =====
  if (lastSpace == HIGH && spaceState == LOW) {
    delay(50);
    Keyboard.write(' ');
    delay(200);
  }

  // ===== Enter =====
  if (lastEnter == HIGH && enterState == LOW) {
    delay(50);
    Keyboard.write(KEY_RETURN);
    delay(200);
  }

  // ===== Backspace =====
  if (lastDelete == HIGH && deleteState == LOW) {
    delay(50);
    Keyboard.write(KEY_BACKSPACE);
    delay(200);
  }

  lastConfirm = confirmState;
  lastSpace   = spaceState;
  lastEnter   = enterState;
  lastDelete  = deleteState;
}
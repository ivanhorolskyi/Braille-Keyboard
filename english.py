#include <Keyboard.h>

// Піни Брайля
const int braillePins[6] = {4, 3, 2, 7, 8, 9};

// Піни додаткових кнопок
const int confirmPin = 10;
const int spacePin = 14;
const int enterPin = 15;
const int deletePin = 16;

// Структура: шаблон Брайля → Alt-код
struct BrailleAlt {
  const char* pattern;
  const char* alt;
};

BrailleAlt table[] = {
  {"100000","0192"}, // а
  {"110000","0193"}, // б
  {"010111","0194"}, // в
  {"110110","0195"}, // г
  {"110111","0165"}, // ґ
  {"100110","0196"}, // д
  {"100010","0197"}, // е
  {"001110","0170"}, // є
  {"010110","0198"}, // ж
  {"101011","0199"}, // з
  {"010100","0200"}, // и
  {"101111","0178"}, // і
  {"100111","0175"}, // ї
  {"111101","0201"}, // й
  {"101000","0202"}, // к
  {"111000","0203"}, // л
  {"101100","0204"}, // м
  {"101110","0205"}, // н
  {"101010","0206"}, // о
  {"111100","0207"}, // п
  {"111010","0208"}, // р
  {"011100","0209"}, // с
  {"011110","0210"}, // т
  {"101001","0211"}, // у
  {"110100","0212"}, // ф
  {"110010","0213"}, // х
  {"100100","0214"}, // ц
  {"111110","0215"}, // ч
  {"100011","0216"}, // ш
  {"101101","0217"}, // щ
  {"011111","0220"}, // ь
  {"110011","0222"}, // ю
  {"110101","0223"}, // я
  {"010000","0044"}, // ,  запятая
  {"010011","0046"}, // .  точка
  {"010010","0059"}, // ;  точка с запятой
  {"010001","0058"}, // :  двоеточие
  {"011001","0033"}, // !  восклицательный знак
  {"011010","0063"}, // ?  вопросительный знак
};

const int tableSize = sizeof(table) / sizeof(table[0]);

// ===== Функція Alt-коду через NumPad =====
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
    p += digitalRead(braillePins[i]) == LOW ? '1' : '0';
  }
  return p;
}

// ===== Пошук Alt-коду по шаблону =====
const char* findAlt(String pattern) {
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
  pinMode(spacePin, INPUT_PULLUP);
  pinMode(enterPin, INPUT_PULLUP);
  pinMode(deletePin, INPUT_PULLUP);
}

void loop() {
  static bool lastConfirm = HIGH;
  static bool lastSpace = HIGH;
  static bool lastEnter = HIGH;
  static bool lastDelete = HIGH;

  bool confirmState = digitalRead(confirmPin);
  bool spaceState = digitalRead(spacePin);
  bool enterState = digitalRead(enterPin);
  bool deleteState = digitalRead(deletePin);

  // ===== Кнопка підтвердження =====
  if (lastConfirm == HIGH && confirmState == LOW) {
    delay(50); // debounce
    String pattern = readBraille();
    const char* alt = findAlt(pattern);
    if (alt != nullptr) {
      sendAltCode(alt);
    }
    delay(300); // антидребезг
  }

  // ===== Кнопка пробіл =====
  if (lastSpace == HIGH && spaceState == LOW) {
    delay(50);
    Keyboard.write(' ');
    delay(200);
  }

  // ===== Кнопка Enter =====
  if (lastEnter == HIGH && enterState == LOW) {
    delay(50);
    Keyboard.write(KEY_RETURN);
    delay(200);
  }

  // ===== Кнопка Delete (Backspace) =====
  if (lastDelete == HIGH && deleteState == LOW) {
    delay(50);
    Keyboard.write(KEY_BACKSPACE); // теперь удаляет предыдущий символ
    delay(200);
  }

  lastConfirm = confirmState;
  lastSpace = spaceState;
  lastEnter = enterState;
  lastDelete = deleteState;
}

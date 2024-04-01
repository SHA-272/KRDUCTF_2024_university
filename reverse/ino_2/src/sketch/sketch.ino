#define A 8
#define B 7
#define C 6
#define D 5
#define E 4
#define F 3
#define G 2

const byte values[][7] = {
  { 1, 0, 1, 1, 1, 1, 1 },
  { 0, 0, 1, 1, 1, 1, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 1, 0, 1, 1, 0, 1 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 0, 1, 1, 0, 0, 1, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 0, 1, 1, 0, 1, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 0, 0, 1, 1, 1, 1, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 0, 1, 1, 0, 0, 1, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 1, 0, 1, 1, 0, 1 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 0, 1, 1, 0, 0, 1, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 0, 1, 1, 0, 1, 1 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 1, 1, 1, 1, 0, 1, 1 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 1, 0, 0, 1, 1, 1, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 1, 1, 1, 1, 1, 1, 0 },
  { 1, 0, 1, 1, 0, 1, 1 },
  { 1, 0, 0, 0, 1, 1, 1 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 1, 1, 1, 1, 1, 1, 0 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 1, 0, 1, 1, 0, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 0, 1, 1, 1, 1, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 1, 1, 1, 1, 0, 0, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 1, 1, 0, 1, 1, 0, 1 },
  { 1, 1, 1, 0, 0, 0, 0 },
  { 0, 1, 1, 1, 1, 0, 1 }
};

void setup() {
  pinMode(A, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(C, OUTPUT);
  pinMode(D, OUTPUT);
  pinMode(E, OUTPUT);
  pinMode(F, OUTPUT);
  pinMode(G, OUTPUT);
}

void loop() {
  for (int i = 0; i < sizeof(values) / sizeof(values[0]); i++) {
    displayPattern(values[i]);
    delay(1000);
  }
}

void displayPattern(const byte pattern[]) {
  digitalWrite(A, pattern[0]);
  digitalWrite(B, pattern[1]);
  digitalWrite(C, pattern[2]);
  digitalWrite(D, pattern[3]);
  digitalWrite(E, pattern[4]);
  digitalWrite(F, pattern[5]);
  digitalWrite(G, pattern[6]);
}

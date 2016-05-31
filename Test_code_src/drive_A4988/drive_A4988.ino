
void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);

}

void loop() {
  digitalWrite(3, HIGH);
  digitalWrite(3, LOW);
  delay(1000);
}

/*
 Role: Test for the current sequence.
 Electronics: TI DRV8823 Stepper driver
 Board: Robopoly's PRismino.
 
 Step 1: APH 1, AEN 1, BPH x, BEN 0
 Step 2: APH x, AEN 0, BPH 1, BEN 1
 Step 3: APH 0, AEN 1, BPH x, BEN 0
 Step 4: APH x, AEN 0, BPH 0, BEN 1

 0 100.0% 0.0% full step
 1 100.0%* 19.5% 1/8 step
 2 92.4% 38.2% 1/4 step
 3 83.1% 55.5% 3/8 step
 4 70.7% 70.7% 1/2 step
 5 55.5% 83.1% 5/8 step
 6 38.2% 92.4% 3/4 step
 7 19.5% 100.0% 7/8 step
 8 0.0% 100.0% full step
*/

uint8_t res = 4;

uint8_t state = 0;
uint16_t base = 0;
int count = 0;
bool forward = true;

uint8_t current[] = {0b000, 0b011, 0b110, 0b111};

#define APH  1
#define AEN  0
#define BPH  7
#define BEN  6

#define A10  2
#define B10  8

#define DATA  0
#define CLK   1
#define SSTB  7

void setup() {
  pinMode(SSTB, OUTPUT);
  pinMode(DATA, OUTPUT);
  pinMode(CLK, OUTPUT);
  Serial.begin(9600);
  digitalWrite(SSTB, LOW);
  digitalWrite(DATA, LOW);
  digitalWrite(CLK, LOW);

  Serial.begin(9600);
}

void loop() {
  state = count%(4*res);
  base = 0;

  if (res == 2)
  {
        Serial.println(base);
        if (state == 0)
        {
                base |= (1 << AEN) | (1 << APH);
                base |= (current[3] << A10);
        }
        if (state == 1)
        {
                base |= (1 << AEN) | (1 << APH) | (1 << BEN) | (1 << BPH);
                base |= (current[1] << A10) | (current[1] << B10);
        }
        if (state == 2)
        {
                base |= (1 << BEN) | (1 << BPH);
                base |= (current[3] << B10);
        }
        if (state == 3)
        {
                base |= (1 << AEN) | (1 << BEN) | (1 << BPH);
                base |= (current[1] << A10) | (current[1] << B10);
        }
        if (state == 4)
        {
                base |= (1 << AEN);
                base |= (current[3] << A10);
        }
        if (state == 5)
        {
                base |= (1 << AEN) | (1 << BEN);
                base |= (current[1] << A10) | (current[1] << B10);
        }
        if (state == 6)
        {
                base |= (1 << BEN);
                base |= (current[3] << B10);
        }
        if (state == 7)
        {
                base |= (1 << AEN) | (1 << APH) | (1 << BEN);
                base |= (current[1] << A10) | (current[1] << B10);
        }
  }
  else if (res == 4)
  {
        if (state == 0) {
                base |= (1 << AEN) | (1 << APH);
                base |= (current[3] << A10); }
        else if ((state > 0) && (state < 4)) {
                base |= (1 << AEN) | (1 << APH) | (1 << BEN) | (1 << BPH);
                base |= (current[3-state] << A10) | (current[state-1] << B10); }
        else if (state == 4) {
                base |= (1 << BEN) | (1 << BPH);
                base |= (current[3] << B10); }
        else if ((state > 4) && (state < 8)) {
                base |= (1 << AEN) | (1 << BEN) | (1 << BPH);
                base |= (current[state-5] << A10) | (current[7-state] << B10); }
        else if (state == 8) {
                base |= (1 << AEN);
                base |= (current[3] << A10); }
        else if ((state > 8) && (state < 12)) {
                base |= (1 << AEN) | (1 << BEN);
                base |= (current[11-state] << A10) | (current[state-9] << B10); }
        else if (state == 12) {
                base |= (1 << BEN);
                base |= (current[3] << B10); }
        else if ((state > 12) && (state < 16)) {
                base |= (1 << AEN) | (1 << APH) | (1 << BEN);
                base |= (current[state-13] << A10) | (current[15-state] << B10); }
  }
  else if (res == 8)
  {
        if (state == 0) {
               base |= (1 << AEN) | (1 << APH);
               base |= (0b111 << A10); }
        if ((state > 0) && (state < 8 )) {
               base |= (1 << AEN) | (1 << APH) | (1 << BEN) | (1 << BPH);
               base |= ((7-state) << A10) | ((state-1) << B10); }
        if (state == 8) {
                base |= (1 << BEN) | (1 << BPH);
                base |= (0b111 << B10); }
         if ((state > 8) && (state < 16)) {
                base |= (1 << AEN) | (1 << BEN) | (1 << BPH);
                base |= ((state-9) << A10) | ((15-state) << B10); }
         if (state == 16) {
                base |= (1 << AEN);
               base |= (0b111 << A10); }
        if ((state > 16) && (state < 24)){
               base |= (1 << AEN) | (1 << BEN);
               base |= ((23-state) << A10) | ((state-17) << B10); }
         if (state == 24) {
               base |= (1 << BEN);
               base |= (0b111 << B10); }
         if ((state > 24) && (state < 32)) {
                base |= (1 << AEN) | (1 << APH) | (1 << BEN);
               base |= ((state-25) << A10) | ((31-state) << B10);}
  }

  
  for(uint8_t i = 0; i < 16; i++)
  {
    digitalWrite(DATA, (base & (1 << i)) >> i);
    digitalWrite(CLK, HIGH);
    digitalWrite(CLK, LOW);
  }
  
  digitalWrite(SSTB, HIGH);
  digitalWrite(SSTB, LOW);

  Serial.print(state);
  Serial.print(": ");
  Serial.println(base, BIN);

  if(forward)
  {
    count++;
    if(count > 199)
      forward = false;
  }
  else
  {
    count--;
    if(count < 0)
      forward = true;
  }
      
  delay(1000);
}

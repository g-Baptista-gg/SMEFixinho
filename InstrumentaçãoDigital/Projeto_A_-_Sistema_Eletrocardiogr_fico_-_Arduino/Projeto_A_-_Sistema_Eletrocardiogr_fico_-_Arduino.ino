/* Time related variables */
unsigned long currentTime;
unsigned long previousTime = 0; //Time of last data aquisition
unsigned long timeR = 0; //Time of last R wave detection
unsigned long deadTime = 0; //Time when the heart stopped beating
unsigned long previousTimeEnd = 0; //Time of last byte received
unsigned long interval = 20; //Time interval between data aquisitions
unsigned long timeEnd = 500; //Maximum time allowed without receiving bytes before stopping aquisition

/* Pins connected */
int ecg = A1;
int propranolol = 6;
int atropina = 7;
int pacemaker = 8;
int desfibrilhador = 9;

/* Aquisition and serial communication variables */
int data; //10-bit data
int dataByte; //8-bit data
float bpm;

/* R waves detection limits */
float upperLimit = 170;
float lowerLimit = 150;

/* Flag variables */
bool R = 0; //R wave
bool flag1 = 0; //Propanolol
bool flag2 = 0; //Atropina
bool flag3 = 0; //Pacemaker
bool flag4 = 0; //Desfibrilhador

void setup() {  
  Serial.begin(9600); //Begins serial communication

  /* Setup of connected pins */
  pinMode(ecg, INPUT);
  pinMode(propranolol, OUTPUT);
  pinMode(atropina, OUTPUT);
  pinMode(pacemaker, OUTPUT);
  pinMode(desfibrilhador, OUTPUT);
}

void loop() {
  currentTime = millis();
  
  if (Serial.available() > 0) {
    int inByte = Serial.read();

    switch (inByte) {
      case 'a':
        interval = 40; //Sampling rate: 25 S/s
        break;
      case 'b':
        interval = 20; //Sampling rate: 50 S/s
        break;
      case 'c':
        interval = 10; //Sampling rate: 100 S/s
        break;
      case 'd':
        interval = 5; //Sampling rate: 200 S/s
        break;
      case 'e':
        //Serial.end();
        break;
      case 'f':
        digitalWrite(propranolol, HIGH); //Turn on propanolol LED test
        break;
      case 'g':
        digitalWrite(propranolol, LOW); //Turn off propanolol LED test
        break;
      case 'h':
        digitalWrite(atropina, HIGH); //Turn on atropina LED test
        break;
      case 'i':
        digitalWrite(atropina, LOW); //Turn off atropina LED test
        break;
      case 'j':
        digitalWrite(pacemaker, HIGH); //Turn on pacemaker LED test
        break;
      case 'k':
        digitalWrite(pacemaker, LOW); //Turn off pacemaker LED test
        break;
      case 'l':
        digitalWrite(desfibrilhador, HIGH); //Turn on desfribilhador LED test
        break;
      case 'm':
        digitalWrite(desfibrilhador, LOW); //Turn off desfribilhador LED test
      }
  }

  /* It makes aquisitions with a certain sampling rate and sends them to the computer through serial communication */
  if (currentTime - previousTime >= interval) {
    data = analogRead(ecg);
    dataByte = map(data, 0, 1023, 0, 255);
    Serial.println(dataByte);
    previousTime = currentTime; //Updates previousTime
  }

  /* It detects sucessive R waves and calculates the number of BPM's */
  if (dataByte >= upperLimit && R == 0) {
    bpm = 60000/(currentTime - timeR);
    timeR = currentTime; //Updates timeR
    R = 1; //Updates R
  }
  if (dataByte <= lowerLimit && R == 1) {
    R = 0; //Updates R
  }

  /* It activates the injection of propanolol if the number of BPM's exceed 160 and deactivates it otherwise */
  if (bpm > 160 && flag1 == 0) {
    digitalWrite(propranolol, HIGH);
    flag1 = 1; //Updates flag1
  }
  if (bpm <= 160 && flag1 == 1) {
    digitalWrite(propranolol, LOW);
    flag1 = 0; //Updates flag1
  }

  /* It activates the injection of atropina if the number of BPM's is between 30 and 40, and deactivates it otherwise */
  if (bpm >= 30 && bpm <= 40 && flag2 == 0) {
    digitalWrite(atropina, HIGH);
    flag2 = 1; //Updates flag2
  }
  if ((bpm < 30 || bpm > 40) && flag2 == 1) {
    digitalWrite(atropina, LOW);
    flag2 = 0; //Updates flag2
  }

  /* It activates a pacemaker if the number of BPM's is between 6 and 30, and deactivates it otherwise */
  if (bpm >= 6 && bpm <= 30 && flag3 == 0) {
    digitalWrite(pacemaker, HIGH);
    flag3 = 1; //Updates flag3
  }
  if ((bpm < 6 || bpm > 30) && flag3 == 1) {
    digitalWrite(pacemaker, LOW);
    flag3 = 0; //Updates flag3
  }

  /* It activates a "desfribilhador" for 5 seconds if there's no new R wave detection in the last 10 seconds, even if halfway through the 5 seconds there's a R wave detection */
  if (currentTime - timeR >= 10000 && flag4 == 0) {
    digitalWrite(desfibrilhador, HIGH);
    deadTime = currentTime; //Updates deadTime
    flag4 = 1; //Updates flag4
  }
  if (currentTime - deadTime >= 5000 && flag4 == 1) {
    digitalWrite(desfibrilhador, LOW);
    flag4 = 0; //Updates flag4
  }

  /* It stops the aquisition and communication of data if the Arduino doesn't receive a new byte in a certain amount of time */
  if (currentTime - previousTimeEnd >= timeEnd) {
    //Serial.end();
  }
  
}

#include <Servo.h>

byte sensorPin = A0;  // select the input pin for the IR sensor
int sensorValue = 0;  // variable to store the value coming from the sensor

// create servo objects to control the servos
Servo horz_servo;
Servo vert_servo;

// variables to store the servo positions
int h_pos = 0;
int v_pos = 0;

// How wide the servos should rotate
byte h_degrees = 45;
byte v_degrees = 45;

// The number of steps the servos take per sweep.
byte h_points = 20;
byte v_points = 20;

// How many degrees each step should be
float h_step_width = (float) h_degrees / h_points;
float v_step_width = (float) v_degrees / v_points;

// How long each step should take.
byte h_delay = 200;
byte v_delay = 200;

// How many times we should read the IR sensor at each step. The higher this
// number, the more accurate the result. This could potentially slow the scan
// however.
byte data_read_num = 5;

// variable to store the current time
unsigned long time;

void setup()
{
  horz_servo.attach(9);  // attaches the servo on pin 9 to the servo object
  vert_servo.attach(13);  // attaches the servo on pin 13 to the servo object
  Serial.begin(9600);
}

// going_down is 1 on way down, 0 on way up. This function sweeps the
// horizantal servo
void horz_sweep(byte j, byte going_down)
{

  if (j % 2 == going_down)
  {
    for (byte i = 0; i < h_points; i += 1)
    {
      time = millis();  // register current time
      h_pos = i * h_step_width;  // set servo to new position
      horz_servo.write(h_pos);
      delay(h_delay / 2);  // sleep for half of the wait time to give the servo
      // time to move before we read in the data

      // probe the sensor multiple times and average the results
      int temp_Value = 0;
      for (byte k = 0; k < data_read_num; k += 1)
        temp_Value += analogRead(sensorPin);
      sensorValue = temp_Value / data_read_num;

      // print to the serial and sleep the remaining time
      Serial.println(String(sensorValue) + ", " + String(i) + ", " +
                     String(j));
      delay(h_delay - (millis() - time));
    }
  }

  else
  {
    for (byte i = h_points - 1; i >= 0; i -= 1)
    {
      time = millis();
      h_pos = i * h_step_width;
      horz_servo.write(h_pos);
      delay(h_delay / 2);

      int temp_Value = 0;
      for (byte k = 0; k < data_read_num; k += 1)
        temp_Value += analogRead(sensorPin);
      sensorValue = temp_Value / data_read_num;

      Serial.println(String(sensorValue) + ", " + String(i) + ", " +
                     String(j));
      delay(h_delay - (millis() - time));
    }
  }
}

// this function sweeps the vertical servo down then up, while sweeping the
// horizantal servo at each step
void vert_sweep()
{
  for (byte j = 0; j < v_points; j += 1)
  {
    v_pos = j * v_step_width;  // set servo to new position
    vert_servo.write(v_pos);
    horz_sweep(j, 1);  // sweep the horizantal servo
    delay(v_delay);
  }

  for (byte j = v_points - 1; j >= 0; j -= 1)
  {
    v_pos = j * step_width;  // set servo to new position
    vert_servo.write(v_pos);
    horz_sweep(j, 0);  // sweep the horizantal servo
    delay(v_delay);
  }
}

void loop()
{
  vert_sweep();
}

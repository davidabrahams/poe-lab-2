#include <Servo.h>

int sensorPin = A0;  // select the input pin for the potentiometer
int sensorValue = 0;  // variable to store the value coming from the sensor

Servo horz_servo;  // create servo object to control a servo
Servo vert_servo;  // create servo object to control a servo

int h_pos = 0;    // variable to store the servo position
int v_pos = 0;    // variable to store the servo position

int h_degrees = 45;
int v_degrees = 45;

int h_points = 20;
int v_points = 20;

int h_delay = 100;
int v_delay = 100;

unsigned long time;

void setup()
{
  horz_servo.attach(9);  // attaches the servo on pin 9 to the servo object
  vert_servo.attach(13);  // attaches the servo on pin 13 to the servo object
  Serial.begin(9600);
}

// going_down is 1 on way down, 0 on way up
void horz_sweep(int j, int going_down)
{

  if (j % 2 == going_down)
  {
    for (int i = 0; i < h_points; i += 1)
    {
      time = millis();
      float h_step_width = (float) h_degrees / h_points;
      int horz_position = i * h_step_width; // j*step_width
      horz_servo.write(horz_position);
      delay(h_delay / 2);

      int temp_Value = 0;
      for (int k = 0; k < 5; k += 1)
        temp_Value += analogRead(sensorPin);
      sensorValue = temp_Value / 5;

      Serial.println(String(sensorValue) + ", " + String(i) + ", " +
                     String(j));
      delay(h_delay - (millis() - time));
    }
  }

  else
  {
    for (int i = h_points; i >=0; i -= 1)
    {
      time = millis();
      float h_step_width = (float) h_degrees / h_points;
      int horz_position = i * h_step_width; // j*step_width
      horz_servo.write(horz_position);
      delay(h_delay / 2);

      int temp_Value = 0;
      for (int k = 0; k < 5; k += 1)
        temp_Value += analogRead(sensorPin);
      sensorValue = temp_Value / 5;

      Serial.println(String(sensorValue) + ", " + String(i) + ", " +
                     String(j));
      delay(h_delay - (millis() - time));
    }
  }

}

void loop()
{

  for (int j = 0; j < v_points; j += 1)
  {
    float v_step_width = (float) v_degrees / v_points;
    int vert_position = j * v_step_width; // j*step_width
    vert_servo.write(vert_position);
    horz_sweep(j, 1);
    delay(v_delay);
  }

  for (int j = v_points - 1; j >= 0; j -= 1)
  {
    float step_width = (float) v_degrees / v_points;
    int vert_position = j * step_width; // j*step_width
    vert_servo.write(vert_position);
    horz_sweep(j, 0);
    delay(v_delay);
  }
}

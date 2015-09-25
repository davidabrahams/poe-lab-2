/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo horz_servo;  // create servo object to control a servo
Servo vert_servo;  // create servo object to control a servo

int h_pos = 0;    // variable to store the servo position
int v_pos = 0;    // variable to store the servo position

int h_degrees = 90;
int v_degrees = 45;

int h_points = 20;
int v_points = 5;

void setup()
{
  horz_servo.attach(9);  // attaches the servo on pin 9 to the servo object
  vert_servo.attach(13);  // attaches the servo on pin 13 to the servo object
}

// going_down is 1 on way down, 0 on way up
void horz_sweep(int j, int going_down)
{

  if (j % 2 == going_down)
  {
    for (int i = 0; i < h_points; i += 1)
    {
      float h_step_width = (float) h_degrees / h_points;
      int horz_position = i * h_step_width; // j*step_width
      horz_servo.write(horz_position);
      delay(75);
    }
  }

  else
  {
    for (int i = h_points; i >=0; i -= 1)
    {
      float h_step_width = (float) h_degrees / h_points;
      int horz_position = i * h_step_width; // j*step_width
      horz_servo.write(horz_position);
      delay(75);
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
    delay(75);
  }

  for (int j = v_points - 1; j >= 0; j -= 1)
  {
    float step_width = (float) v_degrees / v_points;
    int vert_position = j * step_width; // j*step_width
    vert_servo.write(vert_position);
    horz_sweep(j, 0);

    delay(75);
  }
}

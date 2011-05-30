/*
////////////////////////////////////////////////////////////////////// 

   8x8led Arduino Code
   https://github.com/kevincon/8x8led
  
   Facilitates updating Modern Device <http://www.moderndevice.com> 
   8x8 LED panels via serial. Strings sent to Arduino's hw serial
   should be terminated with a newline character.
  
   Copyright (c) 2011 Kevin Conley, kevindconley@gmail.com
  
   Uses and requires Panel8x8 Arduino library, 
   Copyright (c) 2009 Dataman aka Charley Jones, 8x8Panel@CRJones.Com
   
 
   This file is part of 8x8led.

   8x8led is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   8x8led is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with 8x8led.  If not, see <http://www.gnu.org/licenses/>.
   
//////////////////////////////////////////////////////////////////////
*/

// Please remember to set PANELS to the physical number of
// panels to support in Panel8x8.h -- defaults to 4.
// In most cases for 1-4 panels this won't make any difference.

// Required include for the Panel8x8 library
#include <Panel8x8.h>

// Declare an object of type Panel8x8
Panel8x8 Panel;

// Declare the text to be displayed in RAM at startup
char buffer[512]={"  Waiting for input..."};

// Called once by ardruino to setup the sketch
void setup() {
 // Initialize hardware serial for 9600 baud
 Serial.begin(9600);
 
 // Call Panel.Begin to initialize panel buffers
 // Syntax: buffer address, max buffer size, current text size, 0=Ram/1=Flash
 Panel.Begin(buffer,512,strlen(buffer),0);
};

// Called repeatedly by arduino
void loop() {
  uint8_t sr; // Byte for reading chars over serial
  int start_flag = 1; // Flag to indicate first run of below loop 
  
  // If serial data waiting to be read  
  if (Serial.available() > 0) {
    // Newline char indicates end of received string
    while (sr != '\n') {
      // Change PanelMode from 1 so it doesn't scroll
      Panel.PanelMode = 11;
       // Read in a char
      sr  = Serial.read();

      // On first run of this loop, clear panels and init vars
      if(start_flag) {
	      Panel.ClearOutput();

	      Panel.bIsScrolling=true;

	      Panel.iBufferLen=0;

	      start_flag = 0;
      }
      
      // If sr is newline, done with adding text
      if(sr == '\n')
	break;
      // Also done if nothing else will fit in buffer
      else if(Panel.iBufferLen == Panel.iBufferSize - 1) {
	break;
      }	

      // Write received char to panel, increment buffer pos
      Panel.WriteByte(Panel.iBufferLen++, sr); 
      
    } //end of while(Serial.available()>0) loop
    
    // Write null char to panel output buffer
    // signifies end of message to scroll
    Panel.WriteByte(Panel.iBufferLen,0); 

    // Set PanelMode back to text scrolling
    Panel.PanelMode = 1; 

    // Tell panels to reset for the new msg
    Panel.NewMessage();
   
    // Reset start flag
    start_flag = 1; 
    return;
  } //end of if(Serial.available()>0)
  
  // Call Panel.Loop to pump the panels
  Panel.Loop();  
};

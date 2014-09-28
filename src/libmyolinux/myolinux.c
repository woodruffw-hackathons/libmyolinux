/*

    License: MIT

    Authors: ...

    This library provides parsing and abstraction capabilities
    for dealing with the Myo Armband on Linux. This library takes
    the raw bluetooth packet data and outputs the current state:
    gesture information, acceleration data, and other data supplied
    by the Windows and Mac Myo libraries.

*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

typedef struct {

    float acc_x;
    float acc_y;
    float acc_z;
    float w;
    float x;
    float y;
    float z;
    //float roll;
    //float pitch;
    //float yaw;
    unsigned char gesture;
    unsigned char arm;    

}Packet;

float raw_to_float(const unsigned char *raw){

    return *(float *)raw;

}

Packet *init_packet(const unsigned char *raw_data){

    Packet *packet;

    unsigned char acc_x[4];  memcpy(acc_x,raw_data,4);
    unsigned char acc_y[4]; memcpy(acc_y,raw_data+4,4);
    unsigned char acc_z[4]; memcpy(acc_z,raw_data+8,4);
    
    /* --- slice the quat --- */
    unsigned char w[4]; memcpy(w,raw_data+12,4);
    unsigned char x[4]; memcpy(x,raw_data+16,4);
    unsigned char y[4]; memcpy(y,raw_data+20,4);
    unsigned char z[4]; memcpy(z,raw_data+24,4);
    
    unsigned char gesture = raw_data[28];
    unsigned char arm = raw_data[29];

    /* --- allocate memory for struct --- */

    packet = (Packet *) malloc(sizeof(Packet));
    
    /* --- parse & cast into fields --- */
    
    packet->acc_x = raw_to_float(acc_x);
    packet->acc_y = raw_to_float(acc_y);
    packet->acc_z = raw_to_float(acc_z);

    packet->w = raw_to_float(w);
    packet->x = raw_to_float(x);
    packet->y = raw_to_float(y);
    packet->z = raw_to_float(z);

    //---TODO:calc_euler(packet); roll/pitch/yaw

    packet->gesture = gesture;
    packet->arm = arm;

    return packet;
}

int destroy_packet(Packet *data){
    
    free(data);
    return 0;
}

const char *get_gesture(Packet *data){
    
    const char *unknown = "unknown";
    const char *rest = "rest";
    const char *fist = "fist";
    const char *waveIn = "waveIn";
    const char *waveOut = "waveOut";
    const char *fingersSpread = "fingersSpread";
    const char *reserved1 = "reserved1";
    const char *thumbToPinky = "thumbToPinky";

    switch(data->gesture){

	case 0:
	    return rest;
	case 1:
	    return fist;
	case 2:
	    return waveIn;
	case 3:
	    return waveOut;
	case 4:
	    return fingersSpread;
	case 5:
	    return reserved1;
	case 6:
	    return thumbToPinky;
	default:
	    return unknown;
    }
}

const char *get_arm(Packet *data){

    const char *right = "R";
    const char *left = "L";

    switch (data->arm){
	case 0:
	    return right;
	default:
	    return left;
    }
}

int parse_packet(const unsigned char *raw){

    Packet *p = init_packet(raw);

    printf("x=%f\ty=%f\tz=%f\tval=%f\n", p->acc_x, p->acc_y, p->acc_z, p->w);
 
    printf("gesture=%s\narm=%s\n", get_gesture(p), get_arm(p));
    destroy_packet(p);

    return 0;

}

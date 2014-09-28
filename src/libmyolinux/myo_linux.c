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

typedef struct {

    float acc_x;
    float acc_y;
    float acc_z;
    float acc_val;
    float x;
    float y;
    float z;
    unsigned char gesture;
    unsigned char hand;    

}Packet;

float raw_to_float(const unsigned char *raw){

    return *(float *)raw;

}

Packet *init_packet(const unsigned char *raw_data){

    Packet *packet;

    unsigned char acc_x[4] = memcpy(acc_x,raw_data,4);
    unsigned char acc_y[4] = memcpy(acc_y,raw_data+4,4);
    unsigned char acc_z[4] = memcpy(acc_z,raw_data+8,4);
    unsigned char acc_val[4] = memcpy(acc_val,raw_data+12,4);
    
    /* --- slice crazy packed nonsense (TODO) --- */
    //+16
    //+20
    //+24
    unsigned char gesture = memcpy(&gesture,raw_data+28,1);
    unsigned char hand = memcpy(&gesture,raw_data+29,1);

    /* --- allocate memory for struct --- */

    packet = (Packet *) malloc(sizeof(Packet));
    
    /* --- parse & cast into fields --- */
    
    packet->acc_x = raw_to_float(acc_x);
    packet->acc_y = raw_to_float(acc_y);
    packet->acc_z = raw_to_float(acc_z);
    packet->acc_val = raw_to_float(acc_val);
    //filler
    packet->gesture = gesture;
    packet->hand = hand;

    return packet;
}

int destroy_packet(Packet *data){
    
    free(data);
    return 0;
}

int getGesture(Packet *data){

    //check implementation
    return 0;
}

int main(){

    unsigned char data[30] = {'a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a'};

    Packet *p = init_packet();

}

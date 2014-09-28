#ifndef myolinux_h__
#define myolinux_h__

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

} Packet;

extern float raw_to_float(const unsigned char*);
extern Packet *init_packet(const unsigned char*);
extern int destroy_packet(Packet*);
extern const char *get_gesture(Packet*);
extern const char *get_arm(Packet*);
extern int parse_packet(const unsigned char*);
extern int parse_gesture(const unsigned char*);
#endif

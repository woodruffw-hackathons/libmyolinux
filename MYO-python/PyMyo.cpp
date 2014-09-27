// Copyright (C) 2013-2014 Thalmic Labs Inc.
// Distributed under the Myo SDK license agreement. See LICENSE.txt for details.
// Modified to expose Myo data to Python
// Paul Lutz
// Scott Martin
// Fabricate.IO
#include <iostream>
#include <thread>
#include <mutex>
#include <myo/myo.hpp>

// Indicates the Myo is not on an arm
#define OFF_ARM 'A'

// Timeout to raise exception if no myo found
#define FIND_MYO_TIMEOUT_MS 10000

// Update loop period - 50ms = 20Hz
#define UPDATE_EVENT_PD_MS 50

// Sizes of rotation & accel arrays
#define QUAT_ARR_SZ 4
#define ACCEL_ARR_SZ 3

// Receives events from Myo devices
class DataCollector : public myo::DeviceListener {
private:
	// Variables to hold current Myo state
    bool onArm;
    myo::Arm whichArm;
    myo::Pose currentPose;

	float quat_arr[QUAT_ARR_SZ]; //stores w, x, y, and z rotation
	float accel_arr[ACCEL_ARR_SZ];

	myo::Myo* myMyo;
	std::mutex myoMutex; // Prevents vibration while polling for data

public:
    DataCollector() : onArm(false), currentPose() {
		for(int i = 0; i < QUAT_ARR_SZ; i++) {
			quat_arr[i] = 0.0;
		}
		for(int i = 0; i < ACCEL_ARR_SZ; i++) {
			accel_arr[i] = 0.0;
		}
    }

	// This is used later by the vibrator
	void setMyo(myo::Myo* myo) {
		myMyo = myo;
	}

	void setLock(bool lock) {
		if (lock) {
			myoMutex.lock();
		} else {
			myoMutex.unlock();
		}
	}

    // Called whenever the Myo device provides its current orientation, which is represented
    // as a unit quaternion.
    void onOrientationData(myo::Myo* myo, uint64_t timestamp, const myo::Quaternion<float>& quat) {
		quat_arr[0] = quat.w();
		quat_arr[1] = quat.x();
		quat_arr[2] = quat.y();
		quat_arr[3] = quat.z();
    }

    // Called whenever the Myo detects that the person wearing it has changed their pose, for example,
    // making a fist, or not making a fist anymore.
    void onPose(myo::Myo* myo, uint64_t timestamp, myo::Pose pose) {
		currentPose = pose;
    }

    // Called whenever Myo has recognized a setup gesture after someone has put it on their
    // arm. This lets Myo know which arm it's on and which way it's facing.
    void onArmRecognized(myo::Myo* myo, uint64_t timestamp, myo::Arm arm, myo::XDirection xDirection) {
        onArm = true;
        whichArm = arm;
    }

    // Called whenever Myo has detected that it was moved from a stable position on a person's arm after
    // it recognized the arm. Typically this happens when someone takes Myo off of their arm, but it can also happen
    // when Myo is moved around on the arm.
    void onArmLost(myo::Myo* myo, uint64_t timestamp) {
        onArm = false;
    }

	// Called when the Myo sends acceleration data.
	void onAccelerometerData (myo::Myo* myo, uint64_t timestamp, const myo::Vector3<float> &accel) {
		accel_arr[0] = accel.x();
		accel_arr[1] = accel.y();
		accel_arr[2] = accel.z();
	}

	// Vibrates the Myo
	void vibrate(myo::Myo::VibrationType duration) {
		if (!myMyo) {
			std::cerr << "Myo not set!";
			exit(2);
		}

		myoMutex.lock();
		myMyo->vibrate(duration);
		myoMutex.unlock();
	}

    // Prints the current values that were updated by the on...() functions above.
    void print() {

		// Prints x, y, and z acceleration of the Myo
		for(int i = 0; i < ACCEL_ARR_SZ; i++) {	
			char* bits = reinterpret_cast<char*>(&accel_arr[i]);
			for(int n = 0; n < sizeof(float); ++n) {
				std::cout << (bits[n]);
			}
		}

		// Prints w, x, y, and z rotation of the Myo
		for(int i = 0; i < QUAT_ARR_SZ; i++) {
			char* bits = reinterpret_cast<char*>(&quat_arr[i]);
			for(int n = 0; n < sizeof(float); ++n) {
				std::cout << (bits[n]);
			}
		}

		// Prints Pose byte
		unsigned char poseByte;
		poseByte = currentPose.type() & 0xFF;
		std::cout << poseByte;

		// Prints which arm the Myo is on: 0 = right, 1 = left
		if(onArm) {
			std::cout << (unsigned char)whichArm;
		} else {
			std::cout << OFF_ARM;
		}

        std::cout << '\n';
        std::cout << std::flush; // Prevent caching multiple lines so each line is written immediately
    }
};
DataCollector collector;

// Reads integer values from the console to control vibration
void inputThread() {
    std::string input;
	while(true) {
		std::cin >> input;
		if(std::cin.fail()) {
			std::exit(0);
		}

		collector.vibrate((myo::Myo::VibrationType)input[0]);
	}
}

int main(int argc, char** argv)
{
    try {
		myo::Hub hub("com.fabricate.pyo"); // This provides access to one or more Myos.

		myo::Myo* myo = hub.waitForMyo(FIND_MYO_TIMEOUT_MS);
		if (!myo) {
			throw std::runtime_error("Unable to find a Myo!");
		}
		collector.setMyo(myo);	     // Used as a reference for vibration
		hub.addListener(&collector); // Tell the hub to send data events to the collector

		// This thread reads vibration commands
		std::thread t1 (inputThread);
		t1.detach();

		while (true)  {
			collector.setLock(true); // Prevent vibration thread from writing while we read
			hub.run(UPDATE_EVENT_PD_MS); // Allow myo to push events at the given rate
			collector.setLock(false);
			collector.print();
		}
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
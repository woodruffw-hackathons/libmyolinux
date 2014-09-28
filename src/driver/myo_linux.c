#include <linux/module.h>
#include <linux/config/h>
#include <linux/init.h>

static int __init myo_linux_init(void){

    printk("Loading myo_linux module...\n");
    return 0;

}

static void __exit myo_linux_exit(void){

    printk("Unloading myo_linux module...\n");
    return;

}

module_init(myo_linux_init);
module_exit(myo_linux_exit);

MODULE_LICENSE("MIT");


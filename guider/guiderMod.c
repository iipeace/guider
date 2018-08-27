#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/hrtimer.h>
#include <linux/jiffies.h>
#include <linux/ktime.h>

#define MS_TO_NS(x) (x * 1E6L)

static struct hrtimer guider_timer;
static ktime_t ktime;

enum hrtimer_restart guider_hrtimer_callback(struct hrtimer *timer)
{
    ktime_t now = hrtimer_cb_get_time(&guider_timer);

    //printk("guider_timer called\n");

    hrtimer_forward(&guider_timer, now, ktime);

    return HRTIMER_RESTART;
}

int init_module(void)
{
    unsigned long delay_in_ms = 1L;

    printk("guider_timer registered\n");

    ktime = ktime_set(0, MS_TO_NS(delay_in_ms));

    hrtimer_init(&guider_timer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);

    guider_timer.function = &guider_hrtimer_callback;

    hrtimer_start(&guider_timer, ktime, HRTIMER_MODE_REL);

    return 0;
}

void cleanup_module(void)
{
    int ret;

    ret = hrtimer_cancel(&guider_timer);

    if (ret)
        printk("guider_timer is still in use\n");
    else
        printk("guider_timer unloaded\n");
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Peace Lee");

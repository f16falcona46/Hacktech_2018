#!/bin/sh

echo 0 > /sys/class/pwm/pwmchip0/unexport
echo 0 > /sys/class/pwm/pwmchip0/export
sudo chown pi /sys/class/pwm/pwmchip0/pwm0/*
echo 20000000 > /sys/class/pwm/pwmchip0/pwm0/period
echo 800000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

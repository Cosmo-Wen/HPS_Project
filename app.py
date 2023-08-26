import RPi.GPIO as GPIO
import time

Full = 9

def setup_sensor(trig_pin, echo_pin):
    GPIO.setup(trig_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(echo_pin, GPIO.IN)

def check_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(trig_pin, GPIO.LOW)
    
    while not GPIO.input(echo_pin):
        pass
    t1 = time.time()
    
    while GPIO.input(echo_pin):
        pass
    t2 = time.time()
    
    distance = (t2 - t1) * 340 * 100 / 2
    
    # 限制測量距離在3cm到21cm之間，超出21cm時輸出垃圾桶已滿的值
    if distance < 3:
        distance = 3
    elif distance > 21:
        distance = Full - 0.5
    
    return distance

# 計算平均值
def get_mean(distances):
    if distances:
        return sum(distances) / len(distances)
    else:
        return None

# 獲取多次測量距離值列表
def get_distances(trig_pin, echo_pin, num_measurements):
    distances = []
    for _ in range(num_measurements):
        distance = check_distance(trig_pin, echo_pin)
        distances.append(distance)
        time.sleep(0.1)
    return distances

def is_trash_can_full(reference_distance):
    if reference_distance is not None:
        print('平均距離：%0.2f 公分' % reference_distance)
        if reference_distance < Full:
            return True
        else:
            return False
    else:
        print('無法確定參考距離')
        return None

if __name__ == "__main__":
    try:
        sensor1_Trigger = 20
        sensor1_Echo = 21
        sensor2_Trigger = 22
        sensor2_Echo = 23

        GPIO.setmode(GPIO.BCM)
        
        setup_sensor(sensor1_Trigger, sensor1_Echo)
        setup_sensor(sensor2_Trigger, sensor2_Echo)
        
        while True:
            distances1 = get_distances(sensor1_Trigger, sensor1_Echo, 10)
            distances2 = get_distances(sensor2_Trigger, sensor2_Echo, 10)
            
            reference_distance1 = get_mean(distances1)  # 使用平均值代替眾數
            reference_distance2 = get_mean(distances2)  # 使用平均值代替眾數
            
            is_full_sensor1 = is_trash_can_full(reference_distance1)
            is_full_sensor2 = is_trash_can_full(reference_distance2)
            
            if is_full_sensor1 and is_full_sensor2:
                print('垃圾桶滿了')
            else:
                print('垃圾桶沒有滿')
        
    except KeyboardInterrupt:
        GPIO.cleanup()
from PIL import Image
import time
import psutil 

img = Image.open('/home/thaddaeus/FMU/HRL/LAH2.0/efforts/theta/q_and_per_work/q_work/best_routine_so_far/plots/0.709:ID:GDR1_2066790146043148928.png')
img.show()
time.sleep(5)
for proc in psutil.process_iter():
    if proc.name()=='display':
        proc.kill()


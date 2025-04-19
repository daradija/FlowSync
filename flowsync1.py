import numpy as np

class Phase:
    def __init__(self,intersection,split ):
        self.intersection = intersection
        self.split = split
        self.io=[]

    def open(self, input, output,distance,velocity):
        self.io.append((input, output, Road(distance, velocity)))


class Intersection:
    def __init__(self, inputs, outputs,phases):
        self.input = inputs
        self.output = outputs
        self.phases = [Phase(self,0.5) for _ in range(phases)]
        self.offset = 0
        self.cycle = 90
        self.t = 0

    def run(self):
        second_cicle=(self.t - self.offset)% self.cycle
        phase=second_cicle/self.cycle

        split=0
        for p in self.phases:
            change=split+p.split
            if phase < change:
                changet=(change-split)*self.cycle+self.t
                # print("Change phase", changet)
                for intersection in p.io:
                    input=self.input[intersection[0]]
                    output=self.output[intersection[1]]
                    road=intersection[2]
                    if road.freeInputTime < changet:
                        for t,v in input.get(max(self.t,road.freeInputTime),changet):
                            # empty input
                            road.push(t,v)
                            if road.freeInputTime > changet:
                                break        
                    # Empty the intersection
                    for t,v in road.queue:
                        output.push(t,v)
                    road.queue=[]
                    for p in self.phases:
                        for intersection in p.io:
                            intersection[2].freeInputTime=road.freeInputTime
                self.t=changet
                break
            split=change
        return True
        # print(f"Second cicle: {second_cicle}")
        # print()

class Road:
    def __init__(self, length, velocity):
        self.length = length
        self.velocity = velocity
        self.queue=[]
        self.freeInputTime=0

    def velocityms(self):
        # Convert velocity from km/h to m/s
        return self.velocity / 3.6
    
    def push(self, time, vehicle):
        if time < self.freeInputTime:
            time=self.freeInputTime
        # Hay que hallar a que hora se admite una nueva entrada
        # Es el tiempo de entrada a la velocidad de la via
        # v= e/t => t=e/v
        self.freeInputTime=time+vehicle.totalDistance(self.velocity)/self.velocityms()
        # A que hora sale cabeza y cola 
        self.queue.append((time+self.length/self.velocityms(), vehicle))
        
    def get(self, time, time_to):
        # puede ocurrir tres cosas: delante, en medio, detrás.
        waiting=0
        if self.queue[0][0] < time:
            waiting=time-self.queue[0][0]

        
        while True:
            q=self.queue[0]
            if q[0]+waiting <time_to:
                self.queue.pop(0)
                yield (q[0]+waiting,q[1])
            else:
                break


    
class Vehicle:
    def __init__(self, length):
        self.length = length

    def totalDistance(self,velocity):
        if velocity == 0:
            return 1.5+self.length
        if velocity <= 30:
            return 17
        if velocity <= 50:
            return 28
        

def main():
    road0= Road(100, 50)
    road1= Road(100, 50)

    road3= Road(100, 50)
    road4= Road(100, 50)

    # Create an intersection with 2 inputs and 2 outputs
    intersection = Intersection([road0,road1], [road3,road4],2)


    intersection.phases[0].open(0,0,5,30)
    intersection.phases[1].open(1,1,5,30)


    vehicle= Vehicle(4.2)

    time=0
    while time<60*60: # 1 hour of simulation
        road=None
        if np.random.random() < 0.5:
            road=road0
        else:
            road=road1

        road.push(time,vehicle)
        # v=e/t => t=e/v
        time+= vehicle.totalDistance(road.velocity)/road.velocityms()

    while intersection.run():
        pass


if __name__ == "__main__":
    main()